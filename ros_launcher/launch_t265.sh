#! /usr/bin/bash
# launch t265
#cd /root/ros2_ws/
#source install/setup.bash
#/common/scripts/set_path_in_container.sh
HOSTNAME=$(hostname)t265_node # realsenseのlaunch ファイルでは頭に/を付けるとエラー

#$(echo "exec ros2 launch realsense2_camera rs_launch.py pointcloud.enable:=false enable_gyro:=true enable_accel:=true enable_fisheye1:=false enable_fisheye2:=false camera_name:=t265 camera_namespace:=$HOSTNAME __ns:=$HOSTNAME")
# if [[ ! "${TAG}" == image_* ]]; then
#   echo "Build first"
#   bash
# else
$(echo "exec ros2 launch realsense2_camera rs_launch.py pointcloud.enable:=false enable_gyro:=true enable_accel:=true enable_fisheye1:=false enable_fisheye2:=false initial_reset:=true camera_name:=$HOSTNAME camera_namespace:=$HOSTNAME")
# fi
# topic名は　/Drp5_0t265/<topic_name>　のようになる。

# $(echo "exec ros2 run realsense2_camera realsense2_camera_node --ros-args --remap __ns:=$HOSTNAME")
