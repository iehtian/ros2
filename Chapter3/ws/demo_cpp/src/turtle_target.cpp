#include "rclcpp/rclcpp.hpp"
#include <geometry_msgs/msg/twist.hpp>
#include <rclcpp/publisher.hpp>
#include <rclcpp/timer.hpp>
#include <turtlesim/msg/pose.hpp>
class TUrtleCycleNode : public rclcpp::Node {
private:
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
  rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr subscription_;
  double x_{1.0};
  double y_{1.0};
  double theta_{0.0};
  double k {1.0}; // 线速度增益
   double max_linear_speed {2.0}; // 最大线速度

public:
  explicit TUrtleCycleNode(const std::string &node_name) : Node(node_name) {
    publisher_ = this->create_publisher<geometry_msgs::msg::Twist>(
        "turtle1/cmd_vel", 10);
    subscription_ = this->create_subscription<turtlesim::msg::Pose>(
        "turtle1/pose", 10,std::bind(&TUrtleCycleNode::pose_callback, this, std::placeholders::_1)); // 订阅乌龟的位姿信息，回调函数为pose_callback
  };
  void pose_callback(const turtlesim::msg::Pose::SharedPtr pose) {
      auto current_x = pose->x;
      auto current_y = pose->y;
      auto current_theta = pose->theta;
      RCLCPP_INFO(this->get_logger(), "Current Pose: x=%.2f, y=%.2f, theta=%.2f", current_x, current_y, current_theta);
      // 计算目标点与当前点之间的距离和角度
      double distance = std::sqrt(std::pow(x_ - current_x, 2) + std::pow(y_ - current_y, 2));
      double angle_to_target = std::atan2(y_ - current_y, x_ - current_x);
      double angle_diff = angle_to_target - current_theta;
      // 规范化角度差
      while (angle_diff > M_PI) angle_diff -= 2 * M_PI;
      while (angle_diff < -M_PI) angle_diff += 2 * M_PI;
      // 计算线速度和角速度
      double linear_speed = std::min(k * distance, max_linear_speed); // 线速度与距离成正比，但不超过最大值
      double angular_speed = angle_diff;
      // 发布速度指令
      geometry_msgs::msg::Twist cmd_vel;
      cmd_vel.linear.x = linear_speed;
      cmd_vel.angular.z = angular_speed;
      publisher_->publish(cmd_vel);
  }
};

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  auto node = std::make_shared<TUrtleCycleNode>("turtle_target_node");
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}