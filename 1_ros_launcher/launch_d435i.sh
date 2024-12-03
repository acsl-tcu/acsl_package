#!/bin/sh

# Check if /usr/bin/bash exists
if [ -x "/usr/bin/bash" ]; then
  exec /usr/bin/bash "$@"
# Check if /bin/bash exists
elif [ -x "/bin/bash" ]; then
  exec /bin/bash "$@"
else
  echo "Bash not found in /usr/bin/bash or /bin/bash"
  exit 1
fi

#d435i起動コマンド
HOSTNAME=$(hostname)
$(echo "exec ros2 launch realsense2_camera rs_launch.py  enable_gyro:=true camera_name:=d435 camera_namespace:=/$HOSTNAME")
