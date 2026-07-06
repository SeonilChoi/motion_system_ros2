import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    motor_config_file = LaunchConfiguration('motor_config_file')
    robot_config_file = LaunchConfiguration('robot_config_file')

    motion_control_bridge_pkg_share = get_package_share_directory('motion_control_bridge')
    motion_control_robot_pkg_share = get_package_share_directory('motion_control_robot')

    default_motor_config_file = os.path.join(
        motion_control_bridge_pkg_share,
        'config',
        'example_ethercat_zeroerr.yaml',
    )
    default_robot_config_file = os.path.join(
        motion_control_robot_pkg_share,
        'config',
        'rocking_chair.yaml',
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'motor_config_file',
            default_value=default_motor_config_file,
            description='Absolute path to motor_manager YAML.',
        ),
        DeclareLaunchArgument(
            'robot_config_file',
            default_value=default_robot_config_file,
            description='Absolute path to robot_manager YAML.',
        ),
        Node(
            package='motion_control_bridge',
            executable='motor_manager_node',
            name='motor_manager_node',
            output='screen',
            parameters=[{
                'config_file': motor_config_file,
            }],
        ),
        Node(
            package='motion_control_robot',
            executable='robot_manager_node',
            name='robot_manager_node',
            output='screen',
            parameters=[{
                'config_file': robot_config_file,
            }],
        ),
        Node(
            package='motion_control_rqt',
            executable='run_rqt',
            name='motion_control',
            output='screen',
            arguments=['--force-discover'],
            parameters=[{
                'config_file': motor_config_file,
                'use_robot_manager_widget': True,
            }],
        ),
    ])
