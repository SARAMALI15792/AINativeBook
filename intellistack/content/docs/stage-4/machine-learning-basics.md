---
id: machine-learning-basics
title: Machine Learning for Robotics
sidebar_label: ML Basics
sidebar_position: 2
---

# Machine Learning for Robotics

Machine learning enables robots to learn from data and improve their performance over time. This lesson introduces ML concepts applied to robotics.

## Supervised Learning for Perception

```python
import torch
import torch.nn as nn
import torch.optim as optim

class GripperClassifier(nn.Module):
    """Classify if gripper should open or close based on object size."""

    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(3, 64)  # Input: [width, height, depth]
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 2)   # Output: [open, close]
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# Training loop
model = GripperClassifier()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training data: [width, height, depth] → label
X_train = torch.tensor([[0.1, 0.1, 0.1], [0.3, 0.3, 0.3]])
y_train = torch.tensor([1, 0])  # 1=close, 0=open

for epoch in range(100):
    optimizer.zero_grad()
    outputs = model(X_train.float())
    loss = criterion(outputs, y_train)
    loss.backward()
    optimizer.step()
```

## Reinforcement Learning

```python
import gym
import numpy as np

# Q-Learning for robot navigation
class QLearningAgent:
    def __init__(self, states, actions, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.q_table = np.zeros((states, actions))
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate

    def choose_action(self, state):
        """Epsilon-greedy action selection."""
        if np.random.random() < self.epsilon:
            return np.random.randint(self.q_table.shape[1])
        return np.argmax(self.q_table[state])

    def update(self, state, action, reward, next_state):
        """Update Q-value."""
        best_next = np.max(self.q_table[next_state])
        td_target = reward + self.gamma * best_next
        td_error = td_target - self.q_table[state, action]
        self.q_table[state, action] += self.alpha * td_error
```

## Key Takeaways

- ✅ Supervised learning for perception tasks
- ✅ Reinforcement learning for control policies
- ✅ Simulation provides unlimited training data
- ✅ Transfer learning bridges simulation to reality

## Next Lesson

Continue to [Sim-to-Real Transfer](./sim-to-real) to deploy your models on real robots!
