#! /usr/bin/bash

# vrpn_mocap client launcher
# Details : https://docs.ros.org/en/humble/p/vrpn_mocap/

if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  echo "Usage: dup mocap [SERVER_IP] [PORT]"
  echo ""
  echo "  SERVER_IP  VRPN server IP address (default: 192.168.100.131)"
  echo "  PORT       VRPN server port       (default: 3883)"
  echo ""
  echo "Topics:"
  echo "  /vrpn_mocap/<tracker_name>/pose"
  echo "  /vrpn_mocap/<tracker_name>/twist  (optional)"
  echo "  /vrpn_mocap/<tracker_name>/accel  (optional)"
  exit 0
fi

IP=${1:-192.168.100.131}
PORT=${2:-3883}

$(echo "exec ros2 launch vrpn_mocap client.launch.yaml server:=$IP port:=$PORT")
