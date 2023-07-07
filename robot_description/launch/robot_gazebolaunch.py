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
    file_subpath = 'urdf/robot_v2.xacro'
    xacro_file = os.path.join(get_package_share_directory(pkg_name),file_subpath)
    robot_description_raw = xacro.process_file(xacro_file).toxml()
    
    environment = 'urdf/environment.world'
    environment_path = os.path.join(get_package_share_directory(pkg_name),environment)
    os.environ["GAZEBO_MODEL_PATH"] = environment_path

    headless = LaunchConfiguration('headless')
    use_simulator = LaunchConfiguration('use_simulator')
    world = LaunchConfiguration('world')

    declare_simulator_cmd = DeclareLaunchArgument(
        name='headless',
        default_value='False',
        description='Whether to execute gzclient')
        
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true')
    
    declare_use_simulator_cmd = DeclareLaunchArgument(
        name='use_simulator',
        default_value='True',
        description='Whether to start the simulator')

    declare_world_cmd = DeclareLaunchArgument(
        name='world',
        default_value=environment_path,
        description='Full path to the world model file to load'
    )
    
    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gzserver.launch.py'
            ])
        ]),
        condition=IfCondition(use_simulator),
        launch_arguments={'world': world}.items()
    )    
    gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gzclient.launch.py'
            ])
        ]),
        condition=IfCondition(PythonExpression([use_simulator, ' and not ', headless]))
    )

    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                    arguments=['-topic', 'robot_description',
                                '-entity', 'robot',],
                    output='screen')
    
    robot_state_publisher = Node(package='robot_state_publisher',
                                  executable='robot_state_publisher',
                                  output='screen',
                                  parameters=[{'robot_description': robot_description_raw,
                                 'use_sim_time': True}]
    )

    joint_state_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "controller_manager"]
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


    return LaunchDescription([
        declare_simulator_cmd,
        declare_use_sim_time_cmd,
        declare_use_simulator_cmd,
        declare_world_cmd,
        gazebo_server,
        gazebo_client,
        spawn_entity,
        robot_state_publisher,
        joint_state_broadcaster,
        velocity_controller,
        keyboard_controller
    ])