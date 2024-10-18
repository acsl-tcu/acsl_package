# ros_package

"main" branch shows a template.

"package" is a group of ros2 packages run on a single container.

Each package consists following files

| file name | description |
| ---- | ---- |
|1_ros_launcher|ros launch shell scripts exec in docker container|
||launch_PACKAGE.sh|
|2_ros_packages|ros package build and run in docker container|
||PACKAGE/|
|3_dockerfiles|dockerfile to build a docker image|
||dockerfile.PACKAGE|
|PACKAGE.rules| udev rule|
