cd
cd IDC
rm -r ros_bag

cp -r ~/IDC/properties.yaml ~/IDC/IDC_ws/src/IDC-Simulation/robot_description/config/properties.yaml
gnome-terminal -x bash -c "ros2 launch robot_description robot_gazebolaunch.py" ;
gnome-terminal -x bash -c "sleep 2";
ros2 service call /free_play_command msg_interfaces/srv/FreePlay "free_play_command: {}"
gnome-terminal -x bash -c "sleep 10";
ros2 service call /free_play_command msg_interfaces/srv/FreePlay "free_play_command: {}"