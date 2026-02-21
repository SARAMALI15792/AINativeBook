# Security Incident Report - Exposed Credentials

**Date:** 2026-02-21
**Severity:** CRITICAL
**Status:** REMEDIATION IN PROGRESS

## Summary

Production credentials were accidentally committed to the git repository in `.env` files. These credentials are now considered compromised and must be rotated immediately.

## Exposed Credentials

### 1. Database (Neon PostgreSQL)
- **Location:** `intellistack/backend/.env`, `intellistack/backend/.env.production`, `intellistack/auth-server/.env`
- **Credential:** Database URL with password
- **Impact:** Full database access (read/write/delete)
- **Action Required:** Rotate database password in Neon dashboard

### 2. Google OAuth
- **Location:** `intellistack/backend/.env`, `intellistack/auth-server/.env`
- **Credentials:** Client ID and Client Secret
- **Impact:** Unauthorized OAuth flows, potential account takeover
- **Action Required:** Generate new OAuth credentials in Google Cloud Console

### 3. Better-Auth Secret
- **Location:** `intellistack/backend/.env`, `intellistack/auth-server/.env`
- **Credential:** JWT signing secret
- **Impact:** Token forgery, session hijacking
- **Action Required:** Generate new secret with `openssl rand -base64 32`

### 4. Backend Secret Key
- **Location:** `intellistack/backend/.env`
- **Credential:** Application secret key
- **Impact:** Session manipulation, CSRF bypass
- **Action Required:** Generate new secret with `openssl rand -base64 32`

## Remediation Steps

### Immediate Actions (COMPLETED)
- [x] Remove debug print statements from middleware (commit: pending)
- [x] Update .gitignore to prevent future commits
- [x] Document incident and required actions

### Required Actions (USER MUST COMPLETE)

#### 1. Rotate Neon Database Password (5 minutes)
```bash
# 1. Go to: https://console.neon.tech
# 2. Select project: IntelliStack
# 3. Navigate to: Settings → Reset Password
# 4. Copy new DATABASE_URL
# 5. Update in Railway dashboard:
#    - Backend Service → Variables → DATABASE_URL
#    - Auth Server Service → Variables → DATABASE_URL
```

#### 2. Rotate Google OAuth Credentials (10 minutes)
```bash
# 1. Go to: https://console.cloud.google.com/apis/credentials
# 2. Select project: IntelliStack
# 3. Find OAuth 2.0 Client ID: "IntelliStack Auth"
# 4. Click "Delete" (revoke old credentials)
# 5. Click "Create Credentials" → "OAuth 2.0 Client ID"
# 6. Application type: Web application
# 7. Authorized redirect URIs:
#    - https://<auth-railway-domain>/api/auth/callback/google
#    - http://localhost:3001/api/auth/callback/google (for dev)
# 8. Copy new Client ID and Client Secret
# 9. Update in Railway dashboard:
#    - Auth Server → Variables → GOOGLE_CLIENT_ID
#    - Auth Server → Variables → GOOGLE_CLIENT_SECRET
#    - Backend → Variables → GOOGLE_CLIENT_ID
#    - Backend → Variables → GOOGLE_CLIENT_SECRET
```

#### 3. Generate New Secrets (2 minutes)
```bash
# Generate new Better-Auth secret
openssl rand -base64 32
# Copy output, update in Railway:
# - Auth Server → Variables → BETTER_AUTH_SECRET
# - Backend → Variables → BETTER_AUTH_SECRET

# Generate new Backend secret key
openssl rand -base64 32
# Copy output, update in Railway:
# - Backend → Variables → SECRET_KEY
```

#### 4. Remove .env Files from Git History (15 minutes)
```bash
# WARNING: This rewrites git history - coordinate with team first

# Install git-filter-repo
pip install git-filter-repo

# Backup repository
cd ..
git clone physicalhumoniodbook physicalhumoniodbook-backup

# Remove .env files from history
cd physicalhumoniodbook
git filter-repo --path intellistack/backend/.env --invert-paths --force
git filter-repo --path intellistack/backend/.env.production --invert-paths --force
git filter-repo --path intellistack/auth-server/.env --invert-paths --force
git filter-repo --path intellistack/content/.env --invert-paths --force

# Force push (WARNING: Destructive)
git push origin --force --all
git push origin --force --tags
```

#### 5. Update Local .env Files (2 minutes)
```bash
# After rotating credentials, update local .env files with new values
# DO NOT commit these files - they are now in .gitignore
```

#### 6. Verify Deployment (5 minutes)
```bash
# After updating Railway environment variables, redeploy all services
railway up --service backend --detach
railway up --service auth-server --detach

# Test health endpoints
curl https://<backend-domain>/health
curl https://<auth-domain>/health
```

## Prevention Measures

### Implemented
- [x] Enhanced .gitignore to block all .env variants
- [x] Removed debug print statements that log sensitive data
- [x] Created this incident report

### Recommended
- [ ] Add pre-commit hook to scan for secrets (use `detect-secrets` or `gitleaks`)
- [ ] Enable GitHub secret scanning alerts
- [ ] Use Railway's secret management exclusively (no local .env in production)
- [ ] Implement secret rotation policy (every 90 days)
- [ ] Add security scanning to CI/CD pipeline

## Timeline

- **2026-02-21 23:32 UTC:** Incident discovered during deployment analysis
- **2026-02-21 23:35 UTC:** Debug statements removed, .gitignore updated
- **2026-02-21 23:40 UTC:** Incident report created
- **Pending:** User completes credential rotation
- **Pending:** Git history cleanup
- **Pending:** Deployment verification

## Impact Assessment

**Current Risk:** HIGH
- Credentials exposed in public/private repository
- Unknown if credentials were accessed by unauthorized parties
- All services using compromised credentials

**Post-Remediation Risk:** LOW
- New credentials not exposed
- Git history cleaned
- Prevention measures in place

## Notes

- The exposed credentials were for development/staging, but used the production database
- No evidence of unauthorized access detected (requires log analysis)
- All users should be notified to re-authenticate after credential rotation
- Consider implementing audit logging for database access

## Checklist for User

Before deploying to production:
- [ ] Rotate Neon database password
- [ ] Rotate Google OAuth credentials
- [ ] Generate new Better-Auth secret
- [ ] Generate new Backend secret key
- [ ] Update all Railway environment variables
- [ ] Remove .env files from git history
- [ ] Verify deployments work with new credentials
- [ ] Enable GitHub secret scanning
- [ ] Add pre-commit hooks for secret detection

---

**Report prepared by:** Claude Code (Autonomous Agent)
**Next review:** After user completes remediation steps
