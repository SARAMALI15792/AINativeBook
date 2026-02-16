---
id: 2-4-coordinate-frames
title: "2.4 The Relativity of Space"
sidebar_label: "2.4 TF2 & Transforms"
description: "The Transform Tree, Frame Conventions, and Einstein for Robots."
---

# 2.4 The Relativity of Space
**Stage II: The Graph**

> "Where am I? The answer depends entirely on who you ask."

## 1. The Transform Tree (TF)

The robot is a collection of rigid bodies connected by joints.
Every sensor measures data in its own coordinate frame.
*   **Camera Frame**: Z is forward (Optical).
*   **Base Frame**: X is forward (Mechanical).
*   **Map Frame**: Inertial World Frame.

**The Problem**: If the Camera sees an obstacle at (3, 0, 1), where is that obstacle relative to the Wheels?
**The Solution**: The Transform Tree. A distributed graph of frame relationships published by `robot_state_publisher`.

$$ ^{base}P = ^{base}T_{camera} \times ^{camera}P $$

---

## 2. Standard Frames (REP-105)

To make robots interoperable, we agree on a standard hierarchy:

1.  **map**: Fixed world frame. Z points up. Discontinuous (can jump if loop closure happens). Use for long-term planning.
2.  **odom**: Continuous world frame. Smooth local navigation. Drifts over time. Use for PID control.
3.  **base_link**: The robot's center of mass.
4.  **sensor_link**: Attached to the robot.

**The Golden Rule**:
*   **Localization**: Computes `map` $\to$ `odom`.
*   **Odometry**: Computes `odom` $\to$ `base_link`.
*   **State Publisher**: Computes `base_link` $\to$ `sensor_link`.

---

## 3. Time Travel (The Buffer)

TF is not just spatial; it is temporal.
"Where was the camera relative to the map **50ms ago** when this image was taken?"

The `tf2_ros` buffer stores the last 10 seconds of transforms.
When you ask for a transform, you must specify the **Time**.
`buffer.lookup_transform("map", "camera", time_of_image)`

If you ask for `Time.now()`, you will fail.
Why? Because `Time.now()` hasn't happened yet in the TF buffer (latency). You must ask for `Time(0)` (latest available) or specific timestamp.

---

## Deep FAQ

> **Q: Why does my TF tree break?**
> A: It usually breaks because of **Timestamp Mismatch**. If your computer clock and the robot clock drift by 1 second, TF will reject lookups as "Extrapolation into the Future". Use Chrony/NTP to sync clocks.

> **Q: Static vs. Dynamic Transforms?**
> A:
> *   **Static**: Camera mount on chassis. Never moves. Published once (latched).
> *   **Dynamic**: Wheel rotation, Arm joint. Moves constantly. Published at 50Hz.
