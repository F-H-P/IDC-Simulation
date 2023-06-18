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
# from launch.actions import ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler
# from launch.event_handlers import OnProcessExit

def generate_launch_description():
    pkg_name = 'robot_description'
    file_subpath = 'urdf/robot.xacro'
    xacro_file = os.path.join(get_package_share_directory(pkg_name),file_subpath)
    robot_description_raw = xacro.process_file(xacro_file).toxml()

    robot_controllers = PathJoinSubstitution(
        [
            FindPackageShare("robot_description"),
            "config",
            "controller.yaml"
        ]
    )

    # gazebo = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource([os.path.join(
    #         get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
    #     )
    
    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gzserver.launch.py'
            ])
        ])
    )    
    gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gzclient.launch.py'
            ])
        ])
    )

    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                    arguments=['-topic', 'robot_description',
                                '-entity', 'robot',],
                    output='screen')
    
    # control_node = Node(
    #     package="controller_manager",
    #     executable="ros2_control_node",
    #     parameters=[{'robot_description': robot_description_raw}, robot_controllers],
    #     output="both",
    # )
    
    robot_state_publisher = Node(package='robot_state_publisher',
                                  executable='robot_state_publisher',
                                  output='screen',
                                  parameters=[{'robot_description': robot_description_raw,
                                 'use_sim_time': True}]
    )

    # joint_state_broadcaster = ExecuteProcess(
    #     cmd=["ros2", "control", "load_controller", "--set-state", "active", "--spin-time", "120",
    #          "joint_state_broadcaster"],
    #     output="screen"
    # )

    # joint_position_controller = ExecuteProcess(
    #     cmd=["ros2", "control", "load_controller", "--set-state", "active",
    #          "forward_position_controller"],
    #     output="screen"
    # )

    # broadcaster = RegisterEventHandler(event_handler=OnProcessExit(
    #                                     target_action=spawn_entity,
    #                                     on_exit=[joint_state_broadcaster],))
    
    # controller = RegisterEventHandler(event_handler=OnProcessExit(
    #                             target_action=spawn_entity,
    #                             on_exit=[joint_position_controller],))
    
    # velo_controller = RegisterEventHandler(event_handler=OnProcessExit(
    #                                         target_action=joint_trajectory_controller,
    #                                         on_exit=[velocity_controller],))
#------------------------------------------------------------------------------------------------
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
        gazebo_server,
        gazebo_client,
        spawn_entity,
        # control_node,
        robot_state_publisher,
        # broadcaster,
        # controller
        # velo_controller
        # joint_state_broadcaster,
        # position_controller
    ])