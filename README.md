# Motion System

This repository is a ROS 2 workspace source tree for motor control and related
operator interfaces. It includes a YAML-configured motor manager, ROS 2 bridge
nodes, controller input support, MIDI control support, and an iAHRS IMU driver.

## Clone

Clone this repository as the `src` directory of a colcon workspace:

```bash
mkdir -p ~/colcon_ws
cd ~/colcon_ws
git clone --recurse-submodules https://github.com/SeonilChoi/motion_system.git src
```

If the repository was cloned without submodules, initialize them later:

```bash
cd ~/colcon_ws/src
git submodule update --init --recursive
```

## Build

Install ROS 2 and source your ROS environment first. The examples below assume
ROS 2 Humble:

```bash
cd ~/colcon_ws
source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build
source install/setup.bash
```

For a motor-manager-only build:

```bash
colcon build --packages-up-to motion_control_bridge
```

## Launch

Launch the motor manager with the default example config:

```bash
source /opt/ros/humble/setup.bash
source ~/colcon_ws/install/setup.bash
ros2 launch motion_control_bridge motor_manager_node.launch.py
```

Use a specific motor configuration:

```bash
ros2 launch motion_control_bridge motor_manager_node.launch.py \
  config_file:=~/colcon_ws/src/ros2/motion_system_ros2/motion_control_bridge/config/example_socketcan_cubemars.yaml
```

Other useful launch commands:

```bash
# RQt motor control UI with motor manager
ros2 launch motion_control_rqt display_motor_manager_node.launch.py

# Behringer X-Touch MIDI bridge
ros2 launch xtouch_midi xtouch_node.launch.py

# MIDI-to-motor command bridge
ros2 launch motion_control_midi motion_control_midi_node.launch.py

# iAHRS IMU driver
ros2 launch iahrs_driver iahrs_driver.py

# PlayStation controller teleop
ros2 launch p9n_bringup teleop.launch.py hw_type:=DualSense
```

## Available Communication Methods

Motor communication backends:

- `ethercat`: IgH EtherCAT based cyclic motor communication.
- `canopen`: CANopen over SocketCAN.
- `socketcan`: raw SocketCAN communication.
- `serial`: serial communication for Dynamixel Protocol 2.0 devices.
- `dynamixel`: accepted as a Dynamixel-oriented master type in the motor
  manager configuration.

ROS and device interfaces:

- ROS 2 topics/services for motor commands, motor status, IMU data, and reset
  services.
- MIDI input/output for Behringer X-Touch devices.
- Linux joystick input for PlayStation controllers.
- Serial IMU communication for iAHRS devices.

## Available Drivers

Motor drivers supported by `motor_manager`:

- `dynamixel`
- `cubemars`
- `minas` for Panasonic MINAS drives
- `zeroerr` for ZeroErr drives

Device/interface drivers included in this workspace:

- `iahrs_driver`: iAHRS IMU ROS 2 driver.
- `p9n`: PlayStation controller interface for DualShock3, DualShock4, and
  DualSense controllers.
- `xtouch_midi`: Behringer X-Touch MIDI bridge.

Example motor configuration files are available in:

```text
ros2/motion_system_ros2/motion_control_bridge/config/
```

## 한국어 버전

### 개요

이 저장소는 모터 제어와 관련 운용 인터페이스를 위한 ROS 2 워크스페이스
소스 트리입니다. YAML 설정 기반 `motor_manager`, ROS 2 bridge 노드,
컨트롤러 입력, MIDI 제어, iAHRS IMU 드라이버를 포함합니다.

### Clone

이 저장소를 colcon 워크스페이스의 `src` 디렉터리로 clone합니다:

```bash
mkdir -p ~/colcon_ws
cd ~/colcon_ws
git clone --recurse-submodules https://github.com/SeonilChoi/motion_system.git src
```

submodule 없이 clone했다면 나중에 다음 명령으로 초기화합니다:

```bash
cd ~/colcon_ws/src
git submodule update --init --recursive
```

### Build

먼저 ROS 2를 설치하고 ROS 환경을 source해야 합니다. 아래 예시는 ROS 2
Humble 기준입니다:

```bash
cd ~/colcon_ws
source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build
source install/setup.bash
```

motor manager 관련 패키지만 빌드하려면:

```bash
colcon build --packages-up-to motion_control_bridge
```

### Launch

기본 예제 설정으로 motor manager를 실행합니다:

```bash
source /opt/ros/humble/setup.bash
source ~/colcon_ws/install/setup.bash
ros2 launch motion_control_bridge motor_manager_node.launch.py
```

특정 모터 설정 파일을 사용하려면:

```bash
ros2 launch motion_control_bridge motor_manager_node.launch.py \
  config_file:=~/colcon_ws/src/ros2/motion_system_ros2/motion_control_bridge/config/example_socketcan_cubemars.yaml
```

그 외 유용한 launch 명령:

```bash
# motor manager와 함께 RQt 모터 제어 UI 실행
ros2 launch motion_control_rqt display_motor_manager_node.launch.py

# Behringer X-Touch MIDI bridge
ros2 launch xtouch_midi xtouch_node.launch.py

# MIDI 입력을 모터 명령으로 변환하는 bridge
ros2 launch motion_control_midi motion_control_midi_node.launch.py

# iAHRS IMU 드라이버
ros2 launch iahrs_driver iahrs_driver.py

# PlayStation 컨트롤러 teleop
ros2 launch p9n_bringup teleop.launch.py hw_type:=DualSense
```

### Available Communication Methods

모터 통신 backend:

- `ethercat`: IgH EtherCAT 기반 주기적 모터 통신.
- `canopen`: SocketCAN 기반 CANopen 통신.
- `socketcan`: raw SocketCAN 통신.
- `serial`: Dynamixel Protocol 2.0 장치를 위한 serial 통신.
- `dynamixel`: motor manager 설정에서 Dynamixel 지향 master type으로 사용할 수 있습니다.

ROS 및 장치 인터페이스:

- 모터 명령, 모터 상태, IMU 데이터, reset 서비스를 위한 ROS 2 topic/service.
- Behringer X-Touch 장치를 위한 MIDI 입출력.
- PlayStation 컨트롤러를 위한 Linux joystick 입력.
- iAHRS 장치를 위한 serial IMU 통신.

### Available Drivers

`motor_manager`에서 지원하는 모터 driver:

- `dynamixel`
- `cubemars`
- `minas`: Panasonic MINAS drive용 driver
- `zeroerr`: ZeroErr drive용 driver

이 워크스페이스에 포함된 장치/interface driver:

- `iahrs_driver`: iAHRS IMU ROS 2 driver.
- `p9n`: DualShock3, DualShock4, DualSense 컨트롤러용 PlayStation controller interface.
- `xtouch_midi`: Behringer X-Touch MIDI bridge.

예제 모터 설정 파일은 다음 경로에 있습니다:

```text
ros2/motion_system_ros2/motion_control_bridge/config/
```
