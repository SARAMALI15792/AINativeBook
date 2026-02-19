---
id: 033
title: Debug ChatKit Streaming Bubble Issue
stage: refactor
date: 2026-02-17
surface: agent
model: claude-opus-4-6
feature: 001-intellistack-platform
branch: main
user: saram
command: none
labels: ["chatkit", "streaming", "debug", "sse", "bug-investigation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/content/src/components/ai/ChatKitWidget.tsx
  - CHATKIT_STREAMING_DEBUG.md
tests:
  - Manual testing required: Send message and check browser console
---

## Prompt

now the streaming buble is also not shown .in chatkit

## Response snapshot

Added comprehensive debug logging to investigate why the ChatKit streaming bubble isn't appearing.

**Investigation:**

1. **Checked streaming logic** - Frontend correctly parses SSE events and extracts `data.text`
2. **Verified backend format** - Backend sends proper SSE events with `event: chunk` and `data: {"text": "..."}`
3. **Reviewed CSS** - Streaming bubble styles exist and look correct
4. **Identified need for debugging** - Need to see actual console output to diagnose

**Debug Logging Added:**

1. **Request tracking:**
   - Log backend URL being called
   - Log request headers (including JWT)
   - Log response status

2. **SSE event tracking:**
   - Log each event type received (thread, message_saved, response_start, chunk, response_end)
   - Log event data payload
   - Log streaming chunks as they arrive
   - Log completion with message_id

3. **Error tracking:**
   - Log HTTP errors with response text
   - Log JSON parse failures
   - Warn on malformed SSE data

**Expected Flow:**
```
Sending message → Response 200 → thread event → message_saved event →
response_start event → chunk events (streaming!) → response_end event
```

**Possible Issues:**
1. Backend not sending chunk events
2. Frontend not receiving SSE stream
3. State updates not triggering re-render
4. CSS hiding the bubble
5. JWT authentication failing

**Next Steps:**
1. Restart frontend with debug logs: `cd intellistack/content && npm start`
2. Open browser console (F12)
3. Send a test message in ChatKit
4. Check console output against expected flow
5. Report findings for further diagnosis

**Files Created:**
- `CHATKIT_STREAMING_DEBUG.md` - Comprehensive debugging guide with troubleshooting steps

## Outcome

- ✅ Impact: Debug logging infrastructure in place to diagnose streaming issue
- 🧪 Tests: Manual testing required - need to see console output
- 📁 Files: 2 files modified (1 component, 1 documentation)
- 🔁 Next prompts: Test in browser, share console logs, identify failure point
- 🧠 Reflection: Without seeing actual runtime behavior, added instrumentation to make the issue visible

## Evaluation notes (flywheel)

- Failure modes observed: Streaming bubble not appearing, but root cause unknown without runtime logs
- Graders run and results (PASS/FAIL): Build: PARTIAL (MDX error unrelated to ChatKit), TypeScript: PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test with debug logs, check if SSE events are received, verify state updates
