---
id: 1-5-calculus-dynamics
title: "1.5 The Physics of Motion"
sidebar_label: "1.5 Calculus & Dynamics"
description: "Derivatives, Integrals, Numerical Integration (Euler/RK4), and Lagrangian Mechanics."
---

# 1.5 The Physics of Motion
**Stage I: The Substrate**

> "Calculus is the study of continuous change. Computers are the study of discrete steps. The bridge between them is where simulation lives."

## 1. The Derivative (Velocity)

Position: `x(t)`
Velocity: `v(t) = dx/dt`
Acceleration: `a(t) = dv/dt`

In a computer, we don't have $dt \to 0$. We have $\Delta t$ (Time Step).
`v[k] ≈ (x[k] - x[k-1]) / Δt`
This is the **Finite Difference**. It creates noise. A bumpy position sensor creates massive spikes in derivative-calculated velocity.

---

## 2. The Integral (Dead Reckoning)

`x(t) = ∫ v(t) dt`
In simulation: `x[k] = x[k-1] + v[k] · Δt`

### Drift (The Enemy)
Every integration adds a tiny error.
`Δt` is never perfect. `v[k]` has sensor noise.
**Error Accumulation**: A robot navigating purely by odometry (integrating wheel encoders) will eventually think it is in the next country. This is why we need **Loop Closure** (Stage III).

---

## 3. Numerical Integration

How do we simulate physics? We predict the future state based on the current state.

### Euler Method (First Order)
`x_new = x_old + v · Δt`
Simple. Fast. **Wrong**.
It assumes velocity is constant during the time step. It is not. It adds energy to the system (instability).

### Runge-Kutta 4 (RK4)
The gold standard. It samples the slope at 4 different points within the time step to get a weighted average.
It is computationally expensive but physically stable. Gazebo uses this.

---

## 4. Lagrangian Mechanics

Newton (`F = ma`) is hard for multi-joint arms. You have to calculate constraint forces at every joint pin.
Lagrange says: **Forget forces. Look at Energy.**

`L = T - V`
*   `T`: Kinetic Energy (Motion)
*   `V`: Potential Energy (Gravity/Springs)

**Euler-Lagrange Equation**:
`d/dt(∂L/∂q̇) - ∂L/∂q = 0`

This magic formula gives you the Equations of Motion for *any* robot, no matter how complex, purely by tracking energy. It is the heart of modern physics engines (Dart, MuJoCo).

---

## Deep FAQ

> **Q: Why does my simulation explode (robot flies to infinity)?**
> A: Likely the **Integration Step ($\Delta t$)** is too large. If the robot moves too far in one step, it might penetrate a wall. The physics engine applies a corrective "Spring Force" to push it out. If $\Delta t$ is large, this force is huge. Next step, it shoots past origin. It oscillates and gains infinite energy.

> **Q: What is a Jacobian?**
> A: It is a matrix of partial derivatives relating Joint Velocities (`q̇`) to End-Effector Velocities (`ẋ`). It tells you: "If I move joint 1 by a tiny bit, how much does the hand move?" Singularities occur when the Jacobian loses rank (Hand cannot move in a certain direction).
