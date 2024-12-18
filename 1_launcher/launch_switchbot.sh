#! /usr/bin/bash
$(echo "exec ros2 run switchbot elevator_node --ros-args --remap __ns:=/$HOSTNAME")
