---
id: 2-1-distributed-mind
title: "2.1 The Distributed Mind"
sidebar_label: "2.1 Graph Theory"
description: "Nodes, Edges, and the CAP Theorem in Robotics."
---

# 2.1 The Distributed Mind
**Stage II: The Graph**

> "A robot is not a singular entity. It is a choir."

## 1. The Distributed State Problem

In Stage I, we learned about the **Process** (Chapter 1.1).
Now, imagine we have 50 processes.
*   Process A reads the Camera.
*   Process B controls the Wheels.
*   Process C maps the room.

How does Process A tell Process C that it saw a wall?
If Process A calls `ProcessC.add_wall()`, they are **Coupled**. If Process C crashes, Process A crashes.
This is a Monolith. Monoliths die.

### The Solution: The Graph
We treat every process as a **Node** in a directed graph.
Nodes do not know each other. They only know **Topics** (Edges).

$$ G = (V, E) $$
*   $V$: The set of Nodes (Computing Units)
*   $E$: The set of Topics (Data Streams)

---

## 2. Distributed Consistency (CAP Theorem)

In a distributed system, you can only have 2 of the 3:
1.  **Consistency**: Everyone sees the same data at the same time.
2.  **Availability**: The system always responds to requests.
3.  **Partition Tolerance**: The system survives network cuts.

**Robotics Choice**: We usually sacrifice **Consistency** for Availability.
If the LIDAR node sends data, the Mapping node might receive it 10ms late. That's fine. We tolerate **Eventual Consistency**.
But if the robot drives into a wall because the Stop command didn't arrive, that's bad.
This is why ROS 2 uses **DDS (Data Distribution Service)**.

---

## 3. The Node Lifecycle

A Node is not just a `while True` loop. It has a lifecycle.
1.  **Unconfigured**: Born, but empty.
2.  **Inactive**: Configured (params loaded), but asleep.
3.  **Active**: Processing data.
4.  **Finalized**: Dead.

**Deep Concept**: **Managed Nodes**.
In ROS 2, a "System Manager" can tell a Driver Node: "Go to Sleep", and it stops publishing. This saves CPU/Battery without killing the process.

---

## Deep FAQ

> **Q: Why not use Shared Memory?**
> A: We do! ROS 2 has "Zero Copy" transport (Iceoryx) for nodes on the same machine. But the *abstraction* remains Pub/Sub so that if we move the Node to a different computer over Wi-Fi, the code doesn't change.

> **Q: What is a Discovery Storm?**
> A: When 100 nodes wake up at once, they all shout "I am here!" via Multicast. This can flood the network switch. This is why we use **Discovery Servers** in large fleets.
