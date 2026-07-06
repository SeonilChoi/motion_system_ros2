from rqt_gui_py.plugin import Plugin

from motion_control_rqt.motor_manager_widget import MotorManagerWidget

class MotionControlController(Plugin):
    def __init__(self, context):
        super().__init__(context)

        self.setObjectName('MotionControlController')

        if not context.node.has_parameter('use_robot_manager_widget'):
            context.node.declare_parameter('use_robot_manager_widget', False)

        use_robot_manager_widget = self._parameter_as_bool(
            context.node.get_parameter('use_robot_manager_widget').value
        )
        if use_robot_manager_widget:
            from motion_control_rqt.robot_manager_widget import RobotManagerWidget
            self.widget = RobotManagerWidget(context.node)
        else:
            self.widget = MotorManagerWidget(context.node)

        serial_number = context.serial_number()
        if serial_number >= 1:
            self.widget.setWindowTitle(self.widget.windowTitle() + f' {serial_number}')
        
        context.add_widget(self.widget)

    def shutdown_plugin(self):
        print('MotionControlController shutdown')
        self.widget.shutdown_widget()

    @staticmethod
    def _parameter_as_bool(value):
        if isinstance(value, str):
            return value.lower() in ('1', 'true', 'yes', 'on')
        return bool(value)
