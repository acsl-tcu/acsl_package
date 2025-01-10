#! /usr/bin/bash
$(echo "exec ros2 launch slam_toolbox online_async_launch.py --remap __ns:=/$HOSTNAME")
