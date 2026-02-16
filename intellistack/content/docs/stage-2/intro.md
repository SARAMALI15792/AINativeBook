---
id: intro
title: "Stage 2 - The Graph"
sidebar_label: "Introduction"
sidebar_position: 1
---

# Stage 2: The Graph (Information Flow)

<div className="stage-badge stage-2">Stage 2</div>

> "Before a robot can perceive, it must communicate. We build the nervous system before the eyes."

## The Philosophy of Stage II

In Stage I, we built the **Substrate**—the ability to execute code (Processes) and define math (Linear Algebra).
In Stage II, we solve the **Distributed State Problem**.

A robot is not a single program. It is a distributed system of independent nodes—sensors, actuators, planners—that must agree on a shared reality in real-time.
This agreement is mediated by **The Graph**.

## Learning Objectives

In this Deep Dive, you will master:

1.  **The Distributed Mind**: Understanding Nodes as independent cognitive units in a graph.
2.  **The Pub/Sub Ontology**: The physics of Middleware (DDS), Quality of Service (QoS), and Serialization.
3.  **Service & Action Theory**: Synchronous vs. Asynchronous patterns for robot behavior invocation.
4.  **The Relativity of Space (TF2)**: Managing the geometric relationship between sensor frames and world frames using the Transform Tree.

## Chapter Map

*   **2.1 The Distributed Mind**: Graph Theory & CAP Theorem.
*   **2.2 The Pub/Sub Ontology**: Middleware & QoS.
*   **2.3 The Request/Response**: Services & Actions.
*   **2.4 The Relativity of Space**: TF2 & Transforms.

Prepare to abandon the idea of a "Main Loop". Welcome to the Event-Driven World.
