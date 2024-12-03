#! /usr/bin/bash

source /opt/ros/humble/setup.bash
source ./install/setup.bash

camera=$(lsusb | grep 435)
if [[ -z $camera ]]; then
  # launch t265
  HOSTNAME=$(hostname)t265_node # realsenseのlaunch ファイルでは頭に/を付けるとエラー
  $(echo "exec ros2 launch realsense2_camera rs_launch.py pointcloud.enable:=false enable_gyro:=true enable_accel:=true enable_fisheye1:=false enable_fisheye2:=false camera_name:=$HOSTNAME camera_namespace:=$HOSTNAME")
else
  # launch d435 or d435i
  HOSTNAME=$(hostname)d435_node # realsenseのlaunch ファイルでは頭に/を付けるとエラー
  $(echo "exec ros2 launch realsense2_camera rs_launch.py pointcloud.enable:=false enable_gyro:=false enable_accel:=false enable_fisheye1:=false enable_fisheye2:=false initial_reset:=false camera_name:=d435 camera_namespace:=$HOSTNAME")
fi
## if [[ ! "${TAG}" == image_* ]]; then
#   echo "Build first"
#   bash
# else
#$(echo "exec ros2 launch realsense2_camera rs_launch.py pointcloud.enable:=false enable_gyro:=true enable_accel:=true enable_fisheye1:=false enable_fisheye2:=false initial_reset:=true camera_name:=$HOSTNAME camera_namespace:=$HOSTNAME")
# fi
# topic名は　/Drp5_0t265/<topic_name>　のようになる。

#$(echo "exec ros2 run realsense2_camera realsense2_camera_node --ros-args --remap __ns:=$HOSTNAME")
