#! /usr/bin/bash

#if [[ $1 == "save_map" ]]; then
source /opt/ros/${ROS_DISTRO}/setup.bash
case $1 in
"save_map")
  echo "Save map"
  $(echo "exec ros2 run nav2_map_server map_saver_cli -f /common/ros_launcher/launch_slam_toolbox/map")
  ;;
"slam")
  # ros2 run ros_gz_bridge parameter_bridge /cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist
  # ros2 run ros_gz_bridge parameter_bridge /scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan
  # ros2 run ros_gz_bridge parameter_bridge /model/Robot1/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V --ros-args -r /model/Robot1/tf:=/tf
  # ros2 run ros_gz_bridge parameter_bridge /model/Robot1/odometry@nav_msgs/msg/Odometry@gz.msgs.Odometry --ros-args -r /model/Robot1/odometry:=/odom
  ros2 launch slam_toolbox online_async_launch.py slam_params_file:=/common/ros_launcher/launch_slam_toolbox/rf_robot_slam.yaml
  ;;
"matching")
  ros2 launch slam_toolbox localization_launch.py slam_params_file:=/common/ros_launcher/launch_slam_toolbox/rf_robot_localization.yaml
  ;;
"rviz2")
  rviz2 -d /common/ros_launcher/launch_slam_toolbox/slam_toolbox.rviz
  ;;
esac
