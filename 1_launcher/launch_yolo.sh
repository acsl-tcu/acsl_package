#!/usr/bin/bash
HOSTNAME=$(hostname)
exec ros2 run pos --ros-args --remap __ns:="/$HOSTNAME"
