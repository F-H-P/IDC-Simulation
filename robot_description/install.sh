Fang frab7
Fang frab7#0193

FANG
 — 
21/07/2023 12:33
ที่เทสจากโค้ดล่าสุด column4นับคะแนนไม่ขึ้นนะ
FANG
 — 
21/07/2023 13:08
แล้วก็ถ้าหมดเวลาแล้ว รบกวนเพิ่มส่ง games status data (array{1}) = 2  มาหน่อยครับ
Fang frab7
 — 
21/07/2023 13:26
โอเคคับ
Fang frab7
 — 
21/07/2023 13:38
เค้า test แล้วคะแนนขึันทั้ง column นะ
ฝั่ง test แล้วคะแนนไม่ขึ้นตลอดเลยหรอ
Fang frab7
 — 
21/07/2023 14:04
แก้เรียบร้อยแล้วนะ pull ของล่าสุดได้เลย
ส่วนเรื่องคะแนนฝั่งลอง test ใหม่ดู เค้ามีแก้วิธี check คะแนนไป คิดว่าน่าจะดีขึ้นนะ
แล้วก็เค้ามีแก้ให้ตู้ไม่ขยับแล้ว ถ้าฝั่งลองเล่นแล้วยังมีขยับอยู่มาบอกได้เลยนะ
FANG
 — 
21/07/2023 14:37
สุดยอดด
ยังไม่แน่ใจเรื่องบัคคะแนนเท่าไร เหมือนจะยังมีบางรอบที่บางobjectคะแนนไม่ขึ้น
15.00 มาลองเทสกัน
Fang frab7
 — 
21/07/2023 14:54
ได้เลย
ต้อง call มั้ย
FANG
 เริ่มการโทรเป็นเวลา 1 ชั่วโมง
 — 
21/07/2023 15:01
FANG
 — 
21/07/2023 15:02
https://db76-125-25-108-5.ngrok-free.app/
FANG
 — 
วันนี้ เวลา 10:39
เราเทส installation script ที่ฟาง pushให้ 3วันก่อนแล้วนะ
ปัญหามีแต่ part ฝั่งเรา 5555
FANG
 — 
วันนี้ เวลา 10:49
1.ตัว velocity controllerของเรา ตอน respawnแขน มันหาไม่เจอ ต้องไปแก้ชื่อไฟล์จาก robot_v2 เป็น robot เฉยๆ เราแก้แล้ว แต่ยังไม่ได้ push เลยจะถามว่า pushได้เนาะ ถามเผื่อฟางแก้อะไรไปแล้ว
2.ตัว node webserver มีแก้เพิ่มนิดนึงเราใส่รายละเอียดไว้ใน notion นะ
Fang frab7
 — 
วันนี้ เวลา 11:19
มันอยู่ใน IDC_keyboard_controller ใช่ป่าว
FANG
 — 
วันนี้ เวลา 11:19
ใช่ๆ
Fang frab7
 — 
วันนี้ เวลา 11:19
push ได้เลยๆ
เค้าไม่มีแก้อะไร
FANG
 — 
วันนี้ เวลา 11:56
ฟางมีไรอัพเดตบ้างอะ
Fang frab7
 — 
วันนี้ เวลา 12:39
ก็ update ว่าปัญหาของ week ที่แล้วแก้ได้แล้ว กับเเก้พวก  simulation, install script แล้วก็ structure ของ folder เวลา install
ประมาณนี้แหละ
FANG
 — 
วันนี้ เวลา 13:05
https://9aa0-101-108-10-100.ngrok-free.app/
Fang frab7
 — 
วันนี้ เวลา 13:25
ฝั่งง
FANG
 เริ่มการโทรเป็นเวลา 1 ชั่วโมง
 — 
วันนี้ เวลา 13:25
FANG
 — 
วันนี้ เวลา 13:30
https://354e-101-108-10-100.ngrok-free.app/
Fang frab7
 — 
วันนี้ เวลา 13:36
const configPath = '/home/User/IDC/IDC_ws/src/IDC-Simulation/robot_description/config/properties.yaml';
Fang frab7
 — 
วันนี้ เวลา 13:56

cd
cd IDC/IDC_ws/
colcon build --symlink-install
source /opt/ros/humble/setup.bash
source install/setup.

ขยาย
run.sh1 KB
Fang frab7
 — 
วันนี้ เวลา 14:11
meeting 25/07/66 : 14.00 น.
แปปนะ
FANG
 — 
วันนี้ เวลา 14:30
push ที
Fang frab7
 — 
วันนี้ เวลา 14:52
ไปกินข้าวมา
ขอโทษๆ
เรียบร้อยคับ
FANG
 — 
วันนี้ เวลา 17:20
ได้แล้วนะ
แก้ run.sh เป็นอันนี้
cd
cd IDC/IDC_ws/
colcon build --symlink-install
source /opt/ros/humble/setup.bash
source install/setup.bash

cd src/IDC_Webserver/
ros2 launch robot_description robot_gazebolaunch.py &
gnome-terminal -- sh -c "node client.js; exec bash"
Fang frab7
 — 
วันนี้ เวลา 18:22
เหมื่อจะต้อง kill gzserver, gzclient ทุกครั้งเลยใช่ป่าว
แล้วเหมือนตัว launch file ของ robot มัน run ค้างหลัง ctrl c ที่ terminal อ่ะ
ของฝั่งเป็นเหมือนกันมั้ย
FANG
 — 
วันนี้ เวลา 18:43
เป็น 5555
เอาใหม่ๆ
cd
cd IDC/IDC_ws/
colcon build --symlink-install
source /opt/ros/humble/setup.bash
source install/setup.bash

cd src/IDC_Webserver/
gnome-terminal -- bash -c "ros2 launch robot_description robot_gazebolaunch.py; exec bash" &

gnome-terminal -- sh -c "node client.js; exec bash"
แต่แลคเหมือนฟางแล้ว พอรันใน vmware
Fang frab7
 — 
วันนี้ เวลา 22:01
มันด้ายย
เก่งเกิ้น
FANG
 — 
วันนี้ เวลา 22:02
ภาพ
FANG
 — 
วันนี้ เวลา 22:43
ลองจนได้แล้วนะ install script อะ หลักๆมีแก้ลำดับคือเอา Webserver ไปลงหลังจาก create workspace (มันมี generate ros message) เลยต้องลงโนดหลังจาก build พวก msgs กับ serviceก่อน

Green="\033[32m"
Yellow="\033[33m"
Cyan="\033[36m"
NC="\033[0m"
Green_Bg="\033[42m"
Cyan_Bg="\033[46m"

ขยาย
install.sh4 KB
FANG
 — 
วันนี้ เวลา 22:55
เดี๋ยวพน.ทำ doc ให้
Fang frab7
 — 
วันนี้ เวลา 22:57
ได้เลยคับ
﻿
FANG
funkfang

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
pip install -U niet 
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
source /opt/ros/humble/setup.bash
cd src/IDC_Webserver
npm init
npm install dotenv express fs nodemon rclnodejs socket.io socket.io-client yaml
npx generate-ros-messages
echo -e "${Green}Webserver packages were installed successfully${NC}"

echo -e "${Green_Bg}Packages was installed successfully${NC}"

# Copy Model's Mesh into Gazebo Default model directory
mkdir -p ~/.gazebo/models/robot_description
cp -r ~/IDC/IDC_ws/src/IDC-Simulation/robot_description/meshes ~/.gazebo/models/robot_description

# Setup yaml path
cd src/IDC_Webserver/
u="$USER"
sed -i "s/User/$u/g" client.js 

cp ~/IDC/IDC_ws/src/IDC-Simulation/robot_description/run.sh ~/IDC

echo -e "${Green_Bg}Workspace was created successfully${NC}"
echo -e "${Green}Install success${NC}"