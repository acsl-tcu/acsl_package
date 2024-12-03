import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from custom_msg.msg import StateYolo

class Listener(Node):
    def __init__(self):
        # super().__init__('listener')
        # self.sub = self.create_subscription(String, 'chatter', self.chatter_callback, 2)

        super().__init__('listener')
        self.sub = self.create_subscription(StateYolo, 'yolo', self.chatter_callback, 2)

    def chatter_callback(self, msg):
        # self.get_logger().info('I heard: "%s"' % msg.data)
        print(msg.num)

def main(args=None):
    rclpy.init(args=args)
    try:
        listener = Listener()
        rclpy.spin(listener)
    finally:
        listener.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
