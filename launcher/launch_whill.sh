#! /usr/bin/bash
if [[ ! "${TAG}" == image_* ]]; then
  echo "Build first"
  bash
else
  #$(echo "exec ros2 launch acs rplidar_s1_bos_launch.py --log-opt max-size=100m --log-opt max-file=10 --ros-args --remap __node:=rplidar_node --remap __ns:=/$HOSTNAME")
  #  cp -p /common/ros_launcher/launch_rplidar/rplidar_s1_bos_launch.py /root/ros2_ws/src/rplidar_ros/launch/
  $(echo "exec ros2 run whill_driver whill --log-opt max-size=100m --log-opt max-file=10 --ros-args --remap __node:=whill_node --remap __ns:=/$HOSTNAME")
fi
