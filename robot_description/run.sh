cd
cd IDC/IDC_ws/
source /opt/ros/humble/setup.bash
source install/setup.bash

cd
cd IDC/IDC_ws/src/IDC-Simulation/robot_description/config/
id=$(niet "TeamNo" properties.yaml)
cp -r ~/IDC/properties.yaml ~/IDC/IDC_ws/src/IDC-Simulation/robot_description/config/properties.yaml
ROS_DOMAIN_ID=$id
cd ../../..
cd IDC_Webserver/
gnome-terminal -x bash -c "ROS_DOMAIN_ID=$id ros2 launch robot_description robot_gazebolaunch.py; exec bash" ;
gnome-terminal -x bash -c "ROS_DOMAIN_ID=$id node client.js; exec bash";
cd
cd IDC
ROS_DOMAIN_ID=$id ros2 run robot_description ros_bag.py