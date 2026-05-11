#! /usr/bin/bash
# $(echo "exec ros2 run template --remap __ns:=/$HOSTNAME")
# https://github.com/Livox-SDK/livox_ros_driver2
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  echo "Usage: dup livox_lidar [command]"
  echo ""
  echo "Commands:"
  echo "  (none)   Launch Livox MID360 driver"
  echo "  rviz2    Open rviz2 viewer"
  exit 0
fi

source /opt/ros/${ROS_DISTRO}/setup.bash
if [ -d /root/ros2_ws/src/ws_livox ]; then
  case $1 in
  "rviz2")
    ros2 launch /common/ros_launcher/launch_livox_lidar/rviz_MID360_launch.py user_config_path:=./launch_livox_lidar/MID360_config.json
    ;;
  *)
    ros2 launch livox_ros_driver2 /common/ros_launcher/launch_livox_lidar/msg_MID360_launch.py user_config_path:=./launch_livox_lidar/MID360_config.json
    ;;
  esac
else

  chmod a+x ./setup_livox.sh
  ./setup_livox.sh
fi
