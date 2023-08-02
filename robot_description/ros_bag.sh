# cd 
# cd IDC
# id=$(niet "TeamNo" properties.yaml)
# ROS_DOMAIN_ID=$id ros2 bag record /score_report -o ros_bag

PID=$!
kill $PID