import rclpy
from rclpy.node import Node
from status_interface.msg import SystemStatus


class StatusPublisher(Node):
    def __init__(self):
        super().__init__("status_publisher")
        self.publisher_ = self.create_publisher(SystemStatus, "status", 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = SystemStatus()
        msg.host_name = "localhost"
        msg.cpu_percent = 50.0
        msg.memory_percent = 60.0
        msg.memory_total = 8192.0
        msg.memory_auailable = 4096.0
        msg.net_sent = 1024.0
        msg.net_recv = 2048.0
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    status_publisher = StatusPublisher()
    rclpy.spin(status_publisher)
    status_publisher.destroy_node()
    rclpy.shutdown()
