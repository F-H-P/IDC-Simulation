#!/usr/bin/env python3

import os
import rclpy
from rclpy.node import Node
from gazebo_msgs.srv import SpawnEntity
from rcl_interfaces.srv import SetParameters
import ament_index_python
import xacro
from std_msgs.msg import Float64MultiArray,MultiArrayDimension,Empty
import time
from msg_interfaces.srv import SpawnObj
import subprocess

class GameLogic(Node):
    def __init__(self):
        super().__init__('game_logic')
        self.get_logger().info('Game Logic start!!')
        self.timer = self.create_timer(0.1,self.timer_callback)
        self.spawn_server = self.create_service(SpawnObj,"/spawn_command",self.spawn_callback)
        self.spawn_cylin_obj = self.create_client(SpawnEntity, '/spawn_entity')
        # self.timeout_cilent = self.create_client(TimeOut,"/timeout_command")

        self.spawn_req = Empty()
        self.cylin_obj_req = SpawnEntity.Request()
        self.obj_state = SetParameters.Request()
        self.timeout_req = Empty()
        self.stop_command = Float64MultiArray()

        self.do_timer = False
        self.set_time_start = True
        self.stop_move = False

        self.time_start = 0.0
        self.time_now = 0.0
        self.stop_command.data = [0.0,0.0,0.0,0.0,0.0,0.0]
        self.stop_command.layout.dim = [MultiArrayDimension(label='velocity', size=len(self.stop_command.data))]

    def timer_callback(self):
        if self.do_timer == True:
            self.count_time()
        # if self.stop_move == True:
        #     self.stop_moving()
    
    def spawn_callback(self,request,response):
        self.spawn_req = request.spawn_command
        self.get_logger().info('Game logic server: get spawn command request success!!!!')
        self.spawn_obj_req()
        self.do_timer = True
        obj_state_pub_cmd = ['ros2', 'launch', 'robot_description', 'cylinder_obj_gazebo.launch.py']
        subprocess.Popen(obj_state_pub_cmd)
        self.get_logger().info('Run launch success!!!!')
        return response

    def load_xacro(self):
            pkg_name = 'robot_description'
            file_subpath = 'urdf/cylinder_obj.xacro'
            xacro_file = os.path.join(ament_index_python.get_package_share_directory(pkg_name), file_subpath)
            obj_description_raw = xacro.process_file(xacro_file).toxml()
            return obj_description_raw
                
    def spawn_obj_req(self):
        self.cylin_obj_req.name = "cylinder_object"
        self.cylin_obj_req.xml = self.load_xacro()
        self.cylin_obj_req.robot_namespace = ""
        self.cylin_obj_req.reference_frame = "world"
        self.spawn_cylin_obj.call_async(self.cylin_obj_req)

    def count_time(self):
        if self.set_time_start == True:
            print("Start Timmer!!")
            self.time_start = time.time()
            self.set_time_start = False
        else:
            self.time_now = time.time()

        if self.time_now-self.time_start >= 150.0:
            self.do_timer = False
            self.set_time_start = True
            # self.stop_move = True
            self.get_logger().info("Total time:"+str(self.time_now-self.time_start)+" seconds")
            # self.end_game_req()

    # def end_game_req(self):
    #     timeout_req = TimeOut.Request()
    #     timeout_req.time_out_command = Empty()
    #     self.timeout_cilent.call_async(timeout_req)
    #     self.get_logger().info('End game service is requested successfully')
    #     self.get_logger().info('-------------------')

def main(args=None):
    rclpy.init(args=args)
    game_logic = GameLogic()
    rclpy.spin(game_logic)
    game_logic.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()