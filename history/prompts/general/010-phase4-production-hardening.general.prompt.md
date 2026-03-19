---
id: 010
title: Phase 4 — Production Hardening
stage: refactor
date: 2026-03-17
surface: agent
model: claude-sonnet-4-6
feature: 001-intellistack-platform
branch: 001-intellistack-platform
user: Akhtar
command: "move on the next phase 4 to implementation of work"
labels: ["phase4","production-hardening","security-scan","load-test","connection-pool","observability","metrics","alerting"]
links:
  spec: specs/001-intellistack-platform/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/shared/metrics.py (NEW)
  - tests/load/locustfile.py (NEW)
  - src/shared/database.py
  - src/config/settings.py
  - src/shared/middleware.py
  - src/main.py
  - project_docs/03_sequence/PHASE_SEQUENCE.md
tests:
  - All 68 tests pass (67 Phase 2/3 tests + 1 additional collected) — zero regressions
---

## Prompt

"move on the next phase 4 to implementation of work"

## Response snapshot

Implemented all 5 Phase 4 production hardening tasks:

**4.1 — Security scan**
Ran `python -m bandit -r src/` — initial scan: 1 Medium + 3 Low findings. All 4 were false positives / intentional configurations:
- `src/config/settings.py:28` — `host="0.0.0.0"` → `# nosec B104` (containerised, network-isolated)
- `src/core/assessment/service.py:395` — `random.uniform` → `# nosec B311` (placeholder, not cryptographic)
- `src/core/auth/dependencies.py:125` — `password_hash=''` → `# nosec B106` (sentinel; auth is Better-Auth-managed)
- `src/core/users/routes.py:44` — `password_hash="!better-auth-managed"` → `# nosec B106` (sentinel value)
Final bandit scan: **0 issues (High=0, Medium=0, Low=0)**.

Ran `pip-audit -r requirements.txt` → **0 known vulnerabilities** in project dependencies. (System Python packages excluded — not IntelliStack's responsibility.)

**4.2 — Load test (`tests/load/locustfile.py`)**
Dual-mode load test script:
- Locust mode (`locust -f tests/load/locustfile.py --host http://localhost:8000`) when locust is installed
- Stand-alone asyncio/httpx mode (`python tests/load/locustfile.py --host ... --users 20 --duration 30`) with no extra deps

Three traffic shapes with defined acceptance targets:
- `HealthCheckUser` (40% weight): hits `/health`, `/openapi.json` with no auth — p95 ≤ 200 ms
- `InvalidAlgorithmUser` (30%): sends RS256/HS256/none-alg JWTs to trigger early algorithm-rejection path — p95 ≤ 300 ms
- `MissingTokenUser` (30%): hits protected endpoints without token — expects 401/403, p95 ≤ 300 ms
- Error rate target: ≤ 1% (401/403 are expected and registered as success; only 5xx are failures)

**4.3 — Database connection pool tuning**
`src/shared/database.py` — `_get_connect_args` now passes `server_settings={"statement_timeout": str(ms), "application_name": "intellistack-backend"}` to asyncpg at connect time. This enforces a per-query Postgres GUC timeout so runaway queries cannot block a connection indefinitely.

`init_db` now passes:
- `pool_recycle=settings.db_pool_recycle` (default 1800 s) — recycles connections before Neon/RDS idle-timeout closes them silently
- `pool_reset_on_return="rollback"` — ensures every borrowed connection starts with a clean transaction state

`src/config/settings.py` — added `db_pool_recycle: int = 1800` and `db_statement_timeout_ms: int = 30000`.

**4.4 — Observability: structured metrics + alerting hooks (`src/shared/metrics.py`)**
New `MetricStore` class:
- `inc(name, value, labels)` — monotonic counter
- `set_gauge(name, value, labels)` — arbitrary float gauge
- `observe(name, value, labels)` — histogram with configurable buckets
- `to_prometheus_text()` — Prometheus exposition format for scraping
- `to_dict()` — JSON for `/health/detail`

New `AlertDispatcher` + `AlertRule` dataclass:
- Threshold-based rules; fire once per `cooldown_s` (default 300 s)
- Handler: `async (rule, value) -> None`; built-in `log_alert_handler` writes structured WARNING log
- `register_default_alert_rules()` registers 4 rules on startup: high auth failures (≥100), high HTTP errors (≥50), AI error spike (≥20), rate limiter abuse (≥200)

Wired metrics into:
- `RequestLoggingMiddleware` — increments `http_requests_total{method,status_class}`, observes `http_request_duration_ms`, increments `http_errors_total{status_code}` on ≥400
- `JWKSAuthMiddleware` — increments `auth_failures_total{reason=invalid_algorithm}` on algorithm-confusion rejection
- `UserScopedRateLimiter` — increments `rate_limit_hits_total{prefix}` before 429

Two new endpoints in `src/main.py`:
- `GET /health/detail` — JSON metrics dump (for ops dashboards)
- `GET /metrics` — Prometheus text format (for Prometheus scraper)

**4.5 — Final documentation**
Updated `project_docs/03_sequence/PHASE_SEQUENCE.md`:
- Phase 4 marked ✅ COMPLETE with per-task file references
- Quick Stats table updated with Phase 4 metrics

## Outcome

- ✅ Impact: All 4 production hardening areas complete — zero bandit/pip-audit findings; load test covers 3 real-world traffic shapes; DB pool is stale-connection-safe with per-query timeout; metrics observable at /metrics and /health/detail with alerting hooks
- 🧪 Tests: 68/68 tests pass — zero regressions from Phase 4 changes
- 📁 Files: 2 new source files, 5 modified source files, PHASE_SEQUENCE.md updated
- 🔁 Next prompts: Phase 5 — spec implementation continues (Phase 7: AI Tutor, Phase 8: Community, Phase 9: Assessment, Phase 10: Personalization)
- 🧠 Reflection: The pip-audit system-vs-project distinction matters: running against the global Python environment produces false positives from OS packages. Always scope dependency scans to `requirements.txt` or the virtual environment. For the metrics module, a pure-stdlib approach (no Prometheus client library) keeps zero production deps added while remaining compatible with Prometheus scraping protocol.

## Evaluation notes (flywheel)

- Failure modes observed: locust gevent/zope dependency conflict in sandbox — resolved by using dual-mode design (asyncio/httpx fallback)
- Graders run and results (PASS/FAIL): pytest 68/68 PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Phase 5 — implement AI Tutor (Phase 7 in original spec: Socratic method, debugging helper, code review)
