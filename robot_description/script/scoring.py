#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener 
from std_msgs.msg import Int16MultiArray,Empty
from msg_interfaces.srv import TimeOut

class Scoring(Node):
    def __init__(self):
        super().__init__('scoring')
        self.get_logger().info('Scoring Node start!!')
        self.obj_state_pub = self.create_publisher(Int16MultiArray,"/score_data",10)
        self.score_array = Int16MultiArray()
        self.score_array.data = [0,0,0,0,0,
                                 0,0,0,0,0,
                                 0,0,0,0,0]

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.obj_data = []
        self.init_obj()
        self.timer = self.create_timer(0.1,self.timer_callback)

        self.score_report_pub = self.create_publisher(Int16MultiArray,'/score_report',10)
        self.score_report = Int16MultiArray()
        self.sum_score = 0
        self.complete_status = 0
        self.score_report.data = [self.sum_score,self.complete_status]

        self.timeout_server = self.create_service(TimeOut,"/timeout_command",self.timeout_callback)
        self.timeout_req = TimeOut.Request()

    def init_obj(self):
        for i in range(15):
            self.obj_data.append(self.Node(0.0,0.0,0.0,"obj"+str(i+1),0))
        self.obj_data.append(self.Node(0.0,0.0,0.0,"objL",0))
        self.obj_data.append(self.Node(0.0,0.0,0.0,"objR",0))

    class Node:
        def __init__(self, px, py, pz, obj_frame, state):
            self.px = px
            self.py = py
            self.pz = pz
            self.obj_frame = obj_frame
            self.state = state

    def timer_callback(self):
        for j in range(15):
            # self.get_logger().info('px_'+str(j)+':'+str(self.obj_data[j].px))
            # self.get_logger().info('py_'+str(j)+':'+str(self.obj_data[j].py))
            # self.get_logger().info('pz_'+str(j)+':'+str(self.obj_data[j].pz))

            self.get_position(self.obj_data[j])
            if self.complete_status!=2:
                self.check_charcoal()
                state_changed = self.check_state(self.obj_data[j])
                if state_changed:
                    self.score_array.data[j] = self.obj_data[j].state
                    print("--------------------------")
                    print(self.score_array)
                    print("--------------------------")
                    self.check_complete()
                    self.sum_score = self.check_score()

            self.score_report.data[0] = self.sum_score
            self.score_report.data[1] = self.complete_status
        self.obj_state_pub.publish(self.score_array)
        self.score_report_pub.publish(self.score_report)
    
    def get_position(self,obj):
        toggle = self.listener_post(obj)
        if toggle is True:
            obj.px = self.tf_listener.transform.translation.x
            obj.py = self.tf_listener.transform.translation.y
            obj.pz = self.tf_listener.transform.translation.z

    def listener_post(self,obj):
        child_frame = obj.obj_frame
        try:
            self.tf_listener = self.tf_buffer.lookup_transform('world',child_frame,rclpy.time.Time())
            return True
        except TransformException as ex:
            return False
        
    def check_state(self,obj):
        state_now = 0
        result = False
        if obj.px>=-0.74 and obj.px<=0.74 and obj.py>=0.3 and obj.py<=0.49 and obj.pz>=0.01 and obj.pz<=0.4:
            state_now = 1
            if state_now != obj.state:
                obj.state = state_now
                print("State is change!")
                result = True
                # self.sum_score+=1
            obj.state = 1
        return result
    
    def check_score(self):
        i = 0
        sum_score = 0
        for i in range(15):
            if self.score_array.data[i]==1:
                sum_score+=1
        return sum_score
    
    def check_complete(self):
        floor1 = self.score_array.data[0:5]
        floor2 = self.score_array.data[5:10]
        floor3 = self.score_array.data[10:15]
        if all(1 in floor for floor in [floor1, floor2, floor3]):
            if self.obj_data[15].state == 1 or self.obj_data[16].state == 1:
                self.get_logger().info('Do this')
                self.complete_status = 1

    def check_charcoal(self):
        self.get_position(self.obj_data[15])
        self.get_logger().info('px_L:'+str(self.obj_data[15].px))
        self.get_logger().info('py_L:'+str(self.obj_data[15].py))
        self.get_logger().info('pz_L:'+str(self.obj_data[15].pz))

        self.get_position(self.obj_data[16])
        self.get_logger().info('px_R:'+str(self.obj_data[15].px))
        self.get_logger().info('py_R:'+str(self.obj_data[15].py))
        self.get_logger().info('pz_R:'+str(self.obj_data[15].pz))

        if self.obj_data[15].px>=0.775 and self.obj_data[15].px<=0.925 and self.obj_data[15].py>=-0.15 and self.obj_data[15].py<=0.15 and self.obj_data[15].pz>=0.0 and self.obj_data[15].pz<=0.4:
            self.get_logger().info('Obj_L:'+str(1))
            self.obj_data[15].state = 1
        if self.obj_data[16].px>=-0.925 and self.obj_data[16].px<=-0.775 and self.obj_data[16].py>=-0.15 and self.obj_data[16].py<=0.15 and self.obj_data[16].pz>=0.0 and self.obj_data[16].pz<=0.4:
            self.get_logger().info('Obj_R:'+str(1))
            self.obj_data[16].state = 1


    def timeout_callback(self,request,response):
        self.timeout_req = request.timeout_command
        self.get_logger().info('Get timeout command request success!!!!')
        self.complete_status = 2
        return response


def main(args=None):
    rclpy.init(args=args)
    scoring = Scoring()
    rclpy.spin(scoring)
    scoring.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()