#! /usr/bin/bash

# cd /root/ros2_ws/
#micro-ros agent 起動コマンド
if [[ ! "${TAG}" == image_* ]]; then
  echo "Build first"
  bash
else
  echo "Confirm server IP and port"
  IP=192.168.100.131
  PORT=
  $(echo "exec ros2 launch vrpn_mocap client.launch.yaml server:=$IP port:=$PORT --ros-args --remap __node:=microros_node --remap __ns:=/$HOSTNAME")
fi
# Details : https://index.ros.org/r/vrpn_mocap/
#/vrpn_mocap/<tracker_name>/pose
#/vrpn_mocap/<tracker_name>/twist # optional when mocap reports velocity data
#/vrpn_mocap/<tracker_name>/accel # optional when mocap reports acceleration data
