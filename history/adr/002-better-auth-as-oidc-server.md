# ADR-002: Better-Auth as Standalone OIDC Server

**Date**: 2026-02-11
**Status**: Accepted
**Initiated By**: Feature 002-better-auth-chatkit

---

## Context

IntelliStack Platform requires a modern authentication system that provides:
- Email/password registration with secure password hashing and strength validation
- OAuth 2.1 social login (Google, GitHub) for frictionless onboarding
- OIDC discovery endpoints for standards compliance
- JWKS public key distribution for multi-service token validation
- Email verification, password reset, account lockout, and role-based access control
- Production-grade security (RS256 signing, PKCE, HTTP-only cookies, bcrypt)

**Constraints**:
- Must run as standalone Node.js service (cannot integrate into FastAPI or Next.js)
- Must provide OIDC discovery endpoint (`/.well-known/openid-configuration`)
- Must provide JWKS endpoint (`/.well-known/jwks.json`) for downstream token validation
- Must integrate with existing PostgreSQL database (Neon)
- Must support big-bang data migration from existing custom auth system

**Decision Drivers**:
- Existing custom Python auth system is fragile and missing OIDC/JWKS standards
- Team expertise in TypeScript/Node.js; Better-Auth is mature and well-documented
- Better-Auth ecosystem provides email templates, OAuth providers, admin plugin out of the box
- RS256 JWT signing with JWKS distribution is production standard for microservices

---

## Decision

**Use Better-Auth with the following configuration**:

1. **Better-Auth Plugins**:
   - **JWT Plugin**: RS256 asymmetric signing with auto-generated key pairs, JWKS endpoint at `/.well-known/jwks.json`
   - **OIDC Provider Plugin**: Standards-compliant OIDC discovery, authorization, token endpoints
   - **Admin Plugin**: Role management (student, instructor, admin) with JWT claims

2. **Email & Password**:
   - Email/password registration enabled with strength validation (12+ chars, uppercase, lowercase, number, special char)
   - Email verification required before full platform access (unverified users: browse only, no lessons)
   - Password reset flow with 1-hour expiry tokens via email

3. **OAuth Providers**:
   - Google OAuth 2.1 with PKCE
   - GitHub OAuth 2.1 with PKCE
   - Automatic account linking on email match

4. **Account Security**:
   - Account lockout after 5 consecutive failed login attempts (30-minute cooldown)
   - HTTP-only session cookies (secure, SameSite=Lax)
   - bcrypt password hashing (12-round default)

5. **Database**:
   - Drizzle ORM adapter to PostgreSQL (Neon)
   - Auto-created tables: user, session, account, verification, jwks, oauth_application, auth_event_log (custom)

6. **Email Delivery**:
   - Resend API for production email (verification, password reset, OAuth magic links)
   - SMTP fallback for development (Gmail SMTP)

---

## Consequences

### ✅ Advantages

1. **Production-Grade**: Better-Auth is actively maintained, used by thousands of apps, audited for security
2. **Standards Compliance**: OIDC discovery and JWKS endpoints required by OAuth 2.1 spec; enables future third-party integrations
3. **Feature Complete**: Covers all authentication use cases (email/password, OAuth, email verification, password reset, lockout, roles) without custom implementation
4. **Developer Experience**: Official TypeScript types, clear API, extensive documentation
5. **Email Ecosystem**: Built-in email templates, Resend/SMTP adapter, token management
6. **Security Best Practices**: RS256 signing, PKCE, secure cookies, bcrypt hashing, rate limiting out of the box
7. **Admin Plugin**: Role-based access control with JWT claims integration
8. **Database Agnostic**: Drizzle adapter works with any PostgreSQL version; Neon compatible

### ⚠️ Tradeoffs

1. **Node.js Dependency**: Adds Node.js to tech stack; increases deployment complexity (three runtimes: Node, Python, TypeScript)
2. **Vendor Lock-In (Soft)**: Better-Auth updates may introduce breaking changes; v1 is stable but API could evolve
3. **Data Migration**: Moving from existing custom auth tables to Better-Auth schema requires careful cutover (big-bang migration risk)
4. **Configuration Complexity**: Better-Auth plugins have many configuration options; requires careful setup to avoid security gaps
5. **Custom Auth Events**: Need custom `auth_event_log` table for audit trail (Better-Auth doesn't provide this natively)

### 🚨 Risks

1. **Breaking Changes in Better-Auth**: If v1 has security updates requiring schema changes, migration complex. Mitigation: pin version in package.json, subscribe to security advisories, maintain abstraction layer
2. **Data Migration Failure**: Moving 1000+ users from old schema to Better-Auth schema at cutover could corrupt data. Mitigation: backup before migration, validation script, staging environment test, rollback plan
3. **Custom Extensions**: If platform needs non-standard auth features (biometric, WebAuthn, FIDO2), may need to fork or wrap Better-Auth. Mitigation: MFA can be added via Better-Auth two-factor plugin (post-feature)
4. **Email Delivery Failures**: If Resend API down or rate-limited, verification/password reset emails may not send. Mitigation: SMTP fallback, retry logic, status page monitoring

---

## Alternatives Considered

### Alternative 1: Custom JWT Auth in FastAPI (Keep Current System)

**Approach**: Keep existing Python custom auth; add JWKS endpoint and OIDC discovery manually.

**Components**:
- PyJWT for token generation
- Custom OIDC discovery endpoint
- Manual JWKS generation and rotation

**Rationale for rejection**:
- Existing system is fragile and lacks security hardening
- Building OIDC provider, JWKS, email templates from scratch = 2-3 months engineering effort
- No OAuth provider integration (Google, GitHub) without third-party library complexity
- Role-based access control and admin panel not implemented
- Maintenance burden on small team; Better-Auth offloads this entirely

**Score**: ❌ Rejected — maintenance burden, duplicate effort

---

### Alternative 2: Keycloak (Open-Source Identity Provider)

**Approach**: Deploy Keycloak as standalone service; FastAPI/Frontend integrate via OpenID Connect.

**Components**:
- Keycloak container (Java-based)
- Separate PostgreSQL for Keycloak
- LDAP/OAuth/SAML provider integrations

**Rationale for rejection**:
- Keycloak adds significant operational complexity (Java service, separate DB, scaling)
- Learning curve steep for team
- Overkill for current scale (500 concurrent users); designed for enterprise identity management
- Configuration and customization requires deep Keycloak expertise
- Adds another deployment target and maintenance responsibility

**Score**: ⚠️ Defer — valid for enterprise scale, not justified yet

---

### Alternative 3: Auth0 / Firebase Authentication (Third-Party SaaS)

**Approach**: Use managed authentication service; outsource all auth infrastructure.

**Components**:
- Auth0 or Firebase Auth hosted service
- Integration via SDK (auth0-spa-js, firebase/auth)

**Rationale for rejection**:
- Recurring cost ($200-500/month depending on scale)
- Vendor lock-in; difficult to migrate away later
- Data residency concerns for educational platform (GDPR, data sovereignty)
- Less control over branding and user experience
- Overkill for current stage; Better-Auth gives 95% of benefits without external dependency

**Score**: ⚠️ Defer — valid for B2B SaaS with revenue, defer until later stage

---

### Alternative 4: OAuth 2.0 Resource Owner Password Flow (No OIDC)

**Approach**: Simple JWT-based auth without OIDC; minimal endpoints.

**Components**:
- FastAPI JWT endpoint
- No OIDC discovery
- Manual OAuth provider integration

**Rationale for rejection**:
- Not standards-compliant; limits future third-party integrations
- OAuth 2.0 spec recommends against Resource Owner Password Flow; security risk
- Missing JWKS public key distribution; requires secret sharing between services
- No email verification, password reset, OAuth out of the box
- Vendor lock-in to FastAPI; cannot reuse auth service for future non-HTTP clients

**Score**: ❌ Rejected — non-standard, inflexible

---

## Compatibility & Dependencies

- **Better-Auth**: v1.x (pinned)
- **Express**: HTTP server for auth endpoints (port 3001)
- **Drizzle ORM**: PostgreSQL adapter
- **Node.js**: 18+ (LTS recommended)
- **TypeScript**: 5.3+
- **PostgreSQL**: Neon (managed)
- **Resend API**: Email delivery (production); SMTP fallback (dev)
- **Environment Variables**: `BETTER_AUTH_SECRET`, `DATABASE_URL`, `GOOGLE_CLIENT_ID`, `GITHUB_CLIENT_ID`, `RESEND_API_KEY`

---

## Migration Path

1. **Phase 1**: Auth server scaffolding and Better-Auth setup
2. **Phase 2**: Social login (Google, GitHub OAuth)
3. **Phase 3**: Email verification and password reset
4. **Phase 4**: Custom auth_event_log for audit trail
5. **Phase 7**: Data migration from old auth tables to Better-Auth schema (big-bang cutover)

**Data Mapping** (old → Better-Auth):
- `user.id` → `user.id` (preserve UUID)
- `user.password_hash` → `account.password` (provider_id='credential')
- `oauth_account` → `account` (provider_id='google'|'github')
- `session` → `session` (recreate active sessions)
- `user.role` → `user.role` (flatten to single role field)
- `password_reset_token` → `verification` table
- `login_attempt` → `auth_event_log` (custom table)

---

## Implementation Notes

1. **Configuration**: Better-Auth config in `src/auth.ts` (all plugins, email, OAuth)
2. **Database**: Drizzle setup in `src/db.ts` (PostgreSQL connection, schema)
3. **Email**: Resend handler in `src/email.ts` (templates, retry logic)
4. **Hooks**: Auth event logging in `src/hooks.ts` (login, register, logout events)
5. **Routes**: Auto-generated by Better-Auth; expose at `/api/auth/*`
6. **Docker**: Standalone auth server container in `docker-compose.yml`

---

## Related ADRs

- ADR-001: Three-Service Architecture (this service is one of three)
- ADR-003: JWKS-Based JWT Validation in FastAPI (uses JWKS from this server)

---

## References

- Better-Auth Official Docs: https://better-auth.com
- Better-Auth GitHub: https://github.com/better-auth/better-auth
- OAuth 2.1 Spec: https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1
- OIDC Core Spec: https://openid.net/specs/openid-connect-core-1_0.html
- `specs/002-better-auth-chatkit/plan.md` § Phase 1-2, Research section
- `specs/002-better-auth-chatkit/research.md` § R-001, R-002

---

## Revision History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-02-11 | SDD Agent | Initial decision record |
