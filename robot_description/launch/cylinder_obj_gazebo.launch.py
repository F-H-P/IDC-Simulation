import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    pkg_name = 'robot_description'
    file_subpath = 'urdf/obj.xacro'
    xacro_file = os.path.join(get_package_share_directory(pkg_name),file_subpath)
    obj_description_raw = xacro.process_file(xacro_file).toxml()

    spawn_entity_obj = Node(package='gazebo_ros', executable='spawn_entity.py',
                    arguments=['-topic', 'robot_description',
                                '-entity', 'cylinder_obj',],
                    output='screen')
    
    obj_state_publisher = Node(package='robot_state_publisher',
                                  executable='robot_state_publisher',
                                  output='screen',
                                  parameters=[{'robot_description': obj_description_raw,
                                 'use_sim_time': True}]
    )

    return LaunchDescription([
        # spawn_entity_obj,
        obj_state_publisher
    ])