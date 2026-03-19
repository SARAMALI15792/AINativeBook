---
id: 2-3-services-actions
title: "2.3 The Request/Response"
sidebar_label: "2.3 Services & Actions"
description: "Synchronous RPC vs. Asynchronous Goal seeking."
---

# 2.3 The Request/Response
**Stage II: The Graph**

> "Sometimes, listening is not enough. You must demand an answer."

## 1. Services (The Blocking Call)

Pub/Sub is "Fire and Forget".
Services are "Ask and Wait".
**Client** $\rightarrow$ Request $\rightarrow$ **Server** $\rightarrow$ Response.

**The Danger**: Services are **Synchronous** by default in many minds.
If your Navigation Node calls `GetMap()` and the Map Server hangs for 5 seconds, your robot freezes.
**Rule**: Always call services Asynchronously (`call_async`).

---

## 2. Actions (The Long Game)

A Service is for "Quick questions" (e.g., "Is the gripper open?").
What if the question is "Drive to the Kitchen"?
That takes 5 minutes. You cannot block for 5 minutes.

**The Action Definition**:
1.  **Goal**: "Go to Kitchen". (Client $\to$ Server)
2.  **Feedback**: "I am 50% there... 60% there..." (Server $\to$ Client)
3.  **Result**: "I arrived." or "I hit a cat." (Server $\to$ Client)
4.  **Cancel**: "Stop! Abort!" (Client $\to$ Server)

This is a state machine over a network.

### The Action Server FSM
*   **Idle**
*   **Goal Received**
*   **Executing**
*   **Succeeded / Aborted / Canceled**

---

## 3. The Threading Model

ROS 2 Actions run in a **Multi-Threaded Executor** by default.
Why? Because while the robot is "Driving" (Executing), it must still listen for "Cancel" messages.
If it were single-threaded, it would be deaf while driving.

---

## Deep FAQ

> **Q: When to use Service vs Action?**
> A: Only use Service if the computation takes less than 10ms. If it involves physical motion, it MUST be an Action.

> **Q: Can an Action be Preempted?**
> A: Yes. If a new Goal arrives while one is executing, the Server policy decides: Reject new, or Abort old and Accept new.
