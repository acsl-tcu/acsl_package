#! /usr/bin/bash
flag=$(cat /boot/firmware/config.txt | grep imx519)
if [[ -z $flag ]]; then
  sudo echo "camera_auto_detect=0" >>/boot/firmware/config.txt
  sudo echo "dtoverlay=imx519,cam0" >>/boot/firmware/config.txt
fi
wget -O install_pivariety_pkgs.sh https://github.com/ArduCAM/Arducam-Pivariety-V4L2-Driver/releases/download/install_script/install_pivariety_pkgs.sh
chmod +x install_pivariety_pkgs.sh
./install_pivariety_pkgs.sh -p libcamera_dev
./install_pivariety_pkgs.sh -p libcamera_apps

cp -p ~/.ssh/id_* $ACSL_WORK_DIR/1_launcher
cd ~/.ssh
cat id_rsa >>authorized_keys

cat "#! /usr/bin/bash" >>$ACSL_WORK_DIR/1_launcher/launch_set_ssh_key.sh

cat "cp -p /common/ros_launcher/id_* /root/.ssh/" >>$ACSL_WORK_DIR/1_launcher/launch_set_ssh_key.sh

cd $ACSL_ROS2_DIR/4_docker
ROS_LAUNCH=set_ssh_key docker compose up
