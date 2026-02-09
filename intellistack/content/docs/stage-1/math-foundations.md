---
id: math-foundations
title: Mathematics for Robotics
sidebar_label: Math Foundations
sidebar_position: 4
---

# Mathematics for Robotics

Mathematics is the language of robotics. This lesson covers essential mathematical concepts you'll use throughout your robotics journey.

## Linear Algebra

### Vectors

Vectors represent position, velocity, force, and direction in robotics.

```python
import numpy as np

# 3D position vector
position = np.array([10.5, 20.3, 5.0])  # [x, y, z]

# Velocity vector
velocity = np.array([1.0, 0.5, 0.0])    # [vx, vy, vz]

# Vector operations
new_position = position + velocity
print(f"New position: {new_position}")

# Vector magnitude (length)
speed = np.linalg.norm(velocity)
print(f"Speed: {speed:.2f} m/s")

# Dot product (projection)
a = np.array([1, 0, 0])
b = np.array([1, 1, 0])
dot_product = np.dot(a, b)
print(f"Dot product: {dot_product}")

# Cross product (perpendicular vector)
cross_product = np.cross(a, b)
print(f"Cross product: {cross_product}")
```

### Matrices

Matrices represent transformations like rotation, scaling, and translation.

```python
# 2D Rotation Matrix (90 degrees counterclockwise)
theta = np.pi / 2  # 90 degrees in radians
rotation_2d = np.array([
    [np.cos(theta), -np.sin(theta)],
    [np.sin(theta),  np.cos(theta)]
])

# Apply rotation to point
point = np.array([1, 0])
rotated_point = rotation_2d @ point
print(f"Rotated point: {rotated_point}")

# 3D Rotation Matrix (around Z-axis)
def rotation_matrix_z(angle_rad):
    """Create 3D rotation matrix around Z-axis."""
    c = np.cos(angle_rad)
    s = np.sin(angle_rad)
    return np.array([
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1]
    ])

# Homogeneous transformation (rotation + translation)
def transformation_matrix(rotation, translation):
    """Create 4x4 transformation matrix."""
    T = np.eye(4)
    T[:3, :3] = rotation
    T[:3, 3] = translation
    return T

rotation = rotation_matrix_z(np.pi / 4)
translation = np.array([10, 20, 0])
T = transformation_matrix(rotation, translation)
print(f"Transformation matrix:\n{T}")
```

## Calculus

### Derivatives (Rate of Change)

```python
import numpy as np
import matplotlib.pyplot as plt

# Position as function of time
def position(t):
    return 5 * t**2 + 2 * t + 1

# Velocity is derivative of position
def velocity(t):
    return 10 * t + 2

# Acceleration is derivative of velocity
def acceleration(t):
    return 10

# Plot position, velocity, acceleration
t = np.linspace(0, 5, 100)
plt.figure(figsize=(10, 6))
plt.plot(t, position(t), label='Position')
plt.plot(t, velocity(t), label='Velocity')
plt.plot(t, acceleration(t), label='Acceleration')
plt.xlabel('Time (s)')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.title('Kinematic Relationships')
```

### Numerical Differentiation

```python
def numerical_derivative(func, x, h=1e-5):
    """
    Calculate derivative using finite differences.

    Args:
        func: Function to differentiate
        x: Point to evaluate derivative
        h: Small step size

    Returns:
        Approximate derivative at x
    """
    return (func(x + h) - func(x - h)) / (2 * h)

# Example: Velocity from position
def robot_position(t):
    return 3 * t**2 + 2 * t

t = 2.0
velocity = numerical_derivative(robot_position, t)
print(f"Velocity at t={t}: {velocity:.2f} m/s")
```

### Integration (Area Under Curve)

```python
from scipy import integrate

# Distance traveled given velocity function
def velocity_func(t):
    return 5 * np.sin(t) + 3

# Integrate from t=0 to t=10
distance, error = integrate.quad(velocity_func, 0, 10)
print(f"Distance traveled: {distance:.2f} meters")
```

## Probability and Statistics

### Basic Statistics

```python
import numpy as np

# Sensor measurements with noise
measurements = np.array([10.2, 10.5, 9.8, 10.1, 10.4, 9.9, 10.3])

# Central tendency
mean = np.mean(measurements)
median = np.median(measurements)

# Spread
std_dev = np.std(measurements)
variance = np.var(measurements)

print(f"Mean: {mean:.2f}")
print(f"Std Dev: {std_dev:.2f}")
```

### Probability Distributions

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Normal distribution (common in sensor noise)
mean = 0
std_dev = 1
x = np.linspace(-4, 4, 100)
pdf = stats.norm.pdf(x, mean, std_dev)

plt.plot(x, pdf)
plt.title('Normal Distribution (Gaussian)')
plt.xlabel('Value')
plt.ylabel('Probability Density')
plt.grid(True)
```

### Random Sampling

```python
# Generate random sensor noise
noise = np.random.normal(0, 0.1, 1000)  # mean=0, std=0.1

# Sample from uniform distribution
random_angles = np.random.uniform(0, 2*np.pi, 100)

# Random choice (useful for simulation)
actions = ['forward', 'left', 'right', 'stop']
random_action = np.random.choice(actions)
```

## Coordinate Systems and Transformations

### 2D Transformations

```python
def transform_2d(point, angle, translation):
    """
    Transform a 2D point with rotation and translation.

    Args:
        point: [x, y] position
        angle: Rotation angle in radians
        translation: [tx, ty] translation vector

    Returns:
        Transformed point
    """
    # Rotation matrix
    c, s = np.cos(angle), np.sin(angle)
    R = np.array([[c, -s], [s, c]])

    # Rotate then translate
    rotated = R @ point
    transformed = rotated + translation

    return transformed

# Example: Transform robot position
robot_pos = np.array([5, 0])
angle = np.pi / 4  # 45 degrees
translation = np.array([10, 20])

new_pos = transform_2d(robot_pos, angle, translation)
print(f"New position: {new_pos}")
```

### 3D Rotations (Euler Angles)

```python
def rotation_matrix_euler(roll, pitch, yaw):
    """
    Create 3D rotation matrix from Euler angles.

    Args:
        roll: Rotation around X-axis (radians)
        pitch: Rotation around Y-axis (radians)
        yaw: Rotation around Z-axis (radians)

    Returns:
        3x3 rotation matrix
    """
    # Rotation around X (roll)
    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(roll), -np.sin(roll)],
        [0, np.sin(roll), np.cos(roll)]
    ])

    # Rotation around Y (pitch)
    Ry = np.array([
        [np.cos(pitch), 0, np.sin(pitch)],
        [0, 1, 0],
        [-np.sin(pitch), 0, np.cos(pitch)]
    ])

    # Rotation around Z (yaw)
    Rz = np.array([
        [np.cos(yaw), -np.sin(yaw), 0],
        [np.sin(yaw), np.cos(yaw), 0],
        [0, 0, 1]
    ])

    # Combined rotation (order: yaw, pitch, roll)
    return Rz @ Ry @ Rx

# Example
roll, pitch, yaw = 0, 0, np.pi/4
R = rotation_matrix_euler(roll, pitch, yaw)
print(f"Rotation matrix:\n{R}")
```

## Practice Exercises

### Exercise 1: Distance Calculator

Calculate the Euclidean distance between two 3D points:

```python
def euclidean_distance(p1, p2):
    """
    Calculate distance between two 3D points.

    Args:
        p1: First point [x, y, z]
        p2: Second point [x, y, z]

    Returns:
        Distance
    """
    # Your code here
    pass

# Test
point_a = np.array([0, 0, 0])
point_b = np.array([3, 4, 0])
distance = euclidean_distance(point_a, point_b)
# Expected: 5.0
```

### Exercise 2: Sensor Fusion

Combine multiple noisy sensor readings using weighted average:

```python
def fuse_sensors(readings, weights):
    """
    Fuse sensor readings with confidence weights.

    Args:
        readings: Array of sensor values
        weights: Array of confidence weights (sum to 1)

    Returns:
        Fused estimate
    """
    # Your code here
    pass

# Test
readings = np.array([10.2, 10.5, 9.8])
weights = np.array([0.5, 0.3, 0.2])
fused = fuse_sensors(readings, weights)
```

### Exercise 3: Trajectory Generator

Generate a smooth trajectory between start and goal positions:

```python
def generate_trajectory(start, goal, num_points=10):
    """
    Generate linear trajectory between two points.

    Args:
        start: Starting position [x, y, z]
        goal: Goal position [x, y, z]
        num_points: Number of waypoints

    Returns:
        Array of waypoints
    """
    # Your code here
    # Hint: Use np.linspace
    pass
```

## Key Takeaways

- ✅ Vectors represent position, velocity, and direction
- ✅ Matrices enable transformations (rotation, translation)
- ✅ Calculus describes motion (position → velocity → acceleration)
- ✅ Probability handles sensor noise and uncertainty
- ✅ Coordinate transformations are fundamental to robotics

## Next Lesson

Continue to [Physics for Robotics](./physics-basics) to understand the physical principles governing robot motion.

## Additional Resources

- [Linear Algebra for Machine Learning](https://www.deeplearningbook.org/contents/linear_algebra.html)
- [3Blue1Brown - Essence of Linear Algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab)
- [Khan Academy - Calculus](https://www.khanacademy.org/math/calculus-1)
