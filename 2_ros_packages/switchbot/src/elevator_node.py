#! /bin/python3
import rclpy
from rclpy.node import Node
from bluepy.btle import Scanner, DefaultDelegate
from rclpy.action import ActionServer, ActionClient
from std_msgs.msg import String, Int8, Bool, Int32MultiArray
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # カレントディレクトリの移動
sys.path.append(os.path.join(os.path.dirname(__file__)))  # パスの追加
# parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))
# sys.path.append(parent_dir)

from switchbot_controller import trigger_device

from rclpy.callback_groups import ReentrantCallbackGroup
from interfaces.action import Switchbot

# 最終的に開発していくバージョン


class MAIN(Node):

    def __init__(self):
        super().__init__("elevator_node")
        # self.msg2elevator_subscriber = self.create_subscription(
        #     Int32MultiArray,
        #     '~/robot2elevator',
        #     self.listener_callback,
        #     1)

        self.msg2robot_publisher = self.create_publisher(
            Int32MultiArray, "/robot_node/elevator2robot", 1
        )

        # timer_period = 1.0  # seconds
        # self.timer = self.create_timer(timer_period, self.elevator_callback)

        # self.msg2elevator_subscriber.data = [0, 0, 0]
        self.result = False

        # アクションサーバーの初期化
        self._action_server = ActionServer(
            self,
            Switchbot,
            "~/Switchbot",
            self.elevator_callback,
            callback_group=ReentrantCallbackGroup(),
        )

    # def listener_callback(self, msg):
    #     # self.get_logger().info('I heard: "%s"'% msg.data)
    #     print("Subscribing:", msg.data)
    #     self.msg2elevator_subscriber.data = msg.data

    # def elevator_callback(self):# ゴールが送信されたときに呼ばれるコールバック
    def elevator_callback(self, goal_handle):
        self.get_logger().info("Executing goal...")

        self.request = goal_handle.request.order[0]
        self.floor = goal_handle.request.order[1]
        self.target_floor = goal_handle.request.order[2]

        self.get_logger().info(
            "{0:}階から{1:}階へ移動".format(self.floor, self.target_floor)
        )

        feedback_msg = Switchbot.Feedback()
        feedback_msg.progress = "swichbot startup"
        goal_handle.publish_feedback(feedback_msg)

        # if goal_handle.request.order == 1:
        #     result.progress = trigger_device(['e9:9b:41:91:67:dd', 'Bot', 'Press'])

        if self.request == 0:
            feedback_msg.progress = "待機"
            goal_handle.publish_feedback(feedback_msg)
            goal_handle.succeed()

        elif self.request == 1:  # エレベータを呼ぶ：上の階へ行くとき
            if self.floor == 1:
                feedback_msg.progress = "1 <<--"
                goal_handle.publish_feedback(feedback_msg)
                # self.result = trigger_device(["e9:9b:41:91:67:dd", "Bot", "Press"])
                self.result = trigger_device(["D7:39:08:1C:0E:79", "Bot", "Press"])
                
                if self.result:
                    goal_handle.succeed()
                    feedback_msg.progress = "Success!"
                else:
                    goal_handle.abort()
                    feedback_msg.progress = "Failure..."
            elif self.floor == 2:
                feedback_msg.progress = "2 <<--"
                goal_handle.publish_feedback(feedback_msg)
                # self.result = trigger_device(["c0:da:18:24:ac:20", "Bot", "Press"])  # botがない
                self.result = trigger_device(["D7:39:08:1C:0E:79", "Bot", "Press"])
                if self.result:
                    goal_handle.succeed()
                    feedback_msg.progress = "Success!"
                else:
                    goal_handle.abort()
                    feedback_msg.progress = "Failure..."
            elif self.floor == 3:
                feedback_msg.progress = "3 <<--"
                goal_handle.publish_feedback(feedback_msg)
                # self.result = trigger_device(["c0:da:18:24:ac:20", "Bot", "Press"])  # botがない
                self.result = trigger_device(["D7:39:08:1C:0E:79", "Bot", "Press"])
                if self.result:
                    goal_handle.succeed()
                    feedback_msg.progress = "Success!"
                else:
                    goal_handle.abort()
                    feedback_msg.progress = "Failure..."
            elif self.floor == 4:
                feedback_msg.progress = "4 <<--"
                goal_handle.publish_feedback(feedback_msg)
                # self.result = trigger_device(["c0:da:18:24:ac:20", "Bot", "Press"])
                self.result = trigger_device(["D7:39:08:1C:0E:79", "Bot", "Press"])
                if self.result:
                    goal_handle.succeed()
                    feedback_msg.progress = "Success!"
                else:
                    goal_handle.abort()
                    feedback_msg.progress = "Failure..."

        elif self.request == 2:  # エレベータを呼ぶ：下の階へ行くとき
            if self.floor == 2:
                feedback_msg.progress = "-->> 2"
                goal_handle.publish_feedback(feedback_msg)
                # self.result = trigger_device(["c0:da:18:24:ac:20", "Bot", "Press"])  # botがない
                self.result = trigger_device(["D7:39:08:1C:0E:79", "Bot", "Press"])
                if self.result:
                    goal_handle.succeed()
                    feedback_msg.progress = "Success!"
                else:
                    goal_handle.abort()
                    feedback_msg.progress = "Failure..."
            elif self.floor == 3:
                feedback_msg.progress = "-->> 3"
                goal_handle.publish_feedback(feedback_msg)
                # self.result = trigger_device(["c0:da:18:24:ac:20", "Bot", "Press"])  # botがない
                self.result = trigger_device(["D7:39:08:1C:0E:79", "Bot", "Press"])
                if self.result:
                    goal_handle.succeed()
                    feedback_msg.progress = "Success!"
                else:
                    goal_handle.abort()
                    feedback_msg.progress = "Failure..."
            elif self.floor == 4:
                feedback_msg.progress = "-->> 4"
                goal_handle.publish_feedback(feedback_msg)
                # self.result = trigger_device(["c1:38:32:30:27:85", "Bot", "Press"])
                self.result = trigger_device(["D7:39:08:1C:0E:79", "Bot", "Press"])
                if self.result:
                    goal_handle.succeed()
                    feedback_msg.progress = "Success!"
                else:
                    goal_handle.abort()
                    feedback_msg.progress = "Failure..."
            elif self.floor == 5:
                feedback_msg.progress = "-->> 5"
                goal_handle.publish_feedback(feedback_msg)
                # self.result = trigger_device(["c0:da:18:24:ac:20", "Bot", "Press"])  # botがない
                self.result = trigger_device(["D7:39:08:1C:0E:79", "Bot", "Press"])
                if self.result:
                    goal_handle.succeed()
                    feedback_msg.progress = "Success!"
                else:
                    goal_handle.abort()
                    feedback_msg.progress = "switchbot didn't work"

        elif self.request == 3:  # 扉を開ける
            self.result = trigger_device(["f1:57:59:70:92:3e", "Bot", "Press"])

        elif self.request == 4:  # 扉を閉める
            self.result = trigger_device(["d7:39:08:1c:0e:79", "Bot", "Press"])

        elif self.request == 5:  # エレベータ内の階のボタンを押す
            if self.target_floor == 1:
                self.result = trigger_device(["ca:a2:6c:95:b3:93", "Bot", "Press"])
            elif self.target_floor == 2:
                self.result = trigger_device(["ef:8e:0f:5e:ea:52", "Bot", "Press"])
            elif self.target_floor == 3:
                self.result = trigger_device(["c7:38:32:30:77:6d", "Bot", "Press"])
            elif self.target_floor == 4:
                self.result = trigger_device(["ce:ef:60:f5:a8:da", "Bot", "Press"])
            else:
                self.result = trigger_device(["de:97:4f:e5:f7:6a", "Bot", "Press"])

        # goal_handle.succeed()
        result = Switchbot.Result()  # 結果メッセージの作成
        result.result = feedback_msg.progress

        return result

    # def listener_callback(self, msg):
    #     # self.get_logger().info('I heard: "%s"'% msg.data)
    #     print("Subscribing:", msg.data)
    #     self.msg2elevator_subscriber.data = msg.data

    #     if self.result:
    #         result = 1
    #     else:
    #         result = 0

    #     elevator_state = 0

    #     self.msg2robot = Int32MultiArray()
    #     self.msg2robot.data= [result, elevator_state]

    # self.msg2robot_publisher.publish(self.msg2robot)
    # self.get_logger().info('Publishing: "%s"' % self.msg2robot.data)
    # print("Publishing:", self.msg2robot.data)


def main(args=None):
    rclpy.init(args=args)
    # time.sleep(5.0)
    controller = MAIN()

    rclpy.spin(controller)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    controller.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
