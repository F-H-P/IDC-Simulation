cd
cd IDC/IDC_ws/
colcon build --symlink-install
source /opt/ros/humble/setup.bash
source install/setup.bash

cd src/IDC-Simulation/robot_description/config/
id=$(niet "TeamNo" properties.yaml)
# ROS_DOMAIN_ID=$id ros2 launch robot_description robot_gazebolaunch.py

cd ../../..
cd IDC_Webserver/
gnome-terminal -x sh -c "ROS_DOMAIN_ID=$id ros2 launch robot_description robot_gazebolaunch.py; exec bash" &
gnome-terminal -x sh -c "node client.js; exec bash"