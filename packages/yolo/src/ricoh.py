import cv2
from ultralytics import YOLO
from custom_msg.msg import StateYolo
import rclpy  # ROS Client Library
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Float64MultiArray
import time


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__("yolo_node")  # node
        self.pub_ = self.create_publisher(StateYolo, "yolo", 2)
        print(self)

    def pub(self, num, name, cls, id, deg, degp, degm, kp):
        msg = StateYolo(
            num=num, name=name, cls=cls, id=id, deg=deg, degp=degp, degm=degm, kp=kp
        )  # msgの型，msgの代入
        # print(msg.data)
        self.pub_.publish(msg)  # msgの送信


def yolo(publisher):
    # カメラを起動する
    cap = cv2.VideoCapture(
        0
    )  # 0はデフォルトのカメラを指定します。複数のカメラがある場合は1, 2, ...と変更できます。

    # カメラが正常にオープンされたか確認する
    if not cap.isOpened():
        print("カメラが正常にオープンできませんでした。")
        exit()

    # model = YOLO('yolo11s.pt')
    # model = YOLO("yolo11n.pt")
    model = YOLO("yolo11n.pt")
    # classes = [62]
    classes = range(0, 80)
    conf = 0.3
    max_det = 3
    results = model(
        source=0,
        conf=conf,
        stream=True,
        save=False,
        classes=classes,
        max_det=max_det,
        half=True,
    )

    time_sta = time.time()  # 時間の計測(リアルタイム用)
    # カメラからのビデオフレームを連続的にキャプチャする
    while True:
        for r in results:
            time_end = time.time()  # 時間の取得
            tim = time_end - time_sta  # 時間の差
            time_sta = time.time()  # 前時刻の保存
            print("dt:{:3.0f}ms".format(tim * 1000), end=" ")

            # 読み込んだフレームを表示する
            # plot = r.plot()
            # cv2.namedWindow('WebCam', cv2.WINDOW_NORMAL)
            # cv2.imshow('WebCam', plot)

            # qを押して停止
            if cv2.waitKey(1) & 0xFF == ord("q"):
                cap.release()
                cv2.destroyAllWindows()
                exit()

            num = r.__len__()
            if num <= 0:
                publisher.pub(0, [""], [0], [0], [0], [0], [0], [0])
                continue

            boxes = r.boxes.cpu().numpy()
            cls = boxes.cls
            id = boxes.id
            if r.boxes.id == None:
                id = [0.0] * num

            name = [""] * num
            # for ii in range(0,num,1):
            #     name[ii] = str(model.names[int(cls[ii])])

            x = boxes.xywhn[:, 0]
            deg = 360 * (-x + 0.5)
            xm = boxes.xyxyn[:, 2]
            degm = 360 * (-xm + 0.5)
            xp = boxes.xyxyn[:, 0]
            degp = 360 * (-xp + 0.5)

            kp = []
            # print(r.keypoints)
            if r.keypoints != None:
                keypoints = r.keypoints.xyn.cpu().numpy()
                for points in keypoints[0]:
                    kp.append(points[0])
                    kp.append(points[1])

            publisher.pub(num, name, cls, id, deg, degp, degm, kp)


def main(args=None):
    rclpy.init(args=args)  # RCLの初期化
    publisher = MinimalPublisher()  # インスタンス化
    yolo(publisher)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
