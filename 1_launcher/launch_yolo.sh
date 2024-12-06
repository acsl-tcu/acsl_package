#! /usr/bin/bash
HOSTNAME=$(hostname)
$(echo "exec ros2 run pos --ros-args --remap __ns:=/$HOSTNAME")
