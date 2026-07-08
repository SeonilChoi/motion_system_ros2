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

Runtime configs and motion files are read from `~/colcon_ws/files` by default:

| Type | Default path |
| --- | --- |
| Motor manager YAML | `~/colcon_ws/files/motor_manager/example_ethercat_zeroerr.yaml` |
| Robot manager YAML | `~/colcon_ws/files/robot_manager/rocking_chair.yaml` |
| Motion CSV | `~/colcon_ws/files/robot_manager/rocking_chair.csv` |

Set `MOTION_SYSTEM_FILES_DIR` before launching if the base folder changes.

### Run By Package

`motion_control_msgs` is a message package and has no launch file:

```bash
colcon build --packages-select motion_control_msgs
```

`motion_control_bridge` starts only `motor_manager_node`:

```bash
source /opt/ros/humble/setup.bash
source ~/colcon_ws/install/setup.bash
ros2 launch motion_control_bridge motor_manager_node.launch.py
```

Use a specific motor configuration with `config_file`:

```bash
ros2 launch motion_control_bridge motor_manager_node.launch.py \
  config_file:=$HOME/colcon_ws/files/motor_manager/example_socketcan_cubemars.yaml
```

`motion_control_rqt` has two launch modes:

```bash
# RQt motor control UI with motor manager
ros2 launch motion_control_rqt display_motor_manager_node.launch.py

# RQt motor and rocking-chair robot control UI
ros2 launch motion_control_rqt rocking_chair_robot_manager.launch.py
```

Use `motor_config_file` for RQt launch files, and `robot_config_file` when the
robot manager is included:

```bash
ros2 launch motion_control_rqt rocking_chair_robot_manager.launch.py \
  motor_config_file:=$HOME/colcon_ws/files/motor_manager/example_ethercat_zeroerr.yaml \
  robot_config_file:=$HOME/colcon_ws/files/robot_manager/rocking_chair.yaml
```

`motion_control_midi` starts `motion_control_bridge`, `xtouch_midi`, and
`motion_control_midi_node`:

```bash
# MIDI-to-motor command bridge
ros2 launch motion_control_midi motion_control_midi_node.launch.py

# Record motion data to one CSV path
ros2 launch motion_control_midi motion_control_midi_node.launch.py \
  record_motion:=true \
  record_file_path:=$HOME/colcon_ws/files/robot_manager/recorded_motion.csv
```

`motion_control_robot` starts joystick input, PlayStation teleop,
`motion_control_bridge`, and `robot_manager_node`:

```bash
ros2 launch motion_control_robot robot_manager_node.launch.py
```

Other useful launch commands:

```bash

# Behringer X-Touch MIDI bridge
ros2 launch xtouch_midi xtouch_node.launch.py

# iAHRS IMU driver
ros2 launch iahrs_driver iahrs_driver.py

# PlayStation controller teleop
ros2 launch p9n_bringup teleop.launch.py hw_type:=DualSense
```

RQt has two launch modes:

- `display_motor_manager_node.launch.py` opens the standard `MotorManagerWidget`
  for motor status monitoring and direct motor commands.
- `rocking_chair_robot_manager.launch.py` starts `motor_manager_node`,
  `robot_manager_node`, and RQt with `use_robot_manager_widget:=true`. In this
  mode the plugin uses `RobotManagerWidget`, which inherits from
  `MotorManagerWidget` and adds a second `Robot Manager` tab.

The `Robot Manager` tab publishes `sensor_msgs/msg/Joy` messages on `/joy` so it
drives `robot_manager_node` through the same button mapping as joystick input:

| Button | Joy index | Robot action |
| --- | --- | --- |
| `Disable` | `0` / Cross | Disable motor controllers |
| `Enable` | `9` / Start | Enable motor controllers |
| `Move` | `1` / Circle | Move |
| `Home` | `2` / Triangle | Home |
| `Stop` | `3` / Square | Stop |
| `L1` | `4` | Select previous robot |
| `R1` | `5` | Select next robot |

## Available Communication Methods

Motor communication backends:

- `ethercat`: IgH EtherCAT based cyclic motor communication.
- `canopen`: CANopen over SocketCAN.
- `socketcan`: raw SocketCAN communication.
- `serial`: serial communication for Dynamixel Protocol 2.0 devices.

ROS and device interfaces:

- ROS 2 topics/services for motor commands, motor status, IMU data, and reset
  services.
- MIDI input/output for Behringer X-Touch devices.
- Linux joystick input for PlayStation controllers and RQt-generated
  `sensor_msgs/msg/Joy` robot commands.
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
~/colcon_ws/files/motor_manager
```

Driver hardware parameter files are installed from:

```text
lib/motor_manager/hardware/<driver>/param/
```

The runtime bridge configs reference these files with `package://motor_manager/...`
paths. Dynamixel model control tables are kept under
`lib/motor_manager/hardware/dynamixel/param/control_table/`.

Robot motion CSV files are installed from:

```text
~/colcon_ws/files/robot_manager
```

Robot YAML files reference motion CSV files relative to the robot YAML location.

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

기본 runtime config와 motion 파일은 `~/colcon_ws/files`에서 읽고 씁니다:

| Type | Default path |
| --- | --- |
| Motor manager YAML | `~/colcon_ws/files/motor_manager/example_ethercat_zeroerr.yaml` |
| Robot manager YAML | `~/colcon_ws/files/robot_manager/rocking_chair.yaml` |
| Motion CSV | `~/colcon_ws/files/robot_manager/rocking_chair.csv` |

base folder가 바뀌면 launch 전에 `MOTION_SYSTEM_FILES_DIR` 환경변수를 설정합니다.

### Package별 실행

`motion_control_msgs`는 launch 파일이 없는 message package입니다:

```bash
colcon build --packages-select motion_control_msgs
```

`motion_control_bridge`는 `motor_manager_node`만 실행합니다:

```bash
source /opt/ros/humble/setup.bash
source ~/colcon_ws/install/setup.bash
ros2 launch motion_control_bridge motor_manager_node.launch.py
```

특정 motor config를 쓰려면 `config_file`을 넘깁니다:

```bash
ros2 launch motion_control_bridge motor_manager_node.launch.py \
  config_file:=$HOME/colcon_ws/files/motor_manager/example_socketcan_cubemars.yaml
```

`motion_control_rqt`는 두 가지 launch 모드를 가집니다:

```bash
# motor manager와 함께 RQt 모터 제어 UI 실행
ros2 launch motion_control_rqt display_motor_manager_node.launch.py

# motor manager와 rocking-chair robot 제어를 포함한 RQt UI 실행
ros2 launch motion_control_rqt rocking_chair_robot_manager.launch.py
```

RQt launch에서는 `motor_config_file`을 사용하고, robot manager를 포함할 때는
`robot_config_file`도 함께 넘깁니다:

```bash
ros2 launch motion_control_rqt rocking_chair_robot_manager.launch.py \
  motor_config_file:=$HOME/colcon_ws/files/motor_manager/example_ethercat_zeroerr.yaml \
  robot_config_file:=$HOME/colcon_ws/files/robot_manager/rocking_chair.yaml
```

`motion_control_midi`는 `motion_control_bridge`, `xtouch_midi`,
`motion_control_midi_node`를 함께 실행합니다:

```bash
# MIDI 입력을 모터 명령으로 변환하는 bridge
ros2 launch motion_control_midi motion_control_midi_node.launch.py

# motion data를 하나의 CSV 경로로 녹화
ros2 launch motion_control_midi motion_control_midi_node.launch.py \
  record_motion:=true \
  record_file_path:=$HOME/colcon_ws/files/robot_manager/recorded_motion.csv
```

`motion_control_robot`은 joystick input, PlayStation teleop,
`motion_control_bridge`, `robot_manager_node`를 함께 실행합니다:

```bash
ros2 launch motion_control_robot robot_manager_node.launch.py
```

그 외 유용한 launch 명령:

```bash

# Behringer X-Touch MIDI bridge
ros2 launch xtouch_midi xtouch_node.launch.py

# iAHRS IMU 드라이버
ros2 launch iahrs_driver iahrs_driver.py

# PlayStation 컨트롤러 teleop
ros2 launch p9n_bringup teleop.launch.py hw_type:=DualSense
```

RQt는 두 가지 launch 모드를 가진다:

- `display_motor_manager_node.launch.py`는 기본 `MotorManagerWidget`만 열어서
  motor 상태 확인과 직접 motor command 전송을 제공한다.
- `rocking_chair_robot_manager.launch.py`는 `motor_manager_node`,
  `robot_manager_node`, RQt를 함께 실행하고 `use_robot_manager_widget:=true`를
  전달한다. 이 모드에서는 `MotorManagerWidget`을 상속한 `RobotManagerWidget`이
  실행되며 두 번째 `Robot Manager` 탭이 추가된다.

`Robot Manager` 탭은 `/joy`로 `sensor_msgs/msg/Joy` 메시지를 발행한다.
따라서 `robot_manager_node`는 joystick 입력과 같은 button mapping으로 동작한다:

| Button | Joy index | Robot action |
| --- | --- | --- |
| `Disable` | `0` / Cross | motor controller disable |
| `Enable` | `9` / Start | motor controller enable |
| `Move` | `1` / Circle | Move |
| `Home` | `2` / Triangle | Home |
| `Stop` | `3` / Square | Stop |
| `L1` | `4` | 이전 robot 선택 |
| `R1` | `5` | 다음 robot 선택 |

### Available Communication Methods

모터 통신 backend:

- `ethercat`: IgH EtherCAT 기반 주기적 모터 통신.
- `canopen`: SocketCAN 기반 CANopen 통신.
- `socketcan`: raw SocketCAN 통신.
- `serial`: Dynamixel Protocol 2.0 장치를 위한 serial 통신.

ROS 및 장치 인터페이스:

- 모터 명령, 모터 상태, IMU 데이터, reset 서비스를 위한 ROS 2 topic/service.
- Behringer X-Touch 장치를 위한 MIDI 입출력.
- PlayStation 컨트롤러를 위한 Linux joystick 입력과 RQt가 발행하는
  `sensor_msgs/msg/Joy` robot command.
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
~/colcon_ws/files/motor_manager
```

driver 하드웨어 파라미터 파일은 다음 위치에서 설치됩니다:

```text
lib/motor_manager/hardware/<driver>/param/
```

런타임 bridge 설정은 이 파일들을 `package://motor_manager/...` 경로로 참조합니다.
Dynamixel model control table은
`lib/motor_manager/hardware/dynamixel/param/control_table/` 아래에 있습니다.

robot motion CSV 파일은 다음 위치에서 설치됩니다:

```text
~/colcon_ws/files/robot_manager
```

robot YAML 파일은 motion CSV를 robot YAML 위치 기준 상대 경로로 참조합니다.
