from python_qt_binding.QtCore import QTimer
from python_qt_binding.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from sensor_msgs.msg import Joy

from motion_control_rqt.motor_manager_widget import MotorManagerWidget


JOY_BUTTON_MAX = 10

JOY_BUTTON_CROSS = 0
JOY_BUTTON_CIRCLE = 1
JOY_BUTTON_TRIANGLE = 2
JOY_BUTTON_SQUARE = 3
JOY_BUTTON_PREVIOUS = 4
JOY_BUTTON_NEXT = 5
JOY_BUTTON_START = 9


class RobotManagerWidget(MotorManagerWidget):
    def __init__(self, node):
        super().__init__(node)

        self._joy_publisher = self._node.create_publisher(Joy, 'joy', 10)
        self._add_robot_manager_tab()

    def _add_robot_manager_tab(self):
        if self.q_tab_widget is None:
            return

        robot_tab = QWidget()
        robot_tab_layout = QVBoxLayout(robot_tab)

        command_box = QGroupBox('Robot Manager', robot_tab)
        command_layout = QHBoxLayout(command_box)

        disable_button = QPushButton('Disable', command_box)
        enable_button = QPushButton('Enable', command_box)
        home_button = QPushButton('Home', command_box)
        stop_button = QPushButton('Stop', command_box)
        move_button = QPushButton('Move', command_box)
        previous_button = QPushButton('Previous', command_box)
        next_button = QPushButton('Next', command_box)

        disable_button.clicked.connect(
            lambda: self._publish_joy_button(JOY_BUTTON_CROSS)
        )
        enable_button.clicked.connect(
            lambda: self._publish_joy_button(JOY_BUTTON_START)
        )
        home_button.clicked.connect(
            lambda: self._publish_joy_button(JOY_BUTTON_TRIANGLE)
        )
        stop_button.clicked.connect(
            lambda: self._publish_joy_button(JOY_BUTTON_SQUARE)
        )
        move_button.clicked.connect(
            lambda: self._publish_joy_button(JOY_BUTTON_CIRCLE)
        )
        previous_button.clicked.connect(
            lambda: self._publish_joy_button(JOY_BUTTON_PREVIOUS)
        )
        next_button.clicked.connect(
            lambda: self._publish_joy_button(JOY_BUTTON_NEXT)
        )

        command_layout.addWidget(disable_button)
        command_layout.addWidget(enable_button)
        command_layout.addWidget(home_button)
        command_layout.addWidget(stop_button)
        command_layout.addWidget(move_button)
        command_layout.addWidget(previous_button)
        command_layout.addWidget(next_button)

        robot_tab_layout.addWidget(command_box)
        robot_tab_layout.addStretch(1)

        self.q_tab_widget.addTab(robot_tab, 'Robot Manager')

    def _publish_joy_button(self, button_index: int):
        self._publish_joy(button_index, pressed=True)
        QTimer.singleShot(100, lambda: self._publish_joy(button_index, pressed=False))

    def _publish_joy(self, button_index: int, pressed: bool):
        msg = Joy()
        msg.header.stamp = self._node.get_clock().now().to_msg()
        msg.axes = []
        msg.buttons = [0] * JOY_BUTTON_MAX
        if 0 <= button_index < JOY_BUTTON_MAX:
            msg.buttons[button_index] = 1 if pressed else 0
        self._joy_publisher.publish(msg)
