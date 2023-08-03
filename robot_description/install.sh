Green="\033[32m"
Yellow="\033[33m"
Cyan="\033[36m"
NC="\033[0m"
Green_Bg="\033[42m"
Cyan_Bg="\033[46m"
Bold="\033[1m"
Normal="\033[2m"

while [ true ]
do
echo -e "${Yellow}${Bold}Are you ever installing ROS2 Humble? (Y/N)${Normal}${NC}"
read ROS2installed
if [[($ROS2installed == "Y"||$ROS2installed == "y"||$ROS2installed == "Yes"||$ROS2installed == "YES"||$ROS2installed == "yes")]];
then
echo -e "${Cyan}Updating...${NC}"
sudo apt update
break
elif [[($ROS2installed == "N"||$ROS2installed == "n"||$ROS2installed == "No"||$ROS2installed == "NO"||$ROS2installed == "no")]];
then
echo -e "${Cyan}ROS2 Humble installing...${NC}"
locale

sudo apt update && sudo apt -y install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

locale

sudo apt -y install software-properties-common
sudo add-apt-repository universe

sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update
sudo apt upgrade
sudo apt -y install ros-humble-desktop ros-humble-ros-base ros-dev-tools

source /opt/ros/humble/setup.bash

echo -e "${Green}ROS2 Humble was installed successfully${NC}"
##---------- Press ENTER to continuous ----------##
break
fi
done


echo -e "${Cyan_Bg}Packages installing...${NC}"
##---------- Install Gazebo ----------##
echo -e "${Cyan}Gazebo installing...${NC}"
sudo apt -y install gazebo
echo -e "${Green}Gazebo was installed successfully${NC}"
##---------- Install Controller packages ----------##
echo -e "${Cyan}Controller packages installing...${NC}"
sudo apt -y install ros-humble-controller-manager ros-humble-joint-state-broadcaster ros-humble-ros2-control ros-humble-joint-trajectory-controller ros-humble-velocity-controllers ros-humble-gazebo-plugins ros-humble-gazebo-ros2-control ros-humble-xacro
echo -e "${Green}Controller packages were installed successfully${NC}"
##---------- Install Python package ----------##
echo -e "${Cyan}Python package installing...${NC}"
sudo apt -y install python3.10 python3-pynput python3-pip
pip install -U niet tk
echo -e "${Green}Python package was installed successfully${NC}"


##---------- create Workspace ----------##
echo -e "${Cyan_Bg}Workspace creating...${NC}"
cd
mkdir IDC
cd IDC
mkdir IDC_ws
cd IDC_ws
mkdir src
cd src
git clone https://github.com/F-H-P/IDC-Simulation.git
git clone https://github.com/Fangtnw/IDC_keyboard_control.git
git clone https://github.com/Fangtnw/IDC_Webserver.git
cd ..
colcon build --symlink-install
source install/setup.bash

##---------- Install Webserver packages ----------##
echo -e "${Cyan}Webserver packages installing...${NC}"
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - &&\
sudo apt install -y nodejs
cd src/IDC_Webserver
source /opt/ros/humble/setup.bash
npm init
npm install dotenv express fs nodemon rclnodejs socket.io socket.io-client yaml
npx generate-ros-messages
echo -e "${Green}Webserver packages were installed successfully${NC}"

echo -e "${Green_Bg}Packages was installed successfully${NC}"

# Copy Model's Mesh into Gazebo Default model directory
mkdir -p ~/.gazebo/models/robot_description
cp -r ~/IDC/IDC_ws/src/IDC-Simulation/robot_description/meshes ~/.gazebo/models/robot_description

# Setup yaml path
cd  ~/IDC/IDC_ws/src/IDC_Webserver/
u="$USER"
sed -i "s/User/$u/g" client.js 
cd
cd IDC/IDC_ws/src/IDC_keyboard_control/velocity_controller/velocity_controller
sed -i "s/User/$u/g" velocity_controller.py
cd
cd IDC/IDC_ws/src/IDC-Simulation/robot_description/script
sed -i "s/User/$u/g" ros_bag.py

cp ~/IDC/IDC_ws/src/IDC-Simulation/robot_description/run.sh ~/IDC
# cp ~/IDC/IDC_ws/src/IDC-Simulation/robot_description/free_play.sh ~/IDC
cp -r ~/IDC/IDC_ws/src/IDC-Simulation/robot_description/config/properties.yaml ~/IDC/properties.yaml

echo -e "${Green_Bg}Workspace was created successfully${NC}"
echo -e "${Green}Install success${NC}"