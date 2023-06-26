import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch.actions import IncludeLaunchDescription

from launch_ros.actions import Node
import xacro
from launch.substitutions import PathJoinSubstitution

from launch_ros.substitutions import FindPackageShare
from launch.actions import IncludeLaunchDescription

def generate_launch_description():
    pkg_name = 'robot_description'
    file_subpath = 'urdf/spawn_obj.xacro'
    xacro_file = os.path.join(get_package_share_directory(pkg_name),file_subpath)
    obj_description_raw = xacro.process_file(xacro_file).toxml()
    
    # gazebo_server = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource([
    #         PathJoinSubstitution([
    #             FindPackageShare('gazebo_ros'),
    #             'launch',
    #             'gzserver.launch.py'
    #         ])
    #     ])
    # )    
    # gazebo_client = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource([
    #         PathJoinSubstitution([
    #             FindPackageShare('gazebo_ros'),
    #             'launch',
    #             'gzclient.launch.py'
    #         ])
    #     ])
    # )

    spawn_entity_obj = Node(package='gazebo_ros', executable='spawn_entity.py',
                    arguments=['-topic', 'robot_description',
                                '-entity', 'obj',],
                    output='screen')
    
    obj_state_publisher = Node(package='robot_state_publisher',
                                  executable='robot_state_publisher',
                                  output='screen',
                                  parameters=[{'robot_description': obj_description_raw,
                                 'use_sim_time': True}]
    )

    # joint_state_broadcaster = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     arguments=["joint_state_broadcaster", "--controller-manager", "controller_manager"]
    # )

    # position_controller = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     arguments=["forward_position_controller", "--controller-manager", "controller_manager"]
    # )


    return LaunchDescription([
        # gazebo,
        # gazebo_server,
        # gazebo_client,
        spawn_entity_obj,
        # control_node,
        obj_state_publisher,
        # broadcaster,
        # controller
        # velo_controller
        # joint_state_broadcaster,
        # position_controller
    ])