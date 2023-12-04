import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen
from functools import partial

class TurtlebotController(Node):

    def __init__(self):
        self.previous_x_ = 0
        super().__init__("turtle_controller")
        self.cmd_vel_publisher_ = self.create_publisher(
            msg_type = Twist,
            topic = "turtle1/cmd_vel",
            qos_profile = 10
        )
        self.pose_subscriber = self.create_subscription(
            msg_type=Pose, 
            topic = "turtle1/pose", 
            callback = self.pose_callback,
            qos_profile= 10)
        self.get_logger().info("Turtle Controller has started")

    def pose_callback(self, msg: Pose):
        cmd = Twist()
        if not (2.0 <= msg.x <= 9.0 and 2.0 <= msg.y <= 9.0):
            cmd.linear.x = 1.0
            cmd.angular.z = 0.9
        else:
            cmd.linear.x = 5.0
            cmd.angular.z = 0.0
        self.cmd_vel_publisher_.publish(cmd)

        if msg.x > 5.5 and self.previous_x_ <= 5.5:
            self.previous_x_ = msg.x
            self.get_logger().info("Set color to red")
            self.call_set_pen_service(255, 0, 0 , 3, 0)
        elif msg.x <= 5.5 and self.previous_x_ > 5.5:
            self.previous_x_ = msg.x
            self.get_logger(). info("Set color to green")
            self.call_set_pen_service(0, 255, 0, 3, 0)


    def call_set_pen_service(self, r, g, b, width, off):
        client = self.create_client(srv_type = SetPen, srv_name = "turtle1/set_pen")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("Waiting For Service ...")

        request = SetPen.Request()
        request.r = r
        request.g = g
        request.b = b
        request.width = width
        request.off = off

        future = client.call_async(request=request)
        future.add_done_callback(partial(self.callback_set_pen))

    def callback_set_pen(self, future):
        try:
            response = future.result()
        except Exception as e:
            self.get_logger().error("Server Call Failed: %s" %(e))

def main(args=None):
    rclpy.init(args=args)
    node = TurtlebotController()
    rclpy.spin(node)
    rclpy.shutdown()

