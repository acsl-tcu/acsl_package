#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WHILL Chair CRの制御ROSプログラム\n
Auther:Koki Yamaguchi \n
year:2022 \n
"""
import os
import traceback
from time import sleep, time

import rclpy
from geometry_msgs.msg import Twist, Vector3
from rclpy.node import Node
from std_msgs.msg import Bool, Float64, Int16
from whill import ComWHILL


class whill_ope(ComWHILL):
    def __init__(self, ros, port='/dev/ttyUSB-WhillCR'):
        super().__init__(port)
        self.ros = ros
        # データ受信のコールバック関数の定義
        self.register_callback('data_set_0', self.callback0)
        self.register_callback('data_set_1', self.callback1)
        # 電源が入ったことを通知するCallBackの定義
        self.register_callback('power_on', self.power_on_callback)

        # 電源オン
        self.send_power_on_com(1)
        self.start_data_stream(100)
        while 1:
            if self.power_status == 1:
                break
            else:
                self.refresh()

        # モードプロファイルの読み込み
        self.request_speed_profile()

        # モードの設定
        speedmode = 3
        """
        0 : mode1
        1 : mode2
        2 : mode3
        3 : mode4
        4 : 外部入力
        5 : スマホ入力
        """
        self.set_speed_profile_via_dict(
            speedmode, self.speed_profile[speedmode])

        self.send_joystick(int(0), int(0))  # TODO ジョイスティックコマンド

    def callback0(self):  # コールバック関数0のモードプロファイル
        # print(self.speed_profile[self.speed_mode_indicator])
        pass

    def callback1(self):
        """WHILLからのデータを取得するコールバック関数1
        主にモーターの角度やスピード，走行モード，ジョイスティックの入力など逐次的にデータが変わるものが対象
        """
        # ROS2メッセージの初期化
        level = Int16()
        current = Float64()
        motor_angle = Vector3()
        motor_speed = Vector3()
        speedmode = Int16()
        joy = Vector3()

        # データの格納
        level.data, current.data = self.battery.values()
        motor_angle.x, motor_speed.x = self.right_motor.values()
        motor_angle.y, motor_speed.y = self.left_motor.values()
        speedmode.data = self.speed_mode_indicator
        joy_x, joy_y = self.joy.values()
        joy.x = float(joy_x)
        joy.y = float(joy_y)

        # ROS2へトピックの配信
        self.ros.puber_battery_level.publish(level)
        self.ros.puber_battery_current.publish(current)
        self.ros.puber_motor_angle.publish(motor_angle)
        self.ros.puber_motor_speed.publish(motor_speed)
        self.ros.puber_speedmode.publish(speedmode)
        self.ros.puber_joy.publish(joy)

    def power_on_callback(self):
        """Whillから電源が入ったことを知らされた際に実行する関数"""
        print('WHILL wakes up')

    def send_power_on_com(self, io):
        """whillのイグニッションを管理するための関数"""
        if io:
            self.send_power_on()
        else:
            self.send_power_off()

    def request_speed_profile(self, profile_list=[0, 1, 2, 3, 4, 5]):
        """速度モードの一覧をリクエストする関数"""
        for i in profile_list:
            old_count = self.seq_data_set_0
            self.start_data_stream(10, 0, i)
            while old_count == self.seq_data_set_0:
                self.refresh()
        self.start_data_stream(100)

    def velocity2joy(self, v, w):
        """速度・角速度入力をジョイスティック入力に変換する関数"""
        d = 0.5  # ホイール間距離
        pf = self.speed_profile[self.speed_mode_indicator]
        if 0.0 <= v:
            # 前進と後進で変換が違う為分岐
            front_joy = min(100.0 * v / (pf["forward_speed"] / 36), 100)
        else:
            front_joy = max(100.0 * v / (pf["reverse_speed"] / 36), -100)
        turn_v = -w * d  # 円旋回の定義で単位変換している
        side_joy = max(min(100, 100.0 * turn_v /
                       (pf["turn_speed"] / 36)), -100)
        # print(front_joy , side_joy)
        return front_joy, side_joy


class node(Node):
    def __init__(self) -> None:
        super().__init__("whill")
        # 初期値の設定
        self.sub_vel_t = time()
        self.v = 0
        self.w = 0

        # ROS2 subscriberを定義する
        self.create_subscription(
            Twist, '~/cmd_vel', self.sub_cmd_vel, 1)  # ROS速度コマンドの送信
        self.create_subscription(
            Bool, '~/cmd_power', self.sub_cmd_power, 1)  # Whillのイグニッションを設定する

        # ROS2 Publisherを定義している
        self.puber_battery_level = self.create_publisher(
            Int16, "~/battery_level", 10)
        self.puber_battery_current = self.create_publisher(
            Float64, "~/battery_current", 10)
        self.puber_motor_angle = self.create_publisher(
            Vector3, "~/motor_angle", 10)
        self.puber_motor_speed = self.create_publisher(
            Vector3, "~/motor_speed", 10)
        self.puber_speedmode = self.create_publisher(
            Int16, "~/speed_mode", 10)
        self.puber_joy = self.create_publisher(
            Vector3, "~/joy", 10)

        # whillへの接続フェーズ
        self.whill = whill_ope(self)

        dt = 0.03  # 制御周期
        self.create_timer(dt, self.mainloop)

    def sub_cmd_vel(self, topic):
        """速度・角速度指令トピックを購読し構造体に格納する関数"""
        self.v = topic.linear.x
        self.w = topic.angular.z
        self.sub_vel_t = time()

    def sub_cmd_power(self, topic):
        """電源の制御に関するトピックを購読しWHILLの電源を制御する関数"""
        self.whill.send_power_on_com(topic.data)

    def pub_battey_stat(self, level, current):
        """バッテリーの状態をトピック配信する関数"""
        self.puber_battery_level.publish(level)
        self.puber_battery_current.publish(current)

    def mainloop(self):
        """メインの実行関数\n
        コンストラクタで設定した制御周期でジョイスティックコマンドを送信する．
        """
        if time() < 1.0 + self.sub_vel_t:
            joy_x, joy_y = self.whill.velocity2joy(self.v, self.w)
            self.whill.send_joystick(int(joy_x), int(joy_y))
        else:
            joy_x = 0
            joy_y = 0
            self.whill.send_joystick(int(0), int(0))
            command_bytes = [self.whill.CommandID.SET_JOYSTICK,
                             self.whill.UserControl.ENABLE, 0, 0]
            self.whill.send_command(command_bytes)
        self.whill.refresh()


def main(args=None):
    rclpy.init(args=args)
    ros = node()
    ros.get_logger().info('WHILL ready!!')
    try:
        rclpy.spin(ros)  # ROSのコールバック実行・終了待機
    except KeyboardInterrupt:
        ros.get_logger().info('Shutdown')
    except:
        traceback.print_exc()  # エラーが発生した場合のエラー出力

    # システムが終了するときには必ず．ジョイスティックコマンドが[0,0]を出力
    ros.whill.send_joystick(int(0), int(0))
    sleep(1)
    ros.whill.send_power_on_com(0)  # 電源OFF

    # ROSノードの終了
    ros.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
