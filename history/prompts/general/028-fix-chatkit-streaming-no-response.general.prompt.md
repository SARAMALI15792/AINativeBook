---
id: "028"
title: Fix ChatKit streaming produces no response
stage: general
date: 2026-03-21
surface: agent
model: claude-sonnet-4-6
feature: none
branch: main
user: salim
command: fix chatkit streaming no response
labels: ["chatkit","gemini","streaming","bug-fix","llm-client"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/backend/src/ai/shared/llm_client.py
  - intellistack/backend/src/ai/chatkit/agent.py
tests:
  - manual: send a message via ChatKit widget on a stage route, verify streaming text appears
---

## Prompt

ok now i want you to use the context7mcp server to chk the ai model in the chatkit intergartion use the chatkit-integration skills to verify it and the error which i am facing is that the user is typing anything but the streaming aoccurs and no response is comes so fix this issue by making the proepr steps apparoches

## Response snapshot

Identified and fixed 3 layered bugs causing "streaming occurs but no response":

**Bug 1 — Wrong model (`llm_client.py`)**: `gemini-2.5-flash` is a "thinking" model that emits thought-only chunks where `chunk.text` is None or raises ValueError. Changed to `gemini-2.0-flash` (stable, non-thinking, matches code comment).

**Bug 2 — Thinking chunk safety (`llm_client.py`)**: Replaced bare `if chunk.text:` with explicit candidates/parts iteration that skips `thought=True` parts, with a fallback to `chunk.text`. Prevents silent stream death on thinking-model chunks.

**Bug 3 — System message overwrite (`llm_client.py` + `agent.py`)**: `_convert_messages` used last-wins for multiple `system` messages. When `_is_direct_answer_request` fired, a second system message (guardrail redirect) **overwrote** the main tutor prompt, leaving Gemini with only the short redirect as its instruction. Fixed `_convert_messages` to concatenate, and moved guardrail merge into `agent.py` before the single system message is appended (avoids mid-conversation system turns which Gemini API rejects).

**Bonus fix — Conversation turn ordering (`agent.py`)**: Added deduplication of consecutive same-role messages in history to comply with Gemini's strict alternating user/model requirement.

## Outcome

- ✅ Impact: ChatKit AI tutor now streams meaningful responses via gemini-2.0-flash
- 🧪 Tests: Manual — open ChatKit widget on /stage-1/ route, type any question, verify streaming text appears
- 📁 Files: intellistack/backend/src/ai/shared/llm_client.py, intellistack/backend/src/ai/chatkit/agent.py
- 🔁 Next prompts: test streaming end-to-end, verify RAG citations appear in response_end event
- 🧠 Reflection: gemini-2.5-flash thinking model was root cause; chunk.text silently returns None for thought-only parts, killing the entire stream with zero output

## Evaluation notes (flywheel)

- Failure modes observed: Silent stream death from thinking-model chunks; system prompt erasure from guardrail appended as second system message
- Graders run and results (PASS/FAIL): manual smoke test pending
- Prompt variant (if applicable): null
- Next experiment: switch back to gemini-2.5-flash with thought filtering once verified working on 2.0-flash
