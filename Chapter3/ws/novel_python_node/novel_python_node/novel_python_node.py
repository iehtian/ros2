import requests
from queue import Queue
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String


class NovelPythonNode(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.get_logger().info("NovelPythonNode has been started.")
        self.novelqueue = Queue()
        self.publisher_ = self.create_publisher(String, "topic", 10)
        self.create_timer(5.0, self.timer_callback)

    def timer_callback(self):
        if self.novelqueue.empty():
            self.get_logger().info("Novel queue is empty.")
        else:
            line = self.novelqueue.get()
            msg = String()
            msg.data = line
            self.publisher_.publish(msg)
            self.get_logger().info("Novel line has been published: " + line)

    def download_novel(self, url):
        response = requests.get(url)
        response.encoding = "utf-8"
        text = response.text
        lines = text.splitlines()
        for line in lines:
            self.novelqueue.put(line)
        self.get_logger().info("Novel has been downloaded and added to the queue.")


def main(args=None):
    rclpy.init(args=args)
    novel_node = NovelPythonNode("novel_python_node")
    novel_node.download_novel("http://localhost:8000/novel.txt")
    rclpy.spin(novel_node)
    novel_node.destroy_node()
    rclpy.shutdown()
