import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

class TurtlebotController(Node):

    def __init__(self):
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

    def 
def main(args=None):
    rclpy.init(args=args)
    node = TurtlebotController()
    rclpy.spin(node)
    rclpy.shutdown()

