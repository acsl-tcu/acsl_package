#! /usr/bin/bash
# https://ar-ray.hatenablog.com/entry/2023/09/09/120000
# nmea_navsat_driver
# cp /common/ros_launcher/launch_rtk_gnss/nmea_serial_driver.yaml /root/ros2_ws/install/nmea_navsat_driver/share/nmea_navsat_driver/config/
# $(echo "exec ros2 launch nmea_navsat_driver nmea_serial_driver.launch.py")

# ublox
cp /common/ros_launcher/launch_rtk_gnss/zed_f9p.yaml /root/ros2_ws/src/ublox/ublox_gps/config/
sed -i 's/c94_m8p_rover/zed_f9p/' /root/ros2_ws/src/ublox/ublox_gps/launch/ublox_gps_node-launch.py
$(echo "exec ros2 launch ublox_gps ublox_gps_node-launch.py")
