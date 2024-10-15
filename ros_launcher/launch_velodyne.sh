#! /usr/bin/bash

# https://qiita.com/porizou1/items/c815cb17749aad561909
#  $(echo "exec ros2 launch velodyne velodyne-all-nodes-VLP16-launch.py")

# https://qiita.com/miriwo/items/e829f5a78314e0878f1b
case $1 in
"run")
  $(echo "exec ros2 launch velodyne velodyne-all-nodes-VLP16-launch.py  namespace:=/${HOSTNAME}")
  #$(echo -e "ros2 run velodyne_driver velodyne_driver_node --ros-args -p device_ip:='192.168.1.201' -p model:='VLP16' -p rpm:=1200.0\n ros2 launch velodyne_pointcloud velodyne_transform_node-VLP16-launch.py" | xargs -P 2 -I @ bash -c "exec @")
  #  $(echo -e "ros2 run velodyne_driver velodyne_driver_node --ros-args -p device_ip:='192.168.1.201' -p model:='VLP16' -p rpm:=1200.0 --remap __ns:=/${HOSTNAME}\n ros2 launch velodyne_pointcloud velodyne_transform_node-VLP16-launch.py  --remap __ns:=/${HOSTNAME}" | xargs -P 2 -I @ bash -c "exec @")
  #  $(echo "exec ros2 run velodyne_driver velodyne_driver_node --ros-args -p device_ip:='192.168.1.201' -p model:='VLP16' -p rpm:=1200.0")
  ;;
#ROS2のPCL2形式に変換するノードのようです。
"convert")
  #  $(echo "exec ros2 launch velodyne_pointcloud velodyne_transform_node-VLP16-launch.py")
  #$(echo "exec ros2 launch velodyne_pointcloud velodyne_transform_node-VLP16-composed-launch.py namespace:=/${HOSTNAME}")
  $(echo "exec ros2 launch velodyne velodyne-all-nodes-VLP16-launch.py  namespace:=/${HOSTNAME}")
  ;;
"rviz2")
  $(echo "exec rviz2")
  ;;
esac

# frameをvelodyneに設定
# pointclound2を選択して/velodyne_pointsを開く
