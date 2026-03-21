---
id: 04
title: Quota Error Fallback Response
stage: green
date: 2026-03-22
surface: agent
model: claude-sonnet-4-6
feature: 002-better-auth-chatkit
branch: main
user: salim
command: inline conversation
labels: ["error-handling","chatkit","gemini","ux","fallback"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/backend/src/ai/chatkit/agent.py
tests:
  - manual: trigger 429 from Gemini and observe fallback message in chat UI
---

## Prompt

ok now here when i want to converate to the chatkit it shows me this message so i want to tackle this message so can u tackle this message by talking to the user about the book and a summary and about some concepts and when the api key gets stable then will use the models response:
[full 429 RESOURCE_EXHAUSTED error from gemini-2.0-flash]

## Response snapshot

Modified `SocraticTutorAgent.generate_response()` in `agent.py` to:
1. Detect `RESOURCE_EXHAUSTED` / `429` / `quota` keywords in the exception string.
2. Call new `_quota_fallback_response()` async generator instead of exposing the raw API error.
3. `_quota_fallback_response` does keyword matching on the user's original message and yields a contextually relevant educational reply covering ROS 2, AI integration, Linux/Bash, or a generic platform overview table.
4. Non-quota errors yield a short neutral message.

## Outcome

- ✅ Impact: Students see helpful book content instead of a raw JSON API error during quota exhaustion
- 🧪 Tests: Manual — send a message while GEMINI_API_KEY is exhausted and confirm fallback renders
- 📁 Files: intellistack/backend/src/ai/chatkit/agent.py
- 🔁 Next prompts: Upgrade Gemini plan or add OpenAI fallback provider
- 🧠 Reflection: Keyword-matching fallback is intentionally simple; a smarter routing approach could use the user's stage number to target even more relevant content

## Evaluation notes (flywheel)

- Failure modes observed: none in this session
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): add retry-after countdown to fallback message using the retryDelay from the error details
