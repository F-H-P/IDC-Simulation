# cd
# cd IDC/IDC_ws/
# colcon build --symlink-install
# source /opt/ros/humble/setup.bash
# source install/setup.bash

cd
cd IDC/IDC_ws/src/IDC-Simulation/robot_description/config/
id=$(niet "TeamNo" properties.yaml)
cp -r ~/IDC/properties.yaml ~/IDC/IDC_ws/src/IDC-Simulation/robot_description/config/properties.yaml
# ROS_DOMAIN_ID=$id 
cd ../../..
cd IDC_Webserver/
gnome-terminal -x sh -c "ros2 launch robot_description robot_gazebolaunch.py; exec bash" ;
gnome-terminal -x sh -c "node client.js; exec bash"
