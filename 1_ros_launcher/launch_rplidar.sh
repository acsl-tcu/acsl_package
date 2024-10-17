#! /usr/bin/bash

# $1 None or bos
cp -p /common/ros_launcher/launch_rplidar/* /root/ros2_ws/install/rplidar_ros/share/rplidar_ros/launch/
if [ $1 = "None" ]; then
  $(echo "exec ros2 launch rplidar_ros rplidar_s1_launch.py __ns:=/${HOSTNAME}")
else
  $(echo "exec ros2 launch rplidar_ros rplidar_s1_bos_${1}_launch.py __ns:=/${HOSTNAME}")
fi
