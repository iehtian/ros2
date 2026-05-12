import math
import rclpy
from rclpy.node import Node
from queue import Queue
import geometry_msgs.msg
import turtlesim.msg


class NovelPythonNode(Node):
    target_x = 5.0
    target_y = 5.0
    max_speed = 3.0
    def __init__(self, node_name):
        super().__init__(node_name)
        self.get_logger().info("NovelPythonNode has been started.")
        self.novelqueue = Queue()
        self.subscription_ = self.create_subscription(
            turtlesim.msg.Pose, "turtle1/pose", self.callback, 10
        )
        self.publisher_ = self.create_publisher(
            geometry_msgs.msg.Twist, "turtle1/cmd_vel", 10
        )

    def callback(self, msg):
        current_x = msg.x
        current_y = msg.y
        self.get_logger().info(f"Current position: ({current_x}, {current_y})")
        error_x = self.target_x - current_x
        error_y = self.target_y - current_y
        distance = (error_x**2 + error_y**2) ** 0.5
        # 计算角度和线速度
        angle = math.atan2(error_y, error_x)
        angle_error = angle - msg.theta
        if distance > 0.1:
            speed = min(self.max_speed, distance)
            twist_msg = geometry_msgs.msg.Twist()
            twist_msg.linear.x = speed * (error_x / distance)
            twist_msg.linear.y = speed * (error_y / distance)
            twist_msg.angular.z = angle_error
            self.publisher_.publish(twist_msg)


def main(args=None):
    rclpy.init(args=args)
    node = NovelPythonNode("first_node")
    node.get_logger().info("节点已启动: first_node")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
