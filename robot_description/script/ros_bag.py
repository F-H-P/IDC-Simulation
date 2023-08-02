#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from msg_interfaces.srv import StartRecord, StopRecord
import os
import yaml
import subprocess
from datetime import date
import datetime

# import signal

class RosBag(Node):
    def __init__(self):
        super().__init__('ros_bag')
        self.get_logger().info('RosBag Node start!!')
        self.start_record_server = self.create_service(StartRecord,"/start_record_command",self.start_record_callback)
        self.stop_record_server = self.create_service(StopRecord,"/stop_record_command",self.stop_record_callback)
        self.start_record_req = StartRecord.Request()
        self.stop_record_req = StopRecord.Request()
        # self.timer = self.create_timer(0.1,self.timer_callback)
        # Current PID of recorder
        self.rec_process = None
        self.shutdown = False
        self.ros_domain_id = -1

    def start_record_callback(self,request,response):
        self.start_record_req = request.start_record_command
        # today = date.today()
        domain_id_path = '/home/fhp/IDC/IDC_ws/src/IDC-Simulation/robot_description/config/properties.yaml'
        with open(domain_id_path, 'r') as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)
            self.ros_domain_id = yaml_data['TeamNo']
        os.environ["ROS_DOMAIN_ID"] = str(self.ros_domain_id)

        # filename = today.strftime("%d-%m-%Y-%H-%M-%S")
        dt_now = datetime.datetime.now()
        team_name = yaml_data['Team']
        filename = str(team_name)+" "+str(dt_now)
        record_data = ['ros2', 'bag', 'record', '/score_report', '/state_action', '/pose_obj', '-o', filename]
        self.rec_process = subprocess.Popen(record_data) 
        return response
    
    def stop_record_callback(self,request,response):
        os.environ["ROS_DOMAIN_ID"] = str(self.ros_domain_id)
        self.stop_record_req = request.stop_record_command
        self.get_logger().info('DO THIS!')
        # stop_data = ['bash', 'ros_bag.sh']
        # subprocess.Popen(stop_data)
        # Kill Recorder
        self.rec_process.terminate()
        self.rec_process.wait()
        # self.get_logger().info('Please press "CTRL C" to stop record!!')
        self.get_logger().info('End Process Completed')

        return response
    
    # def timer_callback(self):
    #     if self.shutdown:

    #         # os.killpg(os.getpgid(os.getpid()), signal.SIGINT)
    #         pass
    
def main(args=None):
    rclpy.init(args=args)
    ros_bag = RosBag()
    rclpy.spin(ros_bag)
    ros_bag.destroy_node()
    rclpy.shutdown()
    

if __name__ == '__main__':
    main()