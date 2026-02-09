---
id: physics-basics
title: Physics Fundamentals for Robotics
sidebar_label: Physics Basics
sidebar_position: 5
---

# Physics Fundamentals for Robotics

Understanding physics is crucial for designing, simulating, and controlling robots. This lesson covers the core physics concepts you'll apply in robotics.

## Kinematics (Motion Without Forces)

### Position, Velocity, and Acceleration

```python
import numpy as np
import matplotlib.pyplot as plt

# Position as function of time (constant acceleration)
def position(t, v0=0, a=2.0):
    """
    Calculate position with constant acceleration.

    x(t) = x0 + v0*t + 0.5*a*t^2
    """
    return v0 * t + 0.5 * a * t**2

# Velocity
def velocity(t, v0=0, a=2.0):
    """v(t) = v0 + a*t"""
    return v0 + a * t

# Simulation
time = np.linspace(0, 5, 100)
pos = position(time)
vel = velocity(time)

print(f"Position at t=5s: {position(5):.2f} m")
print(f"Velocity at t=5s: {velocity(5):.2f} m/s")
```

### 2D Motion (Projectile)

```python
def projectile_motion(v0, angle_deg, g=9.81):
    """
    Calculate projectile trajectory.

    Args:
        v0: Initial velocity (m/s)
        angle_deg: Launch angle (degrees)
        g: Gravity (m/s^2)

    Returns:
        time, x, y arrays
    """
    angle_rad = np.radians(angle_deg)
    vx = v0 * np.cos(angle_rad)
    vy = v0 * np.sin(angle_rad)

    # Time of flight
    t_flight = 2 * vy / g

    # Generate trajectory
    t = np.linspace(0, t_flight, 100)
    x = vx * t
    y = vy * t - 0.5 * g * t**2

    return t, x, y

# Example: Robot arm throwing object
t, x, y = projectile_motion(v0=10, angle_deg=45)
plt.plot(x, y)
plt.xlabel('Distance (m)')
plt.ylabel('Height (m)')
plt.title('Projectile Motion')
plt.grid(True)
```

## Dynamics (Forces and Motion)

### Newton's Laws

```python
# F = ma (Force = mass × acceleration)
mass = 50.0  # kg (robot mass)
acceleration = 2.0  # m/s^2

force_required = mass * acceleration
print(f"Force required: {force_required} N")

# Friction force
mu = 0.3  # Coefficient of friction
normal_force = mass * 9.81  # Weight
friction_force = mu * normal_force
print(f"Friction force: {friction_force:.2f} N")
```

### Momentum and Collisions

```python
def collision_velocity(m1, v1, m2, v2):
    """
    Calculate velocities after elastic collision.

    Conservation of momentum: m1*v1 + m2*v2 = m1*v1' + m2*v2'
    Conservation of energy: 0.5*m1*v1^2 + 0.5*m2*v2^2 = 0.5*m1*v1'^2 + 0.5*m2*v2'^2
    """
    # Final velocity of object 1
    v1_final = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)

    # Final velocity of object 2
    v2_final = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)

    return v1_final, v2_final

# Example: Robot colliding with object
m_robot = 50  # kg
v_robot = 2.0  # m/s
m_object = 10  # kg
v_object = 0  # Stationary

v_robot_after, v_object_after = collision_velocity(m_robot, v_robot, m_object, v_object)
print(f"Robot velocity after: {v_robot_after:.2f} m/s")
print(f"Object velocity after: {v_object_after:.2f} m/s")
```

## Energy and Work

```python
# Kinetic energy
def kinetic_energy(mass, velocity):
    """KE = 0.5 * m * v^2"""
    return 0.5 * mass * velocity**2

# Potential energy (gravitational)
def potential_energy(mass, height, g=9.81):
    """PE = m * g * h"""
    return mass * g * height

# Work done
def work_done(force, distance):
    """W = F * d"""
    return force * distance

# Example: Robot climbing ramp
robot_mass = 50  # kg
ramp_height = 2  # meters
ramp_distance = 10  # meters

# Energy required to climb
energy_required = potential_energy(robot_mass, ramp_height)
print(f"Energy required: {energy_required:.2f} J")

# Force needed (assuming frictionless)
force_needed = energy_required / ramp_distance
print(f"Force needed: {force_needed:.2f} N")
```

## Rotational Motion

### Angular Velocity and Acceleration

```python
# Convert between linear and angular velocity
def linear_to_angular(linear_vel, radius):
    """ω = v / r"""
    return linear_vel / radius

def angular_to_linear(angular_vel, radius):
    """v = ω * r"""
    return angular_vel * radius

# Example: Wheel rotation
wheel_radius = 0.1  # meters
linear_velocity = 2.0  # m/s

angular_velocity = linear_to_angular(linear_velocity, wheel_radius)
print(f"Wheel angular velocity: {angular_velocity:.2f} rad/s")
print(f"Wheel RPM: {angular_velocity * 60 / (2 * np.pi):.2f}")
```

### Torque and Moment of Inertia

```python
# Torque = Force × Distance
def calculate_torque(force, lever_arm):
    """τ = F × r"""
    return force * lever_arm

# Rotational Newton's Law: τ = I * α
def angular_acceleration(torque, moment_of_inertia):
    """α = τ / I"""
    return torque / moment_of_inertia

# Example: Robot arm rotation
force = 50  # N
arm_length = 0.5  # m
torque = calculate_torque(force, arm_length)
print(f"Torque: {torque} N⋅m")

# Moment of inertia for rod rotating about end
mass = 5  # kg
I = (1/3) * mass * arm_length**2
alpha = angular_acceleration(torque, I)
print(f"Angular acceleration: {alpha:.2f} rad/s²")
```

## Center of Mass and Stability

```python
def center_of_mass(masses, positions):
    """
    Calculate center of mass for multiple point masses.

    Args:
        masses: Array of masses
        positions: Array of position vectors

    Returns:
        Center of mass position
    """
    total_mass = np.sum(masses)
    weighted_sum = sum(m * p for m, p in zip(masses, positions))
    return weighted_sum / total_mass

# Example: Humanoid robot balance
masses = np.array([10, 5, 5, 30, 15, 15])  # kg (head, arms, torso, legs)
positions = np.array([
    [0, 0, 1.6],    # Head
    [-0.3, 0, 1.2], # Left arm
    [0.3, 0, 1.2],  # Right arm
    [0, 0, 0.8],    # Torso
    [-0.1, 0, 0.4], # Left leg
    [0.1, 0, 0.4]   # Right leg
])

com = center_of_mass(masses, positions)
print(f"Center of mass: {com}")
```

## Simulation Basics

### Simple Physics Simulation

```python
class RobotSimulation:
    """Simple 1D robot simulation with physics."""

    def __init__(self, mass, position=0, velocity=0):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.time = 0
        self.dt = 0.01  # Time step (10ms)

    def apply_force(self, force):
        """Apply force and update state."""
        # F = ma → a = F/m
        acceleration = force / self.mass

        # Update velocity and position (Euler integration)
        self.velocity += acceleration * self.dt
        self.position += self.velocity * self.dt
        self.time += self.dt

    def simulate(self, force, duration):
        """Run simulation for specified duration."""
        trajectory = []
        steps = int(duration / self.dt)

        for _ in range(steps):
            self.apply_force(force)
            trajectory.append({
                'time': self.time,
                'position': self.position,
                'velocity': self.velocity
            })

        return trajectory

# Example: Robot accelerating
robot = RobotSimulation(mass=50)  # 50 kg robot
trajectory = robot.simulate(force=100, duration=5)  # 100 N for 5 seconds

# Extract positions
times = [p['time'] for p in trajectory]
positions = [p['position'] for p in trajectory]

plt.plot(times, positions)
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.title('Robot Motion Under Constant Force')
plt.grid(True)
```

## Practice Exercises

### Exercise 1: Stopping Distance

Calculate the stopping distance for a robot given initial velocity and deceleration:

```python
def stopping_distance(v0, deceleration):
    """
    Calculate stopping distance.

    v^2 = v0^2 + 2*a*d
    When v = 0: d = -v0^2 / (2*a)
    """
    # Your code here
    pass
```

### Exercise 2: Pendulum Simulation

Simulate a simple pendulum (useful for understanding bipedal walking):

```python
def pendulum_angle(theta0, t, L=1.0, g=9.81):
    """
    Calculate pendulum angle at time t.

    Small angle approximation: θ(t) = θ0 * cos(ω*t)
    where ω = sqrt(g/L)
    """
    # Your code here
    pass
```

### Exercise 3: Two-Wheel Robot Kinematics

Given wheel velocities, calculate robot velocity:

```python
def differential_drive_kinematics(v_left, v_right, wheel_base):
    """
    Calculate robot linear and angular velocity.

    Args:
        v_left: Left wheel velocity (m/s)
        v_right: Right wheel velocity (m/s)
        wheel_base: Distance between wheels (m)

    Returns:
        (linear_velocity, angular_velocity)
    """
    # Your code here
    # linear = (v_left + v_right) / 2
    # angular = (v_right - v_left) / wheel_base
    pass
```

## Key Takeaways

- ✅ Kinematics describes motion (position, velocity, acceleration)
- ✅ Dynamics relates forces to motion (F = ma)
- ✅ Energy conservation guides efficient robot design
- ✅ Rotational motion is essential for wheels and joints
- ✅ Center of mass determines stability
- ✅ Simulation validates designs before hardware

## Next Lesson

Continue to [Stage 1 Assessment](./assessment) to test your knowledge and unlock Stage 2!

## Additional Resources

- [Physics for Game Developers](https://www.oreilly.com/library/view/physics-for-game/9781449361037/)
- [Classical Mechanics (MIT OpenCourseWare)](https://ocw.mit.edu/courses/physics/8-01sc-classical-mechanics-fall-2016/)
- [PyBullet Documentation](https://pybullet.org/wordpress/)
