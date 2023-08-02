# cd
# cd IDC/IDC_ws/
# colcon build --symlink-install
# source /opt/ros/humble/setup.bash
# source install/setup.bash

cd
cd IDC
rm -r ros_bag
cd IDC_ws/src/IDC-Simulation/robot_description/config/
id=$(niet "TeamNo" properties.yaml)
cp -r ~/IDC/properties.yaml ~/IDC/IDC_ws/src/IDC-Simulation/robot_description/config/properties.yaml
# ROS_DOMAIN_ID=$id 
cd ../../..
cd IDC_Webserver/
gnome-terminal -x bash -c "ROS_DOMAIN_ID=$id ros2 launch robot_description robot_gazebolaunch.py; exec bash" ;
gnome-terminal -x bash -c "ROS_DOMAIN_ID=$id node client.js; exec bash"
