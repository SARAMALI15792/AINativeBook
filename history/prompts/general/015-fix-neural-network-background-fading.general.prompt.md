---
id: 015
title: Fix Neural Network Background Lines Fading
stage: general
date: 2026-03-20
surface: agent
model: claude-sonnet-4-6
feature: none
branch: main
user: salim
command: fix neural network background animation disappearing after a few seconds
labels: ["bug","animation","canvas","ui","neural-network"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/frontend/src/components/effects/NeuralNetworkBackground.tsx
tests:
  - manual: Neural network lines remain visible indefinitely on homepage
  - manual: Mobile SVG lines also remain visible
---

## Prompt

When the website loads it shows the interface super cool for a few seconds and removes the lines from the website background.

## Response snapshot

Root cause: The canvas "clear" used `ctx.fillStyle = 'rgba(10, 15, 30, 0.1)'; ctx.fillRect(...)` — a trail technique that layers 10% opacity dark overlay each frame. At 60fps, after ~1 second the accumulated opacity reaches 99.8%, creating a solid dark rectangle. Nodes drawn at 15% opacity and connections at 4–16% opacity become invisible against it.

Fixes:
1. Replaced `fillRect` trail with `ctx.clearRect(0, 0, canvas.width, canvas.height)` — canvas clears fully every frame, nodes/connections stay permanently visible
2. Raised node opacity: outer glow 12%, bright core 70% (was flat 15%)
3. Raised connection opacity: 15–55% range (was 4–16%)
4. Increased desktop node count 30→50, connections 60→80 for denser network
5. Fixed mobile SVG stroke/fill opacity to match (was 0.15, now stroke=1 with per-conn opacity, fill=0.7)

## Outcome

- ✅ Impact: Animation stays visible for the full session — never fades
- 🧪 Tests: Visual check in browser
- 📁 Files: 1 file modified
- 🔁 Next prompts: Could add distance-based connection opacity (nearby nodes = brighter lines)
- 🧠 Reflection: Semi-transparent fill as "clear" is a common canvas trail pattern — it only works when content opacity is HIGH relative to the fill opacity. Here content was far too faint.

## Evaluation notes (flywheel)

- Failure modes observed: trail fill accumulating to solid black over content drawn at invisible opacity
- Graders run and results (PASS/FAIL): not run
- Prompt variant (if applicable): none
- Next experiment: Add distance-based opacity (connections only drawn if nodes are within threshold distance)
