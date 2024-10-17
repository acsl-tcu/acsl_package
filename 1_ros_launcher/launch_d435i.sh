#! /usr/bin/bash

# cd /root/ros2_ws/
#d435i起動コマンド
# if [[ ! "${TAG}" == image_* ]]; then
#   echo "Build first"
#   bash
# else
HOSTNAME=$(hostname)
$(echo "exec ros2 launch realsense2_camera rs_launch.py  enable_gyro:=true camera_name:=d435 camera_namespace:=/$HOSTNAME")
# fi
