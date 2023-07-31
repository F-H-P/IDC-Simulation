#!/usr/bin/env python3

import os
import rclpy
from rclpy.node import Node
from gazebo_msgs.srv import SpawnEntity,DeleteEntity
from rcl_interfaces.srv import SetParameters
import ament_index_python
import xacro
from std_msgs.msg import Float64MultiArray,MultiArrayDimension,Empty,Int16MultiArray
import time
from msg_interfaces.srv import SpawnObj,TimeOut,FreePlay,Reset,Start
import subprocess
import tkinter 
import threading

class GameLogic(Node):
    def __init__(self):
        super().__init__('game_logic')
        self.get_logger().info('Game Logic start!!')
       
        self.timer = self.create_timer(0.1,self.timer_callback)
        self.free_play_server = self.create_service(FreePlay,"/free_play_command",self.free_play_callback)
        self.reset_server = self.create_service(Reset,"/reset_command",self.reset_callback)
        self.start_server = self.create_service(Start,"/start_command",self.start_callback)
        self.spawn_server = self.create_service(SpawnObj,"/spawn_command",self.spawn_callback)
        self.spawn_client = self.create_client(SpawnEntity, '/spawn_entity')
        self.spawn_robot_client = self.create_client(SpawnEntity, '/spawn_entity')
        self.delete_client = self.create_client(DeleteEntity,'/delete_entity')
        self.timeout_cilent = self.create_client(TimeOut,"/timeout_command")        

        self.free_play_req = Empty()
        self.reset_req = Empty()
        self.spawn_all = SpawnEntity.Request()
        self.spawn_robot = SpawnEntity.Request()
        self.delete_all = DeleteEntity.Request()
        self.start_req = Empty()
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

    def load_xacro(self,file_path):
            pkg_name = 'robot_description'
            file_subpath = file_path
            xacro_file = os.path.join(ament_index_python.get_package_share_directory(pkg_name), file_subpath)
            obj_description_raw = xacro.process_file(xacro_file).toxml()
            return obj_description_raw

    def spawn_setting(self,request,name,file_path):
        request.name = name
        request.xml = self.load_xacro(file_path)
        request.robot_namespace = ""
        request.reference_frame = "world"

    def delete_entity(self,request,name):
        request.name = name

    def free_play_callback(self,request,response):
        self.free_play_req = request.free_play_command
        self.get_logger().info('get free play command request success!!!!')
        self.spawn_setting(self.spawn_all,"cylinder",'urdf/cylinder.xacro')
        self.spawn_client.call_async(self.spawn_all)
        self.get_logger().info('Spawn all success!!!!')
        obj_state_pub_cmd = ['ros2', 'launch', 'robot_description', 'cylinder.launch.py']
        subprocess.Popen(obj_state_pub_cmd)
        self.get_logger().info('Run launch success!!!!')
        return response
    
    def reset_callback(self,request,response):
        self.reset_req = request.reset_command
        self.get_logger().info('get reset command request success!!!!')
        self.delete_entity(self.delete_all,"cylinder")
        self.delete_client.call_async(self.delete_all)
        self.delete_entity(self.delete_all,"robot")
        self.delete_client.call_async(self.delete_all)
        self.get_logger().info('Delete all success!!!!')

        time.sleep(1.5)

        self.spawn_setting(self.spawn_robot,"charcoal",'urdf/charcoal.xacro')
        self.spawn_robot_client.call_async(self.spawn_robot)
        obj_state_pub_cmd = ['ros2', 'launch', 'robot_description', 'charcoal.launch.py']
        subprocess.Popen(obj_state_pub_cmd)
        self.get_logger().info('Run launch success!!!!')

        self.spawn_setting(self.spawn_robot,"robot",'urdf/robot.xacro')
        self.spawn_robot_client.call_async(self.spawn_robot)
        try:
            controller_cmd = ['ros2', 'run', 'controller_manager', 'spawner', 'forward_velocity_controller']
            subprocess.run(controller_cmd, check=True)
        except Exception as e:
            self.get_logger().error(f'Error spawning controller: {str(e)}')

        self.get_logger().info('Spawn all success!!!!')
        return response
    
    def start_callback(self,request,response):
        self.start_req = request.start_command
        self.get_logger().info('get start command request success!!!!')
        self.do_timer = True
        overlay_thread = threading.Thread(target=self.overlay_display)
        overlay_thread.start()
        # self.overlay_display
        return response
    
    def spawn_callback(self,request,response):
        self.spawn_req = request.spawn_command
        self.get_logger().info('Game logic server: get spawn command request success!!!!')
        self.spawn_setting(self.cylin_obj_req,"cylinder_obj",'urdf/obj.xacro')
        self.spawn_robot_client.call_async(self.cylin_obj_req)
        # self.spawn_obj_req()
        obj_state_pub_cmd = ['ros2', 'launch', 'robot_description', 'cylinder_obj_gazebo.launch.py']
        subprocess.Popen(obj_state_pub_cmd)
        self.get_logger().info('Run launch success!!!!')
        return response

    def overlay_display(self):
        self.overlay = tkinter.Tk()
        # self.overlay.wait_visibility(self.overlay)
        self.overlay.overrideredirect(True)
        self.overlay.geometry("+1500+50")
        self.overlay.lift()
        self.overlay.wm_attributes("-topmost", True)
        # self.overlay.wm_attributes("-alpha", "-0.3")
        self.overlay.config(bg="black")
        self.score_label = tkinter.Label(self.overlay, text='Score : 0', font=('Arial Bold', '40'), fg='yellow', bg='black')
        self.score_label.pack()
        self.timer_label = tkinter.Label(self.overlay, text='Time : 0', font=('Arial Bold', '40'), fg='yellow', bg='black')
        self.timer_label.pack()
        self.score_sub = self.create_subscription(Int16MultiArray, '/score_report',self.update_overlay, 10)
        # self.update_overlay()
        self.overlay.mainloop()
        
    def update_overlay(self,score_data):
        elapsed_time = int(time.time() - self.time_start)
        self.countdown = max(0, 180 - elapsed_time)
        self.timer_label["text"] = f"Timer : {self.countdown}"  

        score_value = str(score_data.data[0])
        self.score_label["text"] = f"Score : {score_value}"
        self.score_label.after(1000, self.update_overlay)

    def count_time(self):
        if self.set_time_start == True:
            self.get_logger().info("Start Timer!!")
            self.time_start = time.time()
            self.set_time_start = False
        else:
            self.time_now = time.time()

        if self.time_now-self.time_start >= 180.0:
            self.do_timer = False
            self.set_time_start = True
            self.get_logger().info("Total time:"+str(self.time_now-self.time_start)+" seconds")
            self.end_game_req()

    def end_game_req(self):
        timeout_req = TimeOut.Request()
        timeout_req.timeout_command = Empty()
        self.timeout_cilent.call_async(timeout_req)
        self.overlay.destroy()
        self.get_logger().info('End game service is requested successfully')
        self.get_logger().info('-------------------')

def main(args=None):
    rclpy.init(args=args)
    game_logic = GameLogic()
    rclpy.spin(game_logic)
    game_logic.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()