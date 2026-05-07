import rclpy
from rclpy.node import Node


def main(args=None):
    rclpy.init(args=args)
    node = Node("first_node")
    node.get_logger().info("节点已启动: first_node")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
