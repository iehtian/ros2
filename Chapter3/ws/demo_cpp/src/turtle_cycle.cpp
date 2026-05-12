#include "rclcpp/rclcpp.hpp"
#include <geometry_msgs/msg/twist.hpp>
#include <rclcpp/publisher.hpp>
#include <rclcpp/timer.hpp>
class TUrtleCycleNode : public rclcpp::Node {
private:
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;

public:
  explicit TUrtleCycleNode(const std::string &node_name) : Node(node_name) {
    publisher_ = this->create_publisher<geometry_msgs::msg::Twist>(
        "turtle1/cmd_vel", 10);
    timer_ = this->create_wall_timer(std::chrono::milliseconds(500), [this]() {
      auto message = geometry_msgs::msg::Twist();
      message.linear.x = 2.0;
      message.angular.z = 1.0;
      publisher_->publish(message);
    });
  }
};

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  auto node = std::make_shared<TUrtleCycleNode>("turtle_cycle_node");
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}