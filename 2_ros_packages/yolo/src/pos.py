# 必要なライブラリのインポート
import cv2
from ultralytics import YOLO
from custom_msg.msg import StateYolo # カスタムメッセージの定義
import rclpy    #ROS Client Library
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Float64MultiArray
import time
import math

class MinimalPublisher(Node):
    # ROS2を定義しているクラス
    def __init__(self):
        super().__init__('yolo_node')   #node
        self.pub_ = self.create_publisher(StateYolo, 'yolo', 2)
        print(self)

    def pub(self,num,name,cls,id,deg,degp,degm,kp):
        msg = StateYolo(num=num,name=name,cls=cls,id=id,deg=deg,degp=degp,degm=degm,kp=kp) #msgの型，msgの代入
        # print(msg.data)
        self.pub_.publish(msg)#msgの送信

def yolo(publisher):
    # 歩行者の認識，角度推定，推定値のPublishを行う

    # カメラを起動する
    cap = cv2.VideoCapture(0)  # 0はデフォルトのカメラを指定します。複数のカメラがある場合は1, 2, ...と変更できます。

    # カメラが正常にオープンされたか確認する
    if not cap.isOpened():
        print("カメラが正常にオープンできませんでした。")
        exit()
   
    # 学習モデルの定義
    model = YOLO('yolov11x-pose.pt') # poseモデル，xは最も重くて正確
    # model = YOLO('yolov11s-pose.pt') # sは軽くて不正確，詳細は公式ページのモデル詳細

    conf=0.3 # 検出確率の閾値
    max_det=5 # 最大検出数
    # 以下の詳細やその他プロパティは公式サイト参照：[https://docs.ultralytics.com/ja/modes/predict/#image-and-video-formats]
    # source：推定を実行するファイル，0なら接続しているカメラのリアルタイムフレームになる
    # stream：すべてのフレームをメモリにロードする代わりに結果のジェネレーターを作成，ビデオやライブストリームを処理するのに有益
    # half：半精度(FP16)推論が可能になりサポートされているGPUでのモデル推論を精度への影響を最小限に抑えながら高速化することができる
    results = model(source=0,conf=conf,stream=True,max_det=max_det,half=True) # YOLOの実行結果をresultsに格納

    # trackモードで推論：追跡IDがつけられる，歩行者の判別が今後必要になったらこっちの方が有用かも
    # persist：現在の画像またはフレームがシーケンスの次であり現在の画像に前の画像からのトラックを期待することをトラッカーに伝える
    # 参考サイト：[https://docs.ultralytics.com/ja/modes/track/#why-choose-ultralytics-yolo-for-object-tracking]
    # tracker = 'botsort.yaml' # 'botsort.yaml' or 'bytetrack.yaml'のどちらか，botsortが新しい方
    # results = model.track(source=0,conf=conf,stream=True,max_det=max_det,half=True,persist=True,tracker=tracker)

    time_sta = time.time()#時間の計測の初期定義
    # カメラからのビデオフレームを連続的にキャプチャする
    while True:
        for r in results:
            time_end = time.time()  # 時間の取得
            tim = time_end- time_sta # 刻み時間の算出
            time_sta = time.time() # 現時刻の保存
            print("dt:{:3.0f}ms".format(tim*1000),end=' ') # プログラムの周期を表示

            # 読み込んだフレームを表示する，基本的にコメントアウトした状態で使用，確認したいときに解除
            # plot = r.plot()
            # cv2.namedWindow('WebCam', cv2.WINDOW_NORMAL)
            # cv2.imshow('WebCam', plot)
            # qを押して停止
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     cap.release()
            #     cv2.destroyAllWindows()
            #     exit()
            
            num = r.__len__() # 検出物体の数を取得
            if num <= 0: # 検出数が0以下なら
                publisher.pub(0,[""],[0],[0],[0],[0],[0],[]) # 検出数0としてPub
                continue # 以下のプログラムを飛ばしてwhwileの最初に戻る

            xm = [] # 変数を配列とした初期定義
            xp = []
            x = []
            deg = [0.0]*num # 初期定義，検出数分用意
            degm = [0.0]*num
            degp = [0.0]*num
            keypoints = r.keypoints.xyn.cpu().numpy() # poseモデル限定，各関節の座標を取得，扱いやすい方に変換
            for ii in range(num): # 検出数分回す
                d1 = keypoints[ii][5] # 5と6が両肩の座標を示す
                d2 = keypoints[ii][6]

                # poseモデルでは体の前後も考慮するため，カメラに対する体の向きで座標の大きい方が変わる
                # xpが座標値が大きい方，xmが小さい方
                if d1[0] < d2[0]:
                    xp.extend(d1)
                    xm.extend(d2)
                    
                else:
                    xp.extend(d2)
                    xm.extend(d1)
            
            # 各ピクセル座標を角度に変換
            for ii in range(num):
                degm[ii] = 2*math.pi*(-xm[2*ii]+0.5)
                degp[ii] = 2*math.pi*(-xp[2*ii]+0.5)
                deg[ii] = (degm[ii] + degp[ii])/2 # 中心座標は上記の間をとる
                
            # BBoxの両端の座標を角度として定義するt機
            # x = boxes.xywhn[:,0]
            # deg = 2*math.pi*(-x+0.5)
            # xm = boxes.xyxyn[:,2]
            # degm = 2*math.pi*(-xm+0.5)
            # xp = boxes.xyxyn[:,0]
            # degp = 2*math.pi*(-xp+0.5)

            kp = []
            # 各関節の座標をすべて取得するときに以下をコメントアウト，現状は一人のみに対応
            # if r.keypoints != None:
            #     keypoints = r.keypoints.xyn.cpu().numpy()
            #     for points in keypoints[0]: # [0]は最初に検出された人を指している，アルゴリズム上実装できていないだけ
            #         kp.append(points[0])
            #         kp.append(points[1])
            
            publisher.pub(num,[""],[0],[0],deg,degp,degm,kp) # 各値のpublish


def main(args=None):
    rclpy.init(args=args)#RCLの初期化
    publisher = MinimalPublisher()  #インスタンス化
    yolo(publisher)
    rclpy.shutdown()

if __name__ == '__main__':
    main()