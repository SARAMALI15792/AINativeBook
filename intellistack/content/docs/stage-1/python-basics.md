---
id: python-basics
title: Python Programming Basics
sidebar_label: Python Basics
sidebar_position: 2
---

# Python Programming for Robotics

Python is the primary programming language for robotics development due to its simplicity, extensive libraries, and strong community support. In this lesson, you'll master Python fundamentals essential for robotics.

## Variables and Data Types

### Basic Types

```python
# Numbers
age = 25                    # Integer
temperature = 36.6          # Float
is_robot_active = True      # Boolean

# Strings
robot_name = "Pepper"
status_message = 'Ready to operate'

# Collections
sensor_readings = [23.5, 24.1, 23.8, 24.2]  # List
robot_position = (10.5, 20.3, 0.0)          # Tuple (x, y, z)
robot_config = {                             # Dictionary
    'name': 'Atlas',
    'manufacturer': 'Boston Dynamics',
    'weight_kg': 89
}
```

### Type Conversion

```python
# String to number
speed_str = "15.5"
speed_float = float(speed_str)

# Number to string
count = 42
message = f"Robot count: {count}"

# List to tuple (immutable)
waypoints_list = [1, 2, 3]
waypoints_tuple = tuple(waypoints_list)
```

## Control Flow

### Conditional Statements

```python
def check_battery_level(battery_percentage):
    """Check battery and return appropriate action."""
    if battery_percentage < 20:
        return "Critical: Return to charging station"
    elif battery_percentage < 50:
        return "Low: Complete current task and charge"
    else:
        return "Normal: Continue operation"

# Usage
battery = 35
action = check_battery_level(battery)
print(action)  # Output: "Low: Complete current task and charge"
```

### Loops

```python
# For loop - iterate over sensor data
sensor_data = [23.5, 24.1, 26.3, 25.0, 24.8]

for reading in sensor_data:
    if reading > 25.0:
        print(f"Warning: High temperature detected: {reading}°C")

# While loop - robot movement
distance_to_goal = 100  # meters
speed = 5  # m/s
time = 0

while distance_to_goal > 0:
    distance_to_goal -= speed
    time += 1
    print(f"Time: {time}s, Distance remaining: {distance_to_goal}m")
```

## Functions

### Basic Function Definition

```python
def calculate_velocity(distance, time):
    """
    Calculate velocity given distance and time.

    Args:
        distance (float): Distance traveled in meters
        time (float): Time taken in seconds

    Returns:
        float: Velocity in m/s
    """
    if time == 0:
        raise ValueError("Time cannot be zero")
    return distance / time

# Usage
velocity = calculate_velocity(100, 20)
print(f"Velocity: {velocity} m/s")
```

### Lambda Functions

```python
# Simple lambda for quick calculations
square = lambda x: x ** 2
print(square(5))  # Output: 25

# Useful in data processing
distances = [10, 20, 15, 30, 25]
sorted_distances = sorted(distances, key=lambda x: x, reverse=True)
print(sorted_distances)  # [30, 25, 20, 15, 10]
```

## Object-Oriented Programming

### Classes and Objects

```python
class Robot:
    """Represents a robotic system."""

    def __init__(self, name, robot_type):
        """Initialize robot with name and type."""
        self.name = name
        self.robot_type = robot_type
        self.battery_level = 100
        self.position = {'x': 0, 'y': 0, 'z': 0}

    def move(self, x, y, z):
        """Move robot to new position."""
        self.position['x'] += x
        self.position['y'] += y
        self.position['z'] += z
        self.battery_level -= 1  # Moving consumes battery
        print(f"{self.name} moved to {self.position}")

    def charge(self):
        """Charge the robot battery to full."""
        self.battery_level = 100
        print(f"{self.name} fully charged!")

    def get_status(self):
        """Return current robot status."""
        return {
            'name': self.name,
            'type': self.robot_type,
            'battery': self.battery_level,
            'position': self.position
        }

# Create robot instance
my_robot = Robot("Atlas", "Humanoid")
my_robot.move(10, 5, 0)
my_robot.move(5, 3, 0)
print(my_robot.get_status())
```

### Inheritance

```python
class MobileRobot(Robot):
    """Mobile robot with wheel-based movement."""

    def __init__(self, name, num_wheels):
        super().__init__(name, "Mobile")
        self.num_wheels = num_wheels
        self.max_speed = 2.0  # m/s

    def set_speed(self, speed):
        """Set movement speed with validation."""
        if speed > self.max_speed:
            print(f"Warning: Speed limited to {self.max_speed} m/s")
            self.speed = self.max_speed
        else:
            self.speed = speed
            print(f"Speed set to {speed} m/s")

# Usage
mobile_bot = MobileRobot("Rover", num_wheels=4)
mobile_bot.set_speed(1.5)
mobile_bot.move(10, 0, 0)
```

## NumPy for Numerical Computing

```python
import numpy as np

# Create arrays
position = np.array([10.5, 20.3, 5.0])
velocity = np.array([1.0, 0.5, 0.0])

# Vector operations
new_position = position + velocity
print(f"New position: {new_position}")

# Matrix operations (rotation)
rotation_matrix = np.array([
    [0, -1, 0],
    [1,  0, 0],
    [0,  0, 1]
])

rotated_position = rotation_matrix @ position  # Matrix multiplication
print(f"Rotated position: {rotated_position}")

# Statistical operations
sensor_readings = np.array([23.5, 24.1, 23.8, 24.2, 26.1])
mean_temp = np.mean(sensor_readings)
std_temp = np.std(sensor_readings)
print(f"Average temperature: {mean_temp:.2f}°C (±{std_temp:.2f})")
```

## Practice Exercises

### Exercise 1: Temperature Converter

Create a function that converts between Celsius and Fahrenheit.

```python
def convert_temperature(value, to_unit):
    """
    Convert temperature between Celsius and Fahrenheit.

    Args:
        value (float): Temperature value
        to_unit (str): Target unit ('C' or 'F')

    Returns:
        float: Converted temperature
    """
    # Your code here
    pass
```

### Exercise 2: Robot Path Planner

Create a class that plans a path for a robot given start and goal positions.

```python
class PathPlanner:
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal
        self.waypoints = []

    def plan_straight_line(self, num_steps=10):
        """Plan a straight-line path with specified steps."""
        # Your code here
        pass

    def get_path_length(self):
        """Calculate total path length."""
        # Your code here
        pass
```

### Exercise 3: Sensor Data Analysis

Analyze sensor data using NumPy to detect anomalies.

```python
import numpy as np

sensor_data = np.array([23.5, 24.1, 23.8, 45.0, 24.2, 23.9, 24.3])

def detect_anomalies(data, threshold=2):
    """
    Detect anomalies using standard deviation.

    Args:
        data: numpy array of sensor readings
        threshold: number of standard deviations for anomaly

    Returns:
        indices of anomalous readings
    """
    # Your code here
    pass
```

## Key Takeaways

- ✅ Python uses dynamic typing and clean syntax
- ✅ Functions help organize code into reusable blocks
- ✅ Classes enable object-oriented design for complex systems
- ✅ NumPy provides efficient numerical operations for robotics
- ✅ Type hints and docstrings improve code readability

## Next Lesson

Continue to [Linux Fundamentals](./linux-fundamentals) to learn essential command-line skills for robotics development.

## Additional Resources

- [Official Python Tutorial](https://docs.python.org/3/tutorial/)
- [NumPy Documentation](https://numpy.org/doc/stable/)
- [Real Python - Robotics](https://realpython.com/tutorials/robotics/)
