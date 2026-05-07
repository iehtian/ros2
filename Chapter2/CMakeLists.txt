cmake_minimum_required(VERSION 3.8)
set(CMAKE_C_COMPILER "clang")
set(CMAKE_CXX_COMPILER "clang++")
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_BUILD_TYPE Debug)
project(first_package)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic -g)
endif()

find_package(rclcpp REQUIRED)

add_executable(first_node firstnode.cpp)
ament_target_dependencies(first_node rclcpp)

install(TARGETS first_node
  DESTINATION lib/${PROJECT_NAME})
