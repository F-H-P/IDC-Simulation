#!/usr/bin/env python3

import os
import rclpy
from rclpy.node import Node
from gazebo_msgs.srv import SpawnEntity
import ament_index_python
import xacro
from std_msgs.msg import String,Float64MultiArray,MultiArrayDimension
import time
# from msg_interface.srv import Spawn
# from msg_interface.srv import EndGame
from msg_interfaces.srv import CommandGUI
from msg_interface.srv import Spawn

class GameLogic(Node):
    def __init__(self):
        super().__init__('game_logic')
        self.get_logger().info('Game Logic start!!')
        self.timer = self.create_timer(0.1,self.timer_callback)
        self.spawn_server = self.create_service(CommandGUI,"/command_spawn",self.spawn_callback)
        self.spawn_cylin_obj = self.create_client(SpawnEntity, '/spawn_entity')
        self.end_game_cilent = self.create_client(CommandGUI,"/command_end_game")
        self.velocity_publisher = self.create_publisher(Float64MultiArray, '/forward_velocity_controller/commands',10)

        self.spawn_req = String()
        self.cylin_obj_req = SpawnEntity.Request()
        self.end_game_command_req = String()
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
        if self.stop_move == True:
            self.stop_moving()
    
    def spawn_callback(self,request,response):
        self.spawn_req = request.command
        response.res.data = 1
        self.get_logger().info('Game logic server: get spawn command request success!!!!')
        self.spawn_obj_req()
        self.do_timer = True
        return response

    def load_xacro(self):
            pkg_name = 'robot_description'
            file_subpath = 'urdf/spawn_obj.xacro'
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

        if self.time_now-self.time_start >= 5.0:
            self.do_timer = False
            self.set_time_start = True
            self.stop_move = True
            print("Total time:",self.time_now-self.time_start," seconds")
            self.end_game_req()

    def end_game_req(self):
        self.end_game_command_req.data = "End"
        # self.end_game_cilent.call_async(self.end_game_command_req)
        # future_endgame = self.end_game_cilent.call_async(self.end_game_command_req)
        # rclpy.spin_until_future_complete(self,future_endgame)
        # self.get_logger().info('End game service is requested successfully')
        self.get_logger().info('-------------------')

    def stop_moving(self):
        self.velocity_publisher.publish(self.stop_command)
        print("DO STOP COMMAND!")

def main(args=None):
    rclpy.init(args=args)
    game_logic = GameLogic()
    rclpy.spin(game_logic)
    game_logic.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()