#! /usr/bin/bash
# $(echo "exec ros2 run template --remap __ns:=/$HOSTNAME")
# https://github.com/Livox-SDK/livox_ros_driver2
source /opt/ros/${ROS_DISTRO}/setup.bash
case $1 in
"rviz2")
  ros2 launch /common/ros_launcher/launch_livox_lidar/rviz_MID360_launch.py user_config_path:=./launch_livox_lidar/MID360_config.json
  ;;
*)
  ros2 launch livox_ros_driver2 /common/ros_launcher/launch_livox_lidar/msg_MID360_launch.py user_config_path:=./launch_livox_lidar/MID360_config.json
  ;;
esac
