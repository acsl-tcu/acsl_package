#! /usr/bin/bash
# $(echo "exec ros2 run template --remap __ns:=/$HOSTNAME")

if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  echo "Usage: dup unitree_lidar [command]"
  echo ""
  echo "Commands:"
  echo "  (none)   Launch Unitree L1 LiDAR driver"
  echo "  rviz2    Open rviz2 viewer"
  exit 0
fi

source /opt/ros/${ROS_DISTRO}/setup.bash
case $1 in
"rviz2")
  rviz2 -d src/ros_packages/unilidar_sdk/unitree_lidar_ros2/src/unitree_lidar_ros2/rviz/view.rviz
  ;;
*)
  ros2 launch unitree_lidar_ros2 launch.py port:=ttyUSB-UNITREE-L1
  ;;
esac
