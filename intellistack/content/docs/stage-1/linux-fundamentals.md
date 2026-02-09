---
id: linux-fundamentals
title: Linux Fundamentals for Robotics
sidebar_label: Linux Basics
sidebar_position: 3
---

# Linux Fundamentals for Robotics

Most robotics software runs on Linux (specifically Ubuntu). Understanding the Linux command line is essential for developing, deploying, and debugging robotic systems.

## Why Linux for Robotics?

- ✅ **ROS 2** is primarily developed for Ubuntu
- ✅ **Open source** with extensive community support
- ✅ **Powerful command-line tools** for automation
- ✅ **Package management** simplifies dependency installation
- ✅ **Real-time capabilities** for critical control loops

## Command Line Basics

### Navigation Commands

```bash
# Print working directory
pwd

# List files and directories
ls              # Basic list
ls -la          # Detailed list with hidden files
ls -lh          # Human-readable file sizes

# Change directory
cd /home/user/robotics      # Absolute path
cd ../..                    # Go up two levels
cd ~                        # Go to home directory
cd -                        # Go to previous directory

# Create directories
mkdir robot_project
mkdir -p workspace/src/robot_pkg  # Create nested directories
```

### File Operations

```bash
# Create files
touch robot_config.yaml
echo "Hello, Robot!" > message.txt

# Copy files
cp source.py destination.py
cp -r src/ backup/          # Copy directory recursively

# Move/rename files
mv old_name.py new_name.py
mv file.txt /path/to/destination/

# Remove files
rm file.txt
rm -r directory/            # Remove directory (careful!)
rm -rf build/               # Force remove (VERY careful!)

# View file contents
cat robot_config.yaml       # Print entire file
head -n 20 log.txt          # First 20 lines
tail -n 50 log.txt          # Last 50 lines
tail -f robot_log.txt       # Follow file (real-time updates)
```

### Text Processing

```bash
# Search in files
grep "error" robot_log.txt
grep -r "TODO" src/         # Recursive search
grep -i "warning" log.txt   # Case-insensitive

# Count lines, words, characters
wc -l robot_config.yaml     # Count lines
wc -w README.md             # Count words

# Filter and sort
cat data.csv | sort         # Sort lines
cat data.csv | uniq         # Remove duplicates
cat data.csv | head -n 10   # First 10 lines
```

### Pipes and Redirection

```bash
# Redirect output to file
echo "Starting robot..." > status.log
python robot.py > output.txt 2> errors.txt

# Append to file
echo "Task completed" >> status.log

# Pipe commands together
cat robot_log.txt | grep "ERROR" | wc -l    # Count errors
ps aux | grep python | grep -v grep         # Find Python processes
```

## Package Management (APT)

```bash
# Update package list
sudo apt update

# Upgrade installed packages
sudo apt upgrade

# Install packages
sudo apt install python3-pip
sudo apt install build-essential git cmake

# Search for packages
apt search ros2

# Remove packages
sudo apt remove package-name
sudo apt autoremove          # Remove unused dependencies
```

## File Permissions

```bash
# View permissions
ls -l file.py
# Output: -rwxr-xr-x 1 user group 1234 Jan 1 12:00 file.py
#         --------- owner permissions
#                --- group permissions
#                       --- other permissions

# Change permissions
chmod +x script.sh           # Make executable
chmod 755 file.py            # rwxr-xr-x
chmod 644 config.yaml        # rw-r--r--

# Change ownership
sudo chown user:group file.txt
```

## Process Management

```bash
# View running processes
ps aux                       # All processes
ps aux | grep python         # Find Python processes
top                          # Interactive process viewer
htop                         # Better process viewer (install first)

# Start process in background
python robot_controller.py &

# View background jobs
jobs

# Bring job to foreground
fg %1

# Kill processes
kill PID                     # Graceful termination
kill -9 PID                  # Force kill
pkill -f "robot_controller"  # Kill by name
```

## Environment Variables

```bash
# View environment variables
env
echo $HOME
echo $PATH

# Set temporary variable
export ROS_DOMAIN_ID=42

# Set permanent variable (add to ~/.bashrc)
echo 'export ROS_DOMAIN_ID=42' >> ~/.bashrc
source ~/.bashrc             # Reload configuration
```

## Networking Basics

```bash
# Check network interfaces
ip addr
ifconfig                     # Older command

# Test connectivity
ping google.com
ping 192.168.1.100

# Check open ports
sudo netstat -tulpn
sudo ss -tulpn               # Modern alternative

# Transfer files
scp file.txt user@robot:/home/user/
rsync -avz src/ user@robot:~/project/
```

## Shell Scripting

### Basic Script Structure

```bash
#!/bin/bash
# robot_startup.sh - Start robot services

echo "Starting robot systems..."

# Check if ROS is installed
if command -v ros2 &> /dev/null; then
    echo "ROS 2 found!"
else
    echo "Error: ROS 2 not installed"
    exit 1
fi

# Source ROS environment
source /opt/ros/humble/setup.bash
echo "ROS environment loaded"

# Start robot nodes
ros2 launch robot_bringup robot.launch.py &

echo "Robot startup complete!"
```

### Make Script Executable

```bash
chmod +x robot_startup.sh
./robot_startup.sh
```

## Common Robotics Workflows

### Setting Up ROS Workspace

```bash
# Create workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# Clone robot packages
git clone https://github.com/ros2/examples.git

# Build workspace
cd ~/ros2_ws
colcon build

# Source workspace
source install/setup.bash
```

### Monitoring Robot Logs

```bash
# View ROS logs
ros2 topic echo /robot/status
ros2 node list
ros2 topic list

# Follow custom log file
tail -f ~/ros2_ws/log/robot_controller.log
```

## Practice Exercises

### Exercise 1: File Organization Script

Create a bash script that organizes Python files into directories by type:

```bash
#!/bin/bash
# organize_files.sh

mkdir -p scripts tests configs

mv *.py scripts/
mv test_*.py tests/
mv *.yaml configs/

echo "Files organized!"
```

### Exercise 2: System Monitor

Write a script that checks CPU and memory usage:

```bash
#!/bin/bash
# system_monitor.sh

# Your code here
# Hint: Use 'top' or 'free' commands
```

### Exercise 3: Automated Backup

Create a script that backs up a directory with timestamp:

```bash
#!/bin/bash
# backup_workspace.sh

# Your code here
# Hint: Use 'tar' and 'date' commands
```

## Troubleshooting Tips

### Permission Denied

```bash
# Problem: Permission denied when running script
./script.sh

# Solution: Make executable
chmod +x script.sh
```

### Command Not Found

```bash
# Problem: ros2: command not found

# Solution: Source ROS environment
source /opt/ros/humble/setup.bash

# Make permanent
echo 'source /opt/ros/humble/setup.bash' >> ~/.bashrc
```

### Disk Space Issues

```bash
# Check disk usage
df -h                        # Human-readable disk space
du -sh ~/ros2_ws             # Size of directory

# Find large files
find . -type f -size +100M
```

## Key Takeaways

- ✅ Master basic navigation and file operations
- ✅ Understand permissions and ownership
- ✅ Use pipes to chain commands
- ✅ Write shell scripts for automation
- ✅ Monitor processes and system resources
- ✅ Configure environment variables for ROS

## Next Lesson

Continue to [Mathematics for Robotics](./math-foundations) to learn the mathematical foundations essential for understanding robot motion and control.

## Additional Resources

- [Linux Command Line Tutorial](https://ubuntu.com/tutorials/command-line-for-beginners)
- [Bash Scripting Guide](https://www.gnu.org/software/bash/manual/)
- [ROS 2 Documentation](https://docs.ros.org/en/humble/)
