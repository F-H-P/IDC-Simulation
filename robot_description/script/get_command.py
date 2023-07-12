#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from msg_interfaces.srv import CommandGUI
from std_msgs.msg import String

class CommandServer(Node):
    def __init__(self):
        super().__init__('command_server')
        self.get_logger().info('command server start')
        self.timer = self.create_timer(0.1,self.timer_callback)
        self.end_game_server = self.create_service(CommandGUI,"/command_end_game",self.end_game_callback)
        self.end_game_req = String()

    def timer_callback(self):
        pass

    def end_game_callback(self,request,response):
        self.end_game_req = request.command
        response.res.data = 1
        self.get_logger().info('End Game server: get command requset success!!!!')
        return response

def main(args=None):
    rclpy.init(args=args)
    command_server = CommandServer()
    rclpy.spin(command_server)
    command_server.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()