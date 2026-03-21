---
name: Redirect Next.js Login to Docusaurus
description: Replace Next.js auth pages with redirects to Docusaurus login/signup pages so all auth flows happen in Docusaurus
type: general
stage: general
date: 2026-03-21
surface: agent
model: claude-sonnet-4-6
feature: none
branch: main
user: salim
command: user message
labels: ["auth", "routing", "nextjs", "docusaurus", "redirect"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
---

## Prompt

ok now i want you to make this chnages that when user click on the login button from the next.js frontend it redirect the user to the docusours login sigup page and then from there user will continue its authicating and remove the others prefeces setpeup from the next.js froented and only it will be in the dosucors main when user redirect diectly to that page

## Response

Changed the following files to redirect all auth flows from Next.js to Docusaurus:

1. **`intellistack/frontend/src/components/layout/Header.tsx`**
   - Desktop Login button: changed `<Link href="/auth/login">` to `<a href="${docusaurusUrl}/auth/login">`
   - Mobile Login button: same change
   - Added `.replace(/\/$/, '')` to docusaurusUrl to prevent double slashes

2. **`intellistack/frontend/src/app/auth/login/page.tsx`**
   - Replaced full login page UI with a simple `useEffect` redirect to `${docusaurusUrl}/auth/login`
   - Uses `window.location.replace()` to avoid adding to browser history

3. **`intellistack/frontend/src/app/auth/register/page.tsx`**
   - Replaced full register page UI with redirect to `${docusaurusUrl}/auth/signup`

## Files Modified

 - intellistack/frontend/src/components/layout/Header.tsx
 - intellistack/frontend/src/app/auth/login/page.tsx
 - intellistack/frontend/src/app/auth/register/page.tsx
