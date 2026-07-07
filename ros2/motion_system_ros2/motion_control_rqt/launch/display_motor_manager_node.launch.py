from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

import os


def generate_launch_description():
    motion_control_bridge_pkg_share = get_package_share_directory('motion_control_bridge')
    default_motor_config = os.path.join(
        motion_control_bridge_pkg_share,
        'config',
        'example_ethercat_zeroerr.yaml',
    )

    motor_config_file_arg = DeclareLaunchArgument(
        'motor_config_file',
        default_value=default_motor_config,
        description='Absolute path to motor_manager YAML (masters / drivers).',
    )
    debug_mode_arg = DeclareLaunchArgument(
        'debug_mode',
        default_value='false',
        description='Use raw encoder values instead of position for target position commands.',
    )

    motor_manager = Node(
        package='motion_control_bridge',
        executable='motor_manager_node',
        name='motor_manager_node',
        output='screen',
        parameters=[{
            'config_file': LaunchConfiguration('motor_config_file'),
            'debug_mode': ParameterValue(LaunchConfiguration('debug_mode'), value_type=bool),
        }],
    )

    motion_control = Node(
        package='motion_control_rqt',
        executable='run_rqt',
        name='motion_control',
        output='screen',
        arguments=['--force-discover'],
        parameters=[{
            'config_file': LaunchConfiguration('motor_config_file'),
            'debug_mode': ParameterValue(LaunchConfiguration('debug_mode'), value_type=bool),
        }],
    )

    return LaunchDescription([
        motor_config_file_arg,
        debug_mode_arg,
        motor_manager,
        motion_control,
    ])
