from coverage.files import sep
import rclpy
from rclpy.node import Node
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from queue import Queue
import espeakng
# uv venv --system-site-packages .venv


class NovelPythonNode(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.get_logger().info("NovelPythonNode has been started.")
        self.novelqueue = Queue()
        self.subscription_ = self.create_subscription(
            String, "topic", self.topic_callback, 10
        )
        self.speech_thread_ = self.create_timer(5.0, self.speake_callback)

    def topic_callback(self, msg):
        self.get_logger().info("Novel line has been received: " + msg.data)
        self.novelqueue.put(msg.data)

    def speake_callback(self):
        speaker = espeakng.Speaker()


def main(args=None):
    rclpy.init(args=args)
    node = NovelPythonNode("first_node")
    node.get_logger().info("节点已启动: first_node")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
