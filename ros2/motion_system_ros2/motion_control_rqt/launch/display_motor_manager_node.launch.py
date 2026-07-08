from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

import os


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
    motion_control_bridge_pkg_share = get_package_share_directory('motion_control_bridge')
    default_motor_config = default_config_file(
        motion_control_bridge_pkg_share,
        'motion_control_bridge',
        'example_ethercat_zeroerr.yaml',
    )

    motor_config_file_arg = DeclareLaunchArgument(
        'motor_config_file',
        default_value=default_motor_config,
        description='Absolute path to motor_manager YAML (masters / drivers).',
    )
    jog_mode_arg = DeclareLaunchArgument(
        'jog_mode',
        default_value='false',
        description='Enable jog commands that use raw encoder targets.',
    )

    motor_manager = Node(
        package='motion_control_bridge',
        executable='motor_manager_node',
        name='motor_manager_node',
        output='screen',
        parameters=[{
            'config_file': LaunchConfiguration('motor_config_file'),
            'jog_mode': ParameterValue(LaunchConfiguration('jog_mode'), value_type=bool),
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
            'jog_mode': ParameterValue(LaunchConfiguration('jog_mode'), value_type=bool),
        }],
    )

    return LaunchDescription([
        motor_config_file_arg,
        jog_mode_arg,
        motor_manager,
        motion_control,
    ])
