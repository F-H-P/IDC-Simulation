import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch.actions import IncludeLaunchDescription,DeclareLaunchArgument

from launch_ros.actions import Node
import xacro
from launch.substitutions import PathJoinSubstitution,LaunchConfiguration,PythonExpression

from launch_ros.substitutions import FindPackageShare
from launch.actions import IncludeLaunchDescription

from launch.conditions import IfCondition

def generate_launch_description():
    pkg_name = 'robot_description'
    file_subpath = 'urdf/cylinder.xacro'
    xacro_file = os.path.join(get_package_share_directory(pkg_name),file_subpath)
    obj_description_raw = xacro.process_file(xacro_file).toxml()

    spawn_entity_obj = Node(package='gazebo_ros', executable='spawn_entity.py',
                    arguments=['-topic', 'robot_description',
                                '-entity', 'cylinder',],
                    output='screen')
    
    obj_state_publisher = Node(package='robot_state_publisher',
                                  executable='robot_state_publisher',
                                  output='screen',
                                  parameters=[{'robot_description': obj_description_raw,
                                 'use_sim_time': True}]
    )

    velocity_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["forward_velocity_controller", "--controller-manager", "controller_manager"]
    )

    keyboard_controller = Node(
        package="velocity_controller",
        executable="velocity_controller"
    )

    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gzserver.launch.py'
            ])
        ]),
        # condition=IfCondition(use_simulator),
        # launch_arguments={'world': world}.items()
    )    
    gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gzclient.launch.py'
            ])
        ]),
        # condition=IfCondition(PythonExpression([use_simulator, ' and not ', headless]))
    )

    return LaunchDescription([
        # gazebo_server,
        # gazebo_client,
        spawn_entity_obj,
        obj_state_publisher,
        # velocity_controller,
        # keyboard_controller
    ])