#include "rclcpp/rclcpp.hpp"
#include "status_interface/msg/system_status.hpp"
#include <rclcpp/publisher_base.hpp>

class StatusNode : public rclcpp::Node {
private:
  rclcpp::Publisher<status_interface::msg::SystemStatus>::SharedPtr publisher_;

public:
  explicit StatusNode(const std::string &node_name) : Node(node_name) {
    RCLCPP_INFO(this->get_logger(), "StatusNode has been started.");
    publisher_ = this->create_publisher<status_interface::msg::SystemStatus>(
        "system_status", 10);
    auto timer_callback = std::bind(&StatusNode::call_back, this);
    auto timer = this->create_wall_timer(std::chrono::seconds(1), timer_callback);
  }
  void call_back() {
    auto msg = status_interface::msg::SystemStatus();
    msg.host_name = "localhost";
    msg.cpu_percent = 50.0;
    msg.memory_percent = 60.0;
    msg.memory_total = 8192.0;
    msg.memory_auailable = 4096.0;
    msg.net_sent = 1024.0;
    msg.net_recv = 2048.0;
    publisher_->publish(msg);
  }
};

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  auto node = std::make_shared<StatusNode>("status_node");
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}