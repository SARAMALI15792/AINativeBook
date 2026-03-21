---
id: 021
title: ChatKit Gemini Streaming Integration Fix
stage: green
date: 2026-03-20
surface: agent
model: claude-sonnet-4-6
feature: chatkit
branch: 001-intellistack-platform
user: salim
command: implement plan
labels: ["chatkit","gemini","rag","streaming","bugfix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/backend/src/ai/chatkit/agent.py
  - intellistack/backend/src/ai/chatkit/server.py
tests:
  - manual: POST /api/v1/chatkit/stream returns SSE chunks from Gemini
  - manual: response_end event contains "sources" key with RAG citations
---

## Prompt

Implement the following plan:

# Plan: ChatKit + RAG + Google Gemini Streaming Integration

When users ask questions through ChatKit, answers must come from the book content via RAG retrieval and stream back using Google Gemini (`gemini-2.5-flash`). The RAG pipeline is fully wired (HybridRetriever → ChatKit → SocraticTutorAgent), but `_stream_response()` in `agent.py` bypasses Gemini entirely and calls **OpenAI** instead.

Root causes: wrong model param, `import openai` in _stream_response, broken metadata field lookups on RetrievalResult, non-existent guardrail method, dead Agent instantiation, wrong model name in server metadata, citations never sent to client.

## Response snapshot

Fixed all 8 defects across agent.py and server.py:

1. Added `from src.ai.shared.llm_client import LLMClient` import; removed `Agent, Runner` from agents import
2. Replaced `model: str = "gpt-4o"` with `llm_client: Optional[LLMClient] = None`; added `self._last_citations: List[Dict[str, Any]] = []`
3. Fixed `generate_response()`: reset `_last_citations` at top, built citations using `r.stage_name`, `r.content_title`, `r.text[:200]`, `r.score`
4. Fixed `_format_rag_results()`: replaced `result.metadata.get("source")` / `result.metadata.get("stage")` with `result.stage_name`, `result.content_title`
5. Fixed guardrail call: replaced `SocraticGuardrails.get_redirect_response()` with `SocraticGuardrails.generate_redirect_response(intent=IntentType.CONCEPT, original_request=user_message)`
6. Removed dead `Agent(name="SocraticTutor", ...)` instantiation block
7. Replaced `_stream_response()`: removed `import openai` / `AsyncOpenAI()`, now delegates to `self.llm_client.chat_completion_stream()`
8. `ChatKitTutorAgent.__init__` now creates `LLMClient()` and passes it to `SocraticTutorAgent`
9. `server.py` line ~369: `"model": "gpt-4o"` → `"model": "gemini-2.5-flash"`
10. `server.py` `response_end` event now includes `"sources": self.agent.tutor._last_citations`

## Outcome

- ✅ Impact: ChatKit now routes generation through Gemini 2.5 Flash; RAG citations surface to the client in response_end SSE event
- 🧪 Tests: Manual SSE endpoint test required; no automated tests modified
- 📁 Files: intellistack/backend/src/ai/chatkit/agent.py, intellistack/backend/src/ai/chatkit/server.py
- 🔁 Next prompts: Verify GEMINI_API_KEY in .env; test streaming endpoint end-to-end
- 🧠 Reflection: The `_convert_messages()` abstraction in LLMClient cleanly handles OpenAI→Gemini format translation, so agent.py needed no message format changes

## Evaluation notes (flywheel)

- Failure modes observed: OpenAI import bypassed Gemini entirely; metadata field lookups on RetrievalResult used wrong key names; non-existent guardrail method would have caused AttributeError at runtime
- Graders run and results (PASS/FAIL): Static verification PASS — `import openai` gone, `chat_completion_stream` present, `result.stage_name` used, `sources` in response_end
- Prompt variant (if applicable): null
- Next experiment: Add integration test that mocks LLMClient.chat_completion_stream and verifies SSE event sequence
