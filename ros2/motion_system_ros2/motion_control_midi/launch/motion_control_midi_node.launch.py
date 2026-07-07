import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def default_source_motion_directory(*package_share_paths):
    for package_share_path in package_share_paths:
        path = os.path.abspath(package_share_path)
        while True:
            candidate = os.path.join(
                path,
                'src',
                'lib',
                'robot_manager',
                'robots',
                'motions',
            )
            if os.path.isdir(candidate):
                return candidate

            parent = os.path.dirname(path)
            if parent == path:
                break
            path = parent

    return ''


def generate_launch_description():
    motor_config_file = LaunchConfiguration('motor_config_file')
    robot_config_file = LaunchConfiguration('robot_config_file')
    record_motion = LaunchConfiguration('record_motion')
    record_file_name = LaunchConfiguration('record_file_name')
    record_directory = LaunchConfiguration('record_directory')
    debug_mode = LaunchConfiguration('debug_mode')

    motion_control_midi_pkg_share = get_package_share_directory('motion_control_midi')
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
    default_record_directory = default_source_motion_directory(
        motion_control_midi_pkg_share,
        motion_control_robot_pkg_share,
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
            'record_motion',
            default_value='false',
            description='Enable recording current motor_status positions when btn3 is activated.',
        ),
        DeclareLaunchArgument(
            'record_file_name',
            default_value='rocking_chair.csv',
            description='CSV file name for recorded motion data.',
        ),
        DeclareLaunchArgument(
            'record_directory',
            default_value=default_record_directory,
            description='Directory where recorded motion CSV files are saved.',
        ),
        DeclareLaunchArgument(
            'debug_mode',
            default_value='false',
            description='Use raw encoder values instead of position for target position commands.',
        ),
        Node(
            package='motion_control_bridge',
            executable='motor_manager_node',
            name='motor_manager_node',
            output='screen',
            parameters=[{
                'config_file': motor_config_file,
                'debug_mode': ParameterValue(debug_mode, value_type=bool),
            }],
        ),
        Node(
            package='xtouch_midi',
            executable='xtouch_node',
            name='xtouch_node',
            output='screen',
            parameters=[{
                'btn0_requires_fader_update': True,
                'btn3_requires_fader_update': True,
            }],
        ),
        Node(
            package='motion_control_midi',
            executable='motion_control_midi_node',
            name='motion_control_midi_node',
            output='screen',
            parameters=[{
                'config_file': motor_config_file,
                'robot_config_file': robot_config_file,
                'record_motion': ParameterValue(record_motion, value_type=bool),
                'record_file_name': record_file_name,
                'record_directory': record_directory,
            }],
        ),
    ])
