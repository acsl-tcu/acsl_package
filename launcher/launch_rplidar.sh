#! /usr/bin/bash

# $1 None or bos
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  echo "Usage: dup rplidar <mode>"
  echo ""
  echo "Modes:"
  echo "  None     Launch rplidar S1 (standalone)"
  echo "  front    Launch rplidar S1 for BOS (front)"
  echo "  behind   Launch rplidar S1 for BOS (behind)"
  exit 0
fi

cp -p /common/ros_launcher/launch_rplidar/* /root/ros2_ws/install/rplidar_ros/share/rplidar_ros/launch/
if [ $1 = "None" ]; then
  $(echo "exec ros2 launch rplidar_ros rplidar_s1_launch.py __ns:=/${HOSTNAME}")
else
  $(echo "exec ros2 launch rplidar_ros rplidar_s1_bos_${1}_launch.py __ns:=/${HOSTNAME}")
fi
