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

    def init_obj(self):
        for i in range(15):
            self.obj_data.append(self.Node(0.0,0.0,0.0,"obj"+str(i+1),0))

    class Node:
        def __init__(self, px, py, pz, obj_frame, state):
            self.px = px
            self.py = py
            self.pz = pz
            self.obj_frame = obj_frame
            self.state = state

    def timer_callback(self):
        for j in range(15):
            self.get_position(self.obj_data[j])
            # print("obj",str(j+1),"_px:",self.obj_data[j].px)
            # print("obj",str(j+1),"_py:",self.obj_data[j].py)
            # print("obj",str(j+1),"_pz:",self.obj_data[j].pz) 
            state_changed = self.check_state(self.obj_data[j])
            if state_changed:
                self.score_array.data[j] = self.obj_data[j].state
                print("--------------------------")
                print(self.score_array)
                print("--------------------------")

                self.check_complete()
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
        if obj.px>=-0.725 and obj.px<=0.725 and obj.py>=0.3 and obj.py<=0.4 and obj.pz<=0.25:
            state_now = 1
            # print("Obj is fall!!")
            if state_now != obj.state:
                obj.state = state_now
                print("State is change!")
                result = True
                self.sum_score+=1
            obj.state = 1
        return result
    
    def check_complete(self):
        floor1 = self.score_array.data[0:4]
        floor2 = self.score_array.data[5:9]
        floor3 = self.score_array.data[10:14]
        if all(1 in floor for floor in [floor1, floor2, floor3]):
            self.complete_status = 1

def main(args=None):
    rclpy.init(args=args)
    scoring = Scoring()
    rclpy.spin(scoring)
    scoring.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()