#!/usr/bin/bash

source /opt/ros/${ROS_DISTRO}/setup.bash

if [[ -f /root/ros2_ws/install/setup.bash ]]; then
  source /root/ros2_ws/install/setup.bash
fi

# ublox RTK-GNSS ノード起動
# デバイスパスとボーレートは環境変数で指定可能
DEVICE=${UBLOX_DEVICE:-/dev/ttyACM0}
BAUDRATE=${UBLOX_BAUDRATE:-115200}

echo "[launch_ublox] device=${DEVICE} baudrate=${BAUDRATE}"

ros2 launch ublox_gps ublox_gps_node-launch.py \
  device:=${DEVICE} \
  baudrate:=${BAUDRATE}
