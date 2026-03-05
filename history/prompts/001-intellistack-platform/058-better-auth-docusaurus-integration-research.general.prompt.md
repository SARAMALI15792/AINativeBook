---
id: 058
title: Research Better Auth Integration Patterns for Docusaurus
stage: general
date: 2026-02-25
surface: agent
model: claude-sonnet-4.5
feature: 001-intellistack-platform
branch: main
user: saram
command: research
labels: ["better-auth", "docusaurus", "authentication", "integration", "research", "documentation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - BETTER_AUTH_DOCUSAURUS_INTEGRATION.md
tests:
  - None (research task)
---

## Prompt

Research and document the following technical decisions for implementing Better Auth authentication within a Docusaurus application:

1. **Better Auth Client Integration in Docusaurus**:
   - How to integrate Better Auth client library in Docusaurus (React-based static site generator)
   - Webpack configuration needed for Better Auth imports
   - Client module initialization patterns in Docusaurus
   - Session management and cookie handling in Docusaurus context

2. **Docusaurus Custom Pages for Auth**:
   - Best practices for creating custom React pages in Docusaurus (outside docs structure)
   - Routing configuration for /auth/login, /auth/signup, /onboarding/* pages
   - How to bypass Docusaurus's default doc-centric routing for auth pages

3. **Docusaurus Custom Navbar Components**:
   - How to create custom navbar items that show/hide based on authentication state
   - Swizzling vs custom components for auth-aware navigation
   - Best practices for integrating React state management in Docusaurus navbar

4. **Protected Routes in Docusaurus**:
   - Patterns for protecting content routes in Docusaurus
   - Client-side route guards and redirects
   - Handling SSR/SSG with authentication checks

5. **Cross-Origin Session Management**:
   - Cookie configuration for same-domain different-path deployment (e.g., / and /AINativeBook/)
   - Session validation patterns in Docusaurus client-side code
   - Handling session expiration and refresh in static site context

Provide concrete recommendations with code patterns and configuration examples. Focus on production-ready approaches that work with Docusaurus v3.x and Better Auth latest version.

## Response snapshot

Conducted comprehensive research using Context7 documentation for Better Auth and Docusaurus, analyzed existing implementation in the IntelliStack codebase, and compiled findings into a detailed technical documentation.

### Key Research Areas Covered:

1. **Better Auth Client Integration**
   - Lazy singleton pattern with Proxy for safe module-scope imports
   - Custom fetch implementation for graceful degradation
   - ExecutionEnvironment guards for client-only execution
   - Webpack configuration with resolve aliases

2. **Custom Pages Implementation**
   - Dynamic import pattern for auth client
   - Layout wrapper usage with @theme/Layout
   - Return URL preservation for post-login redirects
   - OAuth flow handling with Better Auth social providers

3. **Custom Navbar Components**
   - Component registration via swizzled ComponentTypes
   - BrowserOnly wrapper to prevent SSR hydration mismatches
   - AuthContext provider for centralized state management
   - Custom event system for cross-component synchronization

4. **Protected Routes Pattern**
   - useEffect-based client-side redirects
   - Loading states to prevent content flash
   - DocPage layout swizzling for protecting documentation
   - Path-based authentication requirements

5. **Cross-Origin Session Management**
   - Cookie configuration for different deployment scenarios
   - SameSite attribute handling (Lax vs None)
   - Cross-subdomain cookie sharing patterns
   - JWT token exchange for backend API authentication

### Documentation Deliverable:

Created comprehensive technical document: `BETTER_AUTH_DOCUSAURUS_INTEGRATION.md`

**Contents:**
- 6 major sections with detailed implementation patterns
- Code examples for all integration points
- Production deployment considerations
- Security best practices
- Implementation checklist
- Anti-patterns to avoid
- Complete reference architecture

**Key Patterns Documented:**
- Lazy Singleton + Proxy pattern for auth client
- BrowserOnly wrapper for SSR compatibility
- Custom event-based state synchronization
- useEffect redirect pattern for protected routes
- JWT exchange pattern for backend authentication
- Cookie configuration for various deployment scenarios

### Technical Insights:

1. **SSR/SSG Constraints**: Docusaurus pre-renders at build time, requiring careful client-side auth checks
2. **Environment Variables**: Build-time only; client reads from `window.__DOCUSAURUS__`
3. **Cookie Sharing**: Different strategies for same-domain, cross-subdomain, and cross-origin
4. **Session vs JWT**: Better Auth uses opaque session IDs; JWT plugin generates signed tokens for backend
5. **Graceful Degradation**: Auth server unavailability shouldn't crash the site

### Implementation Status:

The IntelliStack codebase already implements most of these patterns:
- ✅ Lazy singleton auth client with Proxy
- ✅ AuthContext provider in Root.tsx
- ✅ Custom AuthNavbarItem component
- ✅ Protected route component
- ✅ Login/register pages with OAuth
- ✅ Client module initialization
- ✅ JWT token exchange function

### Production Readiness:

Documented patterns are production-ready and include:
- CORS configuration
- Security headers
- Error tracking integration points
- Bundle optimization strategies
- Monitoring recommendations

## Outcome

- ✅ Impact: Comprehensive technical documentation created for Better Auth + Docusaurus integration
- 🧪 Tests: None (research and documentation task)
- 📁 Files: Created BETTER_AUTH_DOCUSAURUS_INTEGRATION.md (6 sections, ~800 lines)
- 🔁 Next prompts: Implementation of any missing patterns, ADR for authentication architecture decisions
- 🧠 Reflection: Research revealed that IntelliStack already implements most best practices. Documentation serves as reference for future development and onboarding.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (research task)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate documented patterns against production deployment scenarios

---

**Research Sources:**
- Context7: /better-auth/better-auth (2752 code snippets)
- Context7: /websites/docusaurus_io (10038 code snippets)
- IntelliStack codebase analysis (auth-server, content/src)
- Better Auth official documentation
- Docusaurus v3.x documentation

**Key Files Analyzed:**
- intellistack/content/docusaurus.config.ts
- intellistack/content/src/lib/auth-client.ts
- intellistack/content/src/clientModules/authInit.ts
- intellistack/content/src/contexts/AuthContext.tsx
- intellistack/content/src/theme/NavbarItem/AuthNavbarItem.tsx
- intellistack/content/src/components/ProtectedRoute.tsx
- intellistack/content/src/pages/login.tsx
- intellistack/auth-server/src/auth.ts
