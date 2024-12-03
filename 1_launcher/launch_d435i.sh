#!/bin/sh
source /opt/ros/dashing/setup.bash
source ~/ros2_ws/install/local_setup.bash
HOSTNAME=$(hostname)
#d435i起動コマンド
#ros2 run realsense_ros2_camera realsense_ros2_camera camera_namespace:=/$HOSTNAME
# # Check if /usr/bin/bash exists
# if [ -x "/usr/bin/bash" ]; then
#   exec /usr/bin/bash ros2 run realsense_ros2_camera realsense_ros2_camera camera_namespace:=/$HOSTNAME
# #  exec /usr/bin/bash
# # Check if /bin/bash exists
# elif [ -x "/bin/bash" ]; then
#   exec /bin/bash ros2 run realsense_ros2_camera realsense_ros2_camera camera_namespace:=/$HOSTNAME
# else
#   echo "Bash not found in /usr/bin/bash or /bin/bash"
#   exit 1
# fi
#$(echo "exec ros2 launch realsense2_camera rs_launch.py  enable_gyro:=true camera_name:=d435 camera_namespace:=/$HOSTNAME")
#$(echo "exec ros2 run realsense_ros2_camera realsense_ros2_camera camera_namespace:=/$HOSTNAME")
ros2 launch realsense_ros2_camera ros2_intel_realsense.launch.py camera_name:=d435 camera_namespace:=/$HOSTNAME"
