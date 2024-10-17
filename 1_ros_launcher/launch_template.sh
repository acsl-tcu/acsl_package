#! /usr/bin/bash

# https://emanual.robotis.com/docs/en/platform/turtlebot3/slam/#run-slam-node
export TURTLEBOT3_MODEL=burger
case $1 in
"robot")
  $(echo "exec ros2 launch turtlebot3_bringup robot.launch.py --remap __ns:=/$HOSTNAME")
  ;;
"cartographer")
  $(echo "exec ros2 launch turtlebot3_cartographer cartographer.launch.py --remap __ns:=/$HOSTNAME")
  ;;
esac
