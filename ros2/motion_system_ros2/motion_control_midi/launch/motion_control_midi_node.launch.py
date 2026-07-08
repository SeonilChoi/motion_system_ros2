import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


MOTION_SYSTEM_FILES_DIR = os.environ.get(
    'MOTION_SYSTEM_FILES_DIR',
    os.path.expanduser('~/colcon_ws/files'),
)
DEFAULT_MOTOR_CONFIG_FILE = os.path.join(
    MOTION_SYSTEM_FILES_DIR,
    'motor_manager',
    'example_ethercat_zeroerr.yaml',
)
DEFAULT_RECORD_FILE_PATH = os.path.join(
    MOTION_SYSTEM_FILES_DIR,
    'robot_manager',
    'rocking_chair.csv',
)


def generate_launch_description():
    motor_config_file = LaunchConfiguration('motor_config_file')
    record_motion = LaunchConfiguration('record_motion')
    record_file_path = LaunchConfiguration('record_file_path')
    jog_mode = LaunchConfiguration('jog_mode')

    return LaunchDescription([
        DeclareLaunchArgument(
            'motor_config_file',
            default_value=DEFAULT_MOTOR_CONFIG_FILE,
            description='Absolute path to motor_manager YAML.',
        ),
        DeclareLaunchArgument(
            'record_motion',
            default_value='false',
            description='Enable recording current motor_status positions when btn3 is activated.',
        ),
        DeclareLaunchArgument(
            'record_file_path',
            default_value=DEFAULT_RECORD_FILE_PATH,
            description='Absolute path where recorded motion CSV data is saved.',
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
                'record_motion': ParameterValue(record_motion, value_type=bool),
                'record_file_path': record_file_path,
            }],
        ),
    ])
