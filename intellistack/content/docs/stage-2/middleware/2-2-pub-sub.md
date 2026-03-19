---
id: 2-2-pub-sub
title: "2.2 The Pub/Sub Ontology"
sidebar_label: "2.2 Middleware & QoS"
description: "DDS, IDL, Serialization, and the physics of message passing."
---

# 2.2 The Pub/Sub Ontology
**Stage II: The Graph**

> "Do not speak to the listener. Speak to the ether. If the listener is worthy, they will hear you."

## 1. The Middleware (DDS)

ROS 2 is built on top of **DDS (Data Distribution Service)**.
DDS is an industrial standard used in Battleships, Spacecraft, and Finance.
It is a **Data-Centric** architecture.
*   **Topic**: A named channel (e.g., `/camera/image_raw`).
*   **Type**: The schema (e.g., `sensor_msgs/Image`).
*   **Domain**: The virtual network (ID 0-100). Nodes on Domain 0 cannot see nodes on Domain 1.

### The IDL (Interface Definition Language)
Before we can talk, we must agree on grammar.
`.msg` files are language-agnostic.
`int32 x` becomes `int32_t` in C++ and `int` in Python.
The build system (`colcon`) generates these bindings.

---

## 2. Theoretical Quality of Service (QoS)

In TCP/IP (Web), we demand reliability. If a packet is lost, we retry.
In Robotics, **Reliability is sometimes failure.**

**Scenario**: You are driving at 100km/h.
*   **Reliable**: You miss a LIDAR packet. The system pauses to re-request it. By the time it arrives, it is 50ms old. You are now driving blind based on history.
*   **Best Effort**: You miss a packet. You ignore it. You process the *next* packet which is fresh.

**The QoS Policies**:
1.  **Reliability**: Reliable vs. Best Effort.
2.  **Durability**: Transient Local (History for late-joiners) vs. Volatile (Live only).
3.  **History**: Keep Last N.

**Golden Rule**:
> "Use Reliable for Commands (Stop!). Use Best Effort for Sensors (High Bandwidth)."

---

## 3. Serialization (The Alchemy)

How do you send a C++ Object over a wire?
You can't. You must **Serialize** it into a byte stream (CDR - Common Data Representation).
1.  **Struct Memory Layout**: Padding and alignment.
2.  **Endianness**: Little vs. Big Endian.
3.  **Zero Copy**: If both nodes are on the same shared memory, we just pass the *pointer*. This bypasses serialization entirely.

---

## Deep FAQ

> **Q: Why not use JSON?**
> A: JSON is slow. Parsing text takes CPU. CDR is binary and tightly packed. In a 1000Hz loop, JSON parsing would kill the latency budget.

> **Q: Can I subscribe to my own topic?**
> A: Yes, but be careful of infinite loops. If your callback publishes to the same topic it listens to, you create feedback screeches (like a microphone near a speaker).
