---
id: ros2-setup
title: ROS 2 Installation and Setup
sidebar_label: ROS 2 Setup
sidebar_position: 2
---

# ROS 2 Installation and Setup

ROS 2 (Robot Operating System 2) is the industry-standard middleware for building robot applications. This lesson will guide you through installing and configuring ROS 2 Humble.

## What is ROS 2?

ROS 2 is a set of software libraries and tools for building robot applications. It provides:

- **Communication middleware**: Publish/subscribe messaging
- **Hardware abstraction**: Unified interface for sensors and actuators
- **Device drivers**: Pre-built drivers for common robotics hardware
- **Visualization tools**: RViz for 3D visualization
- **Simulation**: Gazebo integration

## System Requirements

- **OS**: Ubuntu 22.04 LTS (Jammy Jellyfish)
- **Disk Space**: ~5 GB for ROS 2 + dependencies
- **RAM**: Minimum 4 GB (8 GB recommended)
- **ROS 2 Distribution**: Humble Hawksbill (LTS until 2027)

## Installation Steps

### 1. Setup Sources

```bash
# Ensure locale supports UTF-8
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# Setup sources
sudo apt install software-properties-common
sudo add-apt-repository universe

# Add ROS 2 GPG key
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg

# Add repository to sources list
echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
  http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
  | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

### 2. Install ROS 2

```bash
# Update apt cache
sudo apt update
sudo apt upgrade

# Install ROS 2 Humble Desktop (includes RViz, demos, tutorials)
sudo apt install ros-humble-desktop

# Install development tools
sudo apt install ros-dev-tools
```

### 3. Environment Setup

```bash
# Source ROS 2 environment
source /opt/ros/humble/setup.bash

# Make permanent (add to ~/.bashrc)
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc

# Verify installation
ros2 --version
# Expected output: ros2 cli version: humble
```

### 4. Additional Dependencies

```bash
# Install colcon (build tool)
sudo apt install python3-colcon-common-extensions

# Install rosdep (dependency management)
sudo apt install python3-rosdep
sudo rosdep init
rosdep update
```

## Verify Installation

```bash
# Run demo talker node
ros2 run demo_nodes_cpp talker

# In another terminal, run listener
ros2 run demo_nodes_cpp listener

# You should see messages being published and received
```

## Create Your First Workspace

```bash
# Create workspace directory
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# Clone example repository
git clone https://github.com/ros/ros_tutorials.git -b humble

# Build workspace
cd ~/ros2_ws
colcon build

# Source workspace overlay
source install/setup.bash

# Test workspace
ros2 run turtlesim turtlesim_node
```

## ROS 2 Concepts

### Nodes

Nodes are processes that perform computation. A robot system consists of many nodes working together.

```bash
# List running nodes
ros2 node list

# Get node information
ros2 node info /turtlesim
```

### Topics

Topics are named buses for message passing between nodes.

```bash
# List topics
ros2 topic list

# Echo messages from topic
ros2 topic echo /turtle1/pose

# Publish to topic
ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.8}}"

# Topic information
ros2 topic info /turtle1/cmd_vel
```

### Services

Services provide request/response communication.

```bash
# List services
ros2 service list

# Call service
ros2 service call /spawn turtlesim/srv/Spawn \
  "{x: 2, y: 2, theta: 0.2, name: 'turtle2'}"
```

## Configuration

### DDS Configuration (Network Discovery)

```bash
# Set ROS domain ID (isolate your robots)
export ROS_DOMAIN_ID=42

# Add to ~/.bashrc for persistence
echo "export ROS_DOMAIN_ID=42" >> ~/.bashrc
```

### Environment Variables

```bash
# Important ROS 2 environment variables
export ROS_DOMAIN_ID=42          # Network domain
export ROS_LOCALHOST_ONLY=1      # Restrict to localhost
export RCUTILS_COLORIZED_OUTPUT=1  # Colored log output
export RCUTILS_CONSOLE_OUTPUT_FORMAT="[{time}] [{severity}] [{name}]: {message}"
```

## Troubleshooting

### "Command not found: ros2"

```bash
# Solution: Source ROS environment
source /opt/ros/humble/setup.bash
```

### "No executable found"

```bash
# Solution: Check if package is installed
ros2 pkg list | grep package_name

# Install if missing
sudo apt install ros-humble-package-name
```

### DDS Communication Issues

```bash
# Check if nodes can communicate
ros2 multicast receive
# In another terminal:
ros2 multicast send

# If multicast doesn't work, use localhost only
export ROS_LOCALHOST_ONLY=1
```

## Key Takeaways

- ✅ ROS 2 Humble is the current LTS version
- ✅ Always source setup.bash before using ROS commands
- ✅ Workspaces organize your custom packages
- ✅ Nodes communicate via topics, services, and actions
- ✅ DDS handles network communication between nodes

## Next Lesson

Continue to [ROS 2 Programming Basics](./ros2-programming) to create your first ROS 2 nodes!

## Additional Resources

- [ROS 2 Documentation](https://docs.ros.org/en/humble/)
- [ROS 2 Tutorials](https://docs.ros.org/en/humble/Tutorials.html)
- [ROS Discourse Forum](https://discourse.ros.org/)
