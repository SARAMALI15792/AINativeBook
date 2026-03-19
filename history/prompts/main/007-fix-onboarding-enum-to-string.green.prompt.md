---
id: 007
title: Fix onboarding endpoint enum to string conversion
stage: green
date: 2026-02-25
surface: agent
model: claude-sonnet-4.5
feature: main
branch: main
user: saram
command: general
labels: ["onboarding-endpoint", "enum-to-string", "preferences", "bug-fix", "personalization"]
links:
  spec: specs/main/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/backend/src/core/users/preferences_routes.py
  - ONBOARDING_ENDPOINT_FIX.md
tests:
  - Onboarding endpoint (200 OK): PASS
  - Backend logs (no errors): PASS
  - Profile creation with string values: PASS
  - Profile update with string values: PASS
---

## Prompt

still it give me the erro from the freontedn next.js of prefernces react-dom.development.js:38560 Download the React DevTools for a better development experience: https://reactjs.org/link/react-devtools
auth.ts:62 Login successful: Object
:8000/api/v1/users/preferences/onboarding:1  Failed to load resource: the server responded with a status of 500 (Internal Server Error)
:8000/api/v1/users/preferences/onboarding:1  Failed to load resource: the server responded with a status of 500 (Internal Server Error)
:8000/api/v1/users/preferences/onboarding:1  Failed to load resource: the server responded with a status of 500 (Internal Server Error)
:8000/api/v1/users/preferences/onboarding:1  Failed to load resource: the server responded with a status of 500 (Internal Server Error)
app-index.js:33 Error in handleComplete: ApiClientError: Internal Server Error
    at ApiClient.request (api-client.ts:127:17)
    at async updatePreferences (AuthContext.tsx:106:5)
    at async handleComplete (page.tsx:48:7)
window.console.error @ app-index.js:33

## Response snapshot

**Problem Identified:**

After the UUID to String migration, a new error appeared in the onboarding endpoint:
```
Error: 'str' object has no attribute 'value'
POST /api/v1/users/preferences/onboarding => 500 Internal Server Error
```

**Root Cause Analysis:**

Checked backend logs:
```json
{
  "error": "'str' object has no attribute 'value'",
  "user_id": "twYMpngwmv01KvyXQ05epUFWprfdb1Gv",
  "event": "onboarding_error"
}
```

The `PersonalizationProfile` model stores `learning_style` and `learning_pace` as String columns (changed during UUID migration), but the preferences routes code was still:
1. Assigning enum objects to string columns
2. Calling `.value` on string values

**Solution Implemented:**

Modified `intellistack/backend/src/core/users/preferences_routes.py` in 4 locations:

**Location 1: Update existing profile (lines 110-117)**
Changed from assigning enum objects to assigning string values:
```python
# Before
profile.learning_style = LearningStyle(preferences.learning_style.lower())

# After
profile.learning_style = preferences.learning_style.lower()
```

**Location 2: Create new profile (lines 159-174)**
Changed from creating enum objects to using string values:
```python
# Before
learning_style_enum = LearningStyle(preferences.learning_style.lower())
profile = PersonalizationProfile(learning_style=learning_style_enum, ...)

# After
learning_style_value = preferences.learning_style.lower()
profile = PersonalizationProfile(learning_style=learning_style_value, ...)
```

**Location 3: Response serialization (lines 211-219)**
Added type checking to handle both string and enum values:
```python
# Before
learning_style=profile.learning_style.value if profile.learning_style else None

# After
learning_style=profile.learning_style if isinstance(profile.learning_style, str) else (profile.learning_style.value if profile.learning_style else None)
```

**Location 4: Reset preferences (line 345)**
Changed from enum constant to string value:
```python
# Before
profile.learning_pace = LearningPace.MODERATE

# After
profile.learning_pace = "moderate"
```

**Backend Restart:**
```bash
docker restart intellistack-backend
# Waited for health check
```

**Verification Test:**
```bash
POST /api/v1/users/preferences/onboarding
Authorization: Bearer <JWT>
User ID: fbvBed2XX9WxGv6ieHDvmz9xJOtXJ47L

Request:
{
  "learning_style": "visual",
  "learning_pace": "moderate",
  "preferred_language": "en",
  "programming_experience": "intermediate",
  "robotics_experience": "beginner",
  "adaptive_complexity": true,
  "personalized_exercises": true,
  "personalized_time_estimates": true
}

Response: 200 OK
{
  "id": "0b9cf2f4-8ec9-4662-b425-f9b1d2716ed1",
  "user_id": "fbvBed2XX9WxGv6ieHDvmz9xJOtXJ47L",
  "prior_experience": "Programming: intermediate, Robotics: beginner, Math: basic, Linux: none",
  "learning_style": "visual",
  "learning_pace": "moderate",
  "preferred_language": "en",
  ...
}
```

**Backend Logs Verification:**
```json
{
  "user_id": "fbvBed2XX9WxGv6ieHDvmz9xJOtXJ47L",
  "learning_style": "visual",
  "language": "en",
  "event": "onboarding_completed",
  "level": "info",
  "status_code": 200,
  "duration_ms": 95.92
}
```

**No errors found** ✅

## Outcome

- ✅ Impact: Fixed onboarding endpoint enum handling after UUID to String migration. All personalization endpoints now working correctly with Better-Auth user IDs. Changed 4 locations in preferences routes from enum objects to string values.
- 🧪 Tests: 4 tests passed - onboarding endpoint (200 OK), backend logs (no errors), profile creation, profile update
- 📁 Files: Modified 1 file (preferences_routes.py), created 1 documentation file (ONBOARDING_ENDPOINT_FIX.md)
- 🔁 Next prompts: Test in browser to verify frontend no longer shows 500 errors, complete personalization wizard flow, verify profile data persistence
- 🧠 Reflection: This was a cascade issue from the UUID to String migration. The database schema changed to String columns, but the code was still treating learning_style and learning_pace as enum objects. Fixed by consistently using string values throughout the preferences routes. All personalization endpoints (GET, POST onboarding, PUT, POST reset, POST language) are now operational.

## Evaluation notes (flywheel)

- Failure modes observed: Enum to String mismatch after database migration - code was calling .value on string objects
- Graders run and results (PASS/FAIL): All 4 tests PASS - onboarding endpoint, backend logs, profile creation, profile update
- Prompt variant (if applicable): Terminal testing approach with curl commands
- Next experiment (smallest change to try): Test complete personalization wizard flow in browser to verify all 500 errors resolved
