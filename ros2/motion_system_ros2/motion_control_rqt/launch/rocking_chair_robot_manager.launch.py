import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def default_config_file(package_share_path, package_name, file_name):
    installed_path = os.path.join(package_share_path, 'config', file_name)
    path = os.path.abspath(package_share_path)

    while True:
        source_path = os.path.join(
            path,
            'src',
            'ros2',
            'motion_system_ros2',
            package_name,
            'config',
            file_name,
        )
        if os.path.isfile(source_path):
            return source_path

        parent = os.path.dirname(path)
        if parent == path:
            return installed_path
        path = parent


def generate_launch_description():
    motor_config_file = LaunchConfiguration('motor_config_file')
    robot_config_file = LaunchConfiguration('robot_config_file')
    jog_mode = LaunchConfiguration('jog_mode')

    motion_control_bridge_pkg_share = get_package_share_directory('motion_control_bridge')
    motion_control_robot_pkg_share = get_package_share_directory('motion_control_robot')

    default_motor_config_file = default_config_file(
        motion_control_bridge_pkg_share,
        'motion_control_bridge',
        'example_ethercat_zeroerr.yaml',
    )
    default_robot_config_file = default_config_file(
        motion_control_robot_pkg_share,
        'motion_control_robot',
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
        DeclareLaunchArgument(
            'jog_mode',
            default_value='false',
            description='Enable jog commands that use raw encoder targets.',
        ),
        Node(
            package='motion_control_bridge',
            executable='motor_manager_node',
            name='motor_manager_node',
            output='screen',
            parameters=[{
                'config_file': motor_config_file,
                'jog_mode': ParameterValue(jog_mode, value_type=bool),
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
                'jog_mode': ParameterValue(jog_mode, value_type=bool),
                'use_robot_manager_widget': True,
            }],
        ),
    ])
