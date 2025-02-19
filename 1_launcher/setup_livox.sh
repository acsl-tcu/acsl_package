#! /usr/bin/bash
# https://github.com/Livox-SDK/livox_ros_driver2
# https://github.com/Livox-SDK/Livox-SDK2/blob/master/README.md
if [ ${HOSTNAME:0:1} == "D" ]; then
  # docker container 内での使用を想定
  cd ./src/ros_packages/Livox-SDK2/
  mkdir build
  cd build
  cmake .. && make -j
  make install

  cd ../../..
  ln -s ./ros_packages/ws_livox .
  cd ./ws_livox/src/libox_ros_driver2/
  ./build.sh humble
fi
