#! /usr/bin/bash
# $(echo "exec ros2 run template --remap __ns:=/$HOSTNAME")

source /opt/ros/${ROS_DISTRO}/setup.bash
case $1 in
"rviz2")
  rviz2 -d src/ros_packages/unilidar_sdk/unitree_lidar_ros2/src/unitree_lidar_ros2/rviz/view.rviz
  ;;
*)
  ros2 launch unitree_lidar_ros2 launch.py port:=ttyUSB-UNITREE-L1
  ;;
esac
