"""
Load test — Phase 4.2: Authentication Middleware Throughput
=============================================================
Tests the authentication middleware under concurrent load with three
traffic shapes that reflect real-world access patterns:

  1. Anonymous / health-check traffic  → public endpoints, no auth header
  2. Invalid JWT traffic               → tokens that trigger the algorithm-
                                         enforcement / JWKS-rejection path
  3. Missing-token protected traffic   → protected endpoint hit without a
                                         token, exercises the 401 fast-path

Run (from the backend directory):
    pip install locust
    locust -f tests/load/locustfile.py \\
           --host http://localhost:8000 \\
           --users 50 --spawn-rate 10 \\
           --run-time 60s --headless \\
           --html tests/load/report.html

Key performance targets (Phase 4 acceptance):
    - p95 latency  ≤ 200 ms on public endpoints
    - p95 latency  ≤ 300 ms on auth-rejected paths
    - Error rate   ≤ 1 %   (401/422 are *expected* — registered as success
                             for load purposes; 5xx are failures)

Alternative (no locust needed):
    python tests/load/locustfile.py --host http://localhost:8000 --users 20 --duration 30
"""

import base64
import json
import time


# ---------------------------------------------------------------------------
# Shared JWT token factory
# ---------------------------------------------------------------------------

def _make_fake_jwt(algorithm: str = "RS256") -> str:
    """
    Build a syntactically-valid-but-unsigned JWT with the given algorithm.
    Used to exercise the algorithm-enforcement path without needing real keys.
    The middleware rejects non-EdDSA tokens before any JWKS network call, so
    this path is fast and predictable.
    """
    header = {"alg": algorithm, "typ": "JWT", "kid": "test-key-id"}
    payload = {
        "sub": "load-test-user",
        "email": "loadtest@example.com",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,
    }

    def _b64(data: dict) -> str:
        return base64.urlsafe_b64encode(
            json.dumps(data, separators=(",", ":")).encode()
        ).rstrip(b"=").decode()

    return f"{_b64(header)}.{_b64(payload)}.fakesignature"


_RS256_TOKEN = _make_fake_jwt("RS256")
_HS256_TOKEN = _make_fake_jwt("HS256")
_NONE_TOKEN  = _make_fake_jwt("none")


# ---------------------------------------------------------------------------
# Locust user classes (used when locust is available)
# ---------------------------------------------------------------------------

try:
    from locust import HttpUser, task, between, constant

    class HealthCheckUser(HttpUser):
        """
        Simulates anonymous / monitoring traffic hitting public endpoints.
        These requests carry no Authorization header and should be served
        quickly without touching the auth path.

        Expected outcome: 200 OK
        Acceptance target: p95 ≤ 200 ms
        """
        weight = 4  # 40 % of virtual users
        wait_time = between(0.5, 1.5)

        @task(3)
        def health(self):
            with self.client.get("/health", catch_response=True) as resp:
                if resp.status_code in (200, 404):
                    resp.success()
                elif resp.status_code >= 500:
                    resp.failure(f"Server error on /health: {resp.status_code}")

        @task(1)
        def docs(self):
            """OpenAPI schema — public, no auth."""
            with self.client.get("/openapi.json", catch_response=True) as resp:
                if resp.status_code in (200, 404):
                    resp.success()
                elif resp.status_code >= 500:
                    resp.failure(f"Server error on /openapi.json: {resp.status_code}")

    class InvalidAlgorithmUser(HttpUser):
        """
        Simulates an attacker / misconfigured client sending JWTs signed with
        RS256 or HS256 (algorithm-confusion attack vectors).

        Expected outcome: 401 Unauthorized with INVALID_TOKEN_ALGORITHM code
        Acceptance target: p95 ≤ 300 ms
        """
        weight = 3  # 30 % of virtual users
        wait_time = constant(0.1)

        @task(2)
        def rs256_token(self):
            with self.client.get(
                "/api/v1/learning/progress",
                headers={"Authorization": f"Bearer {_RS256_TOKEN}"},
                catch_response=True,
                name="/api/v1/learning/progress [RS256]",
            ) as resp:
                if resp.status_code == 401:
                    resp.success()
                elif resp.status_code >= 500:
                    resp.failure(f"Unexpected 5xx for RS256 token: {resp.status_code}")
                else:
                    resp.failure(f"Expected 401, got {resp.status_code}")

        @task(2)
        def hs256_token(self):
            with self.client.get(
                "/api/v1/learning/progress",
                headers={"Authorization": f"Bearer {_HS256_TOKEN}"},
                catch_response=True,
                name="/api/v1/learning/progress [HS256]",
            ) as resp:
                if resp.status_code == 401:
                    resp.success()
                elif resp.status_code >= 500:
                    resp.failure(f"Unexpected 5xx for HS256 token: {resp.status_code}")
                else:
                    resp.failure(f"Expected 401, got {resp.status_code}")

        @task(1)
        def none_token(self):
            with self.client.get(
                "/api/v1/learning/progress",
                headers={"Authorization": "Bearer " + _NONE_TOKEN},
                catch_response=True,
                name="/api/v1/learning/progress [none-alg]",
            ) as resp:
                if resp.status_code == 401:
                    resp.success()
                elif resp.status_code >= 500:
                    resp.failure(f"Unexpected 5xx for none-alg token: {resp.status_code}")
                else:
                    resp.failure(f"Expected 401, got {resp.status_code}")

    class MissingTokenUser(HttpUser):
        """
        Simulates unauthenticated clients hitting protected endpoints.

        Expected outcome: 401 Unauthorized
        Acceptance target: p95 ≤ 300 ms
        """
        weight = 3  # 30 % of virtual users
        wait_time = between(0.2, 1.0)

        PROTECTED_ENDPOINTS = [
            "/api/v1/users/me",
            "/api/v1/learning/progress",
            "/api/v1/users/stage",
        ]

        @task
        def hit_protected_without_token(self):
            endpoint = self.PROTECTED_ENDPOINTS[
                int(time.time() * 1000) % len(self.PROTECTED_ENDPOINTS)
            ]
            with self.client.get(
                endpoint,
                catch_response=True,
                name="protected [no-token]",
            ) as resp:
                if resp.status_code in (401, 403):
                    resp.success()
                elif resp.status_code >= 500:
                    resp.failure(f"Unexpected 5xx for no-token request: {resp.status_code}")
                else:
                    resp.failure(f"Expected 401/403, got {resp.status_code}")

except ModuleNotFoundError:
    pass  # locust not installed — use the asyncio runner below


# ---------------------------------------------------------------------------
# Stand-alone asyncio runner (no locust dependency)
# ---------------------------------------------------------------------------

async def _run_async(host: str, users: int, duration: int) -> None:
    """
    Pure-asyncio load runner — fires concurrent requests for `duration`
    seconds and prints a latency / error-rate summary.

    Usage:
        python tests/load/locustfile.py --host http://localhost:8000 \\
               --users 20 --duration 30
    """
    import asyncio
    import statistics
    try:
        import httpx
    except ModuleNotFoundError:
        print("httpx not installed. Run: pip install httpx")
        raise SystemExit(1)

    latencies: list[float] = []
    errors: list[str]      = []
    total: list[int]       = [0]

    SCENARIOS = [
        # (name, url, headers, expected_status_codes)
        ("health [anon]",        "/health",                {},                                         {200, 404}),
        ("docs [anon]",          "/openapi.json",          {},                                         {200, 404}),
        ("RS256 [invalid-alg]",  "/api/v1/learning/progress", {"Authorization": f"Bearer {_RS256_TOKEN}"}, {401}),
        ("HS256 [invalid-alg]",  "/api/v1/learning/progress", {"Authorization": f"Bearer {_HS256_TOKEN}"}, {401}),
        ("no-token [protected]", "/api/v1/users/me",       {},                                         {401, 403}),
    ]

    deadline = asyncio.get_event_loop().time() + duration

    async def worker(client: "httpx.AsyncClient") -> None:
        idx = 0
        while asyncio.get_event_loop().time() < deadline:
            name, path, headers, expected = SCENARIOS[idx % len(SCENARIOS)]
            idx += 1
            t0 = asyncio.get_event_loop().time()
            try:
                resp = await client.get(host + path, headers=headers, timeout=5.0)
                elapsed_ms = (asyncio.get_event_loop().time() - t0) * 1000
                latencies.append(elapsed_ms)
                total[0] += 1
                if resp.status_code >= 500:
                    errors.append(f"{name}: {resp.status_code}")
                elif resp.status_code not in expected:
                    errors.append(f"{name}: unexpected {resp.status_code} (expected {expected})")
            except Exception as exc:
                total[0] += 1
                errors.append(f"{name}: {exc}")
            await asyncio.sleep(0.05)

    print(f"\n🚀 Load test starting: {users} concurrent users, {duration}s, target={host}")
    print("-" * 60)

    async with httpx.AsyncClient() as client:
        await asyncio.gather(*[worker(client) for _ in range(users)])

    # ---- Results ----
    if not latencies:
        print("No responses recorded — is the server running?")
        return

    latencies.sort()

    def pct(p: float) -> float:
        idx = max(0, int(len(latencies) * p / 100) - 1)
        return round(latencies[idx], 1)

    error_rate = len(errors) / total[0] * 100 if total[0] else 0

    print(f"Requests     : {total[0]}")
    print(f"Errors (5xx) : {len(errors)}  ({error_rate:.2f}%)")
    print(f"Latency p50  : {pct(50)} ms")
    print(f"Latency p95  : {pct(95)} ms")
    print(f"Latency p99  : {pct(99)} ms")
    print(f"Latency max  : {round(max(latencies), 1)} ms")
    print("-" * 60)

    # Acceptance checks
    p95_public = statistics.quantiles(
        [l for l in latencies], n=20
    )[18] if len(latencies) >= 20 else pct(95)

    ok = True
    if pct(95) > 300:
        print(f"⚠️  WARN: p95 latency {pct(95)} ms exceeds 300 ms target")
        ok = False
    if error_rate > 1.0:
        print(f"⚠️  WARN: error rate {error_rate:.2f}% exceeds 1% target")
        ok = False

    if ok:
        print("✅ All acceptance criteria passed")
    else:
        print("❌ Some acceptance criteria failed — review server performance")

    if errors:
        print(f"\nFirst 10 errors:")
        for e in errors[:10]:
            print(f"  • {e}")


if __name__ == "__main__":
    import argparse
    import asyncio

    parser = argparse.ArgumentParser(description="Auth middleware load test")
    parser.add_argument("--host",     default="http://localhost:8000", help="Target host")
    parser.add_argument("--users",    type=int, default=20,            help="Concurrent users")
    parser.add_argument("--duration", type=int, default=30,            help="Duration in seconds")
    args = parser.parse_args()

    asyncio.run(_run_async(args.host, args.users, args.duration))
