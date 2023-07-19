#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import xacro
from std_msgs.msg import Float64MultiArray,MultiArrayDimension,Empty
import subprocess

class ObjStatePub(Node):
    