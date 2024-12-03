import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from custom_msg.msg import StateYolo
import time

class Talker(Node):
    def __init__(self):
        super().__init__('talker')
        self.i = 0
        self.pub = self.create_publisher(String, 'chatter', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        
    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: {0}'.format(self.i)
        self.i += 1
        self.get_logger().info('Publishing: "{0}"'.format(msg.data))
        self.pub.publish(msg)

class Publisher(Node):

    def __init__(self):
        super().__init__('yolo_node')   #node
        self.pub_ = self.create_publisher(StateYolo, 'yolo', 2)
        print(self)

    def pub(self,num,name,cls,id,deg,degp,degm):
        msg = StateYolo(num=num,name=name,cls=cls,id=id,deg=deg,degp=degp,degm=degm) #msgの型，msgの代入
        # print(msg.data)
        self.pub_.publish(msg)#msgの送信

def yolo(publisher):
    time_sta = time.time()#時間の計測(リアルタイム用)
    while True:
        time_end = time.time()  #時間の取得
        tim = time_end- time_sta #時間の差
        # time_sta = time.time() #前時刻の保存
        print("dt:{:3.0f}sec".format(tim))
        num = int(tim)
        name = [""]
        cls = []
        id = []
        deg = []
        degp = []
        degm = []
        publisher.pub(num,name,cls,id,deg,degp,degm)

def main(args=None):
    rclpy.init(args=args)
    try:
        # publisher = Publisher()
        # yolo(publisher)

        talker = Talker()
        rclpy.spin(talker)
        
    finally:
        talker.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
