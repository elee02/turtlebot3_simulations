import rclpy
from rclpy.node import Node

class TurtlebotController(Node):

    def __init__(self):
        super().__init__("turtle_controller")
        self.get_logger().info("Turtle Controller has started")
        


def main(args=None):
    rclpy.init(args=args)
    rclpy.shutdown()

