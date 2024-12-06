#!/usr/bin/bash
HOSTNAME=$(hostname)
exec ros2 run yolo pos --ros-args --remap __ns:="/$HOSTNAME"
