#! /usr/bin/bash

if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  echo "Usage: dup tb3 <command>"
  echo ""
  echo "Commands:"
  echo "  gazebo        Launch Gazebo simulation"
  echo "  robot         Bring up TurtleBot3 robot"
  echo "  cartographer  Run cartographer SLAM"
  echo "  save_map      Save current map to ~/map"
  exit 0
fi

# https://emanual.robotis.com/docs/en/platform/turtlebot3/slam/#run-slam-node
export TURTLEBOT3_MODEL=burger
#export TURTLEBOT3_MODEL=waffle
#  empty_world.launch.py")
case $1 in
"gazebo")
  $(echo "exec ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py")
  ;;
"robot")
  $(echo "exec ros2 launch turtlebot3_bringup robot.launch.py")
  ;;
"cartographer")
  $(echo "exec ros2 launch turtlebot3_cartographer cartographer.launch.py use_sim_time:=True")
  ;;
"save_map")
  $(echo "exec ros2 run nav2_map_server map_saver_cli -f ~/map")
  ;;
esac
