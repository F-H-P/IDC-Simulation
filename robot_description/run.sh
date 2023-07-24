cd
cd IDC/IDC_ws/
colcon build --symlink-install
source /opt/ros/humble/setup.bash
source install/setup.

cd src/IDC_Webserver/
ros2 launch robot_description robot_gazebolaunch.py;
node client.js
# terminal -e node client.js