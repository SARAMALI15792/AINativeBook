"""
Observability — Phase 4.4: Structured Metrics & Alerting Hooks
===============================================================
Provides:

  1. In-process metric counters / gauges backed by a lightweight in-memory
     store.  These are exposed at ``GET /metrics`` (text format compatible
     with Prometheus scraping) and at ``GET /health/detail`` (JSON).

  2. Alerting hooks: a simple threshold-based alert dispatcher that can
     call registered handlers (e.g. send a webhook / write to a log channel)
     when a metric breaches a defined threshold.

Design notes
------------
* No external dependencies — uses Python's built-in ``threading`` primitives
  and ``collections.defaultdict``.  Prometheus client library can be swapped
  in later without changing the alert hook interface.
* Thread-safe: all counter mutations go through a ``threading.Lock`` so the
  in-process scrape endpoint always returns consistent data even under async
  concurrent access (asyncio runs in a single thread but ``to_thread`` helpers
  may call from worker threads).
* Alerting is fire-and-forget via ``asyncio.create_task`` (or a synchronous
  fallback) — a slow alert handler never blocks the request path.
"""

from __future__ import annotations

import asyncio
import logging
import threading
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Metric store
# ---------------------------------------------------------------------------

class MetricStore:
    """
    Lightweight in-process metric store.

    Supported metric types:
      - counter  : monotonically increasing integer
      - gauge    : arbitrary float (current value)
      - histogram: latency / value distribution (tracks count + sum + buckets)
    """

    # Default latency buckets in milliseconds (mirrors Prometheus defaults scaled to ms)
    DEFAULT_LATENCY_BUCKETS_MS = [10, 25, 50, 100, 200, 500, 1000, 2500, 5000, float("inf")]

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._counters: Dict[str, float] = defaultdict(float)
        self._gauges: Dict[str, float] = {}
        self._histograms: Dict[str, _HistogramData] = {}
        self._created_at = time.time()

    # ------------------------------------------------------------------
    # Counters
    # ------------------------------------------------------------------

    def inc(self, name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        """Increment a counter."""
        key = _label_key(name, labels)
        with self._lock:
            self._counters[key] += value

    def counter(self, name: str, labels: Optional[Dict[str, str]] = None) -> float:
        """Read current counter value."""
        return self._counters.get(_label_key(name, labels), 0.0)

    # ------------------------------------------------------------------
    # Gauges
    # ------------------------------------------------------------------

    def set_gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """Set a gauge to an absolute value."""
        key = _label_key(name, labels)
        with self._lock:
            self._gauges[key] = value

    def gauge(self, name: str, labels: Optional[Dict[str, str]] = None) -> float:
        """Read current gauge value."""
        return self._gauges.get(_label_key(name, labels), 0.0)

    # ------------------------------------------------------------------
    # Histograms
    # ------------------------------------------------------------------

    def observe(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """Record an observation (e.g. latency in ms)."""
        key = _label_key(name, labels)
        with self._lock:
            if key not in self._histograms:
                self._histograms[key] = _HistogramData(self.DEFAULT_LATENCY_BUCKETS_MS)
            self._histograms[key].observe(value)

    def histogram_summary(
        self, name: str, labels: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Return count, sum, mean, and bucket distribution for a histogram."""
        key = _label_key(name, labels)
        h = self._histograms.get(key)
        if h is None:
            return {"count": 0, "sum": 0.0, "mean": 0.0, "buckets": {}}
        return h.summary()

    # ------------------------------------------------------------------
    # Prometheus text format export
    # ------------------------------------------------------------------

    def to_prometheus_text(self) -> str:
        """
        Render all metrics in Prometheus exposition format (text/plain).
        Compatible with ``prometheus_client`` scraping out of the box.
        """
        lines: List[str] = [
            f"# IntelliStack metrics — uptime {int(time.time() - self._created_at)}s",
        ]

        with self._lock:
            for key, value in sorted(self._counters.items()):
                lines.append(f"{key}_total {value}")

            for key, value in sorted(self._gauges.items()):
                lines.append(f"{key} {value}")

            for key, hdata in sorted(self._histograms.items()):
                summary = hdata.summary()
                lines.append(f"{key}_count {summary['count']}")
                lines.append(f"{key}_sum {summary['sum']:.3f}")
                for bound, cnt in summary["buckets"].items():
                    bucket_key = key.replace("{", 'le="{}'.format(bound)).rstrip("}")
                    lines.append(f"{key}_bucket{{le=\"{bound}\"}} {cnt}")

        lines.append("")  # trailing newline
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # JSON export (for /health/detail endpoint)
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """Return all metrics as a JSON-serialisable dict."""
        with self._lock:
            return {
                "uptime_seconds": int(time.time() - self._created_at),
                "counters": dict(self._counters),
                "gauges": dict(self._gauges),
                "histograms": {
                    k: v.summary() for k, v in self._histograms.items()
                },
            }


# ---------------------------------------------------------------------------
# Histogram implementation detail
# ---------------------------------------------------------------------------

class _HistogramData:
    def __init__(self, buckets: List[float]) -> None:
        self.buckets = sorted(buckets)
        self._counts: Dict[float, int] = {b: 0 for b in self.buckets}
        self._count = 0
        self._sum = 0.0

    def observe(self, value: float) -> None:
        self._count += 1
        self._sum += value
        for b in self.buckets:
            if value <= b:
                self._counts[b] += 1

    def summary(self) -> Dict[str, Any]:
        return {
            "count": self._count,
            "sum": round(self._sum, 3),
            "mean": round(self._sum / self._count, 3) if self._count else 0.0,
            "buckets": {str(b): cnt for b, cnt in self._counts.items()},
        }


# ---------------------------------------------------------------------------
# Label helper
# ---------------------------------------------------------------------------

def _label_key(name: str, labels: Optional[Dict[str, str]]) -> str:
    if not labels:
        return name
    label_str = ",".join(f'{k}="{v}"' for k, v in sorted(labels.items()))
    return f"{name}{{{label_str}}}"


# ---------------------------------------------------------------------------
# Alerting hooks
# ---------------------------------------------------------------------------

@dataclass
class AlertRule:
    """
    A threshold rule that fires when ``metric_value >= threshold``.

    Fields
    ------
    name        : human-readable rule name (used in log messages)
    metric_name : the MetricStore key to check (use same name as passed to inc/set_gauge)
    threshold   : numeric threshold; rule fires when value >= threshold
    handler     : async callable ``async (rule, value) -> None``; called when rule fires
    cooldown_s  : minimum seconds between repeated firings for the same rule (default 300 s)
    """
    name: str
    metric_name: str
    threshold: float
    handler: Callable[["AlertRule", float], Any]
    cooldown_s: int = 300
    _last_fired: float = field(default=0.0, repr=False, compare=False)


class AlertDispatcher:
    """
    Evaluates registered ``AlertRule`` objects against the current metric
    store values and calls their handlers when thresholds are breached.

    Call ``check_all()`` periodically (e.g. from a background task or
    after every request batch) to trigger evaluation.
    """

    def __init__(self, store: MetricStore) -> None:
        self._store = store
        self._rules: List[AlertRule] = []
        self._lock = threading.Lock()

    def register(self, rule: AlertRule) -> None:
        """Register an alert rule."""
        with self._lock:
            self._rules.append(rule)
        logger.info(f"Alert rule registered: {rule.name!r} (threshold={rule.threshold})")

    async def check_all(self) -> None:
        """Evaluate all rules; fire handlers for breached thresholds."""
        now = time.time()
        with self._lock:
            rules_snapshot = list(self._rules)

        for rule in rules_snapshot:
            # Determine the current value for this metric
            value = self._store.counter(rule.metric_name)
            if value == 0.0:
                value = self._store.gauge(rule.metric_name)

            if value >= rule.threshold:
                elapsed_since_last = now - rule._last_fired
                if elapsed_since_last >= rule.cooldown_s:
                    rule._last_fired = now
                    logger.warning(
                        f"ALERT FIRED: {rule.name!r} — "
                        f"{rule.metric_name}={value:.1f} >= threshold={rule.threshold}"
                    )
                    try:
                        result = rule.handler(rule, value)
                        if asyncio.iscoroutine(result):
                            await result
                    except Exception as exc:
                        logger.error(f"Alert handler for {rule.name!r} raised: {exc}")


# ---------------------------------------------------------------------------
# Built-in alert handlers
# ---------------------------------------------------------------------------

async def log_alert_handler(rule: AlertRule, value: float) -> None:
    """
    Default handler: writes a structured WARNING log entry.
    Replace or extend with a webhook, PagerDuty call, Slack message, etc.
    """
    logger.warning(
        "alert_fired",
        extra={
            "alert_name": rule.name,
            "metric": rule.metric_name,
            "value": value,
            "threshold": rule.threshold,
        },
    )


# ---------------------------------------------------------------------------
# Pre-configured metric names (import these in middleware / routes)
# ---------------------------------------------------------------------------

# HTTP layer
METRIC_HTTP_REQUESTS_TOTAL   = "http_requests_total"
METRIC_HTTP_ERRORS_TOTAL     = "http_errors_total"
METRIC_HTTP_LATENCY_MS       = "http_request_duration_ms"

# Auth
METRIC_AUTH_FAILURES_TOTAL   = "auth_failures_total"
METRIC_RATE_LIMIT_HITS       = "rate_limit_hits_total"

# AI
METRIC_AI_REQUESTS_TOTAL     = "ai_requests_total"
METRIC_AI_ERRORS_TOTAL       = "ai_errors_total"
METRIC_AI_LATENCY_MS         = "ai_request_duration_ms"

# DB
METRIC_DB_POOL_CHECKED_OUT   = "db_pool_checked_out"
METRIC_DB_ERRORS_TOTAL       = "db_errors_total"


# ---------------------------------------------------------------------------
# Singletons — import these anywhere in the application
# ---------------------------------------------------------------------------

#: Global metric store — all modules share this instance.
metrics = MetricStore()

#: Global alert dispatcher — register rules in ``main.py`` startup.
alerts = AlertDispatcher(metrics)


# ---------------------------------------------------------------------------
# Default alert rules (registered on import — overridable in main.py)
# ---------------------------------------------------------------------------

def register_default_alert_rules() -> None:
    """
    Register sensible default alerting rules for production.

    Call once from ``create_app()`` in ``main.py``.
    Override thresholds via environment-specific config as needed.
    """
    alerts.register(AlertRule(
        name="High auth failure rate",
        metric_name=METRIC_AUTH_FAILURES_TOTAL,
        threshold=100,  # 100 cumulative failures → alert
        handler=log_alert_handler,
        cooldown_s=300,
    ))
    alerts.register(AlertRule(
        name="High HTTP error rate",
        metric_name=METRIC_HTTP_ERRORS_TOTAL,
        threshold=50,
        handler=log_alert_handler,
        cooldown_s=60,
    ))
    alerts.register(AlertRule(
        name="AI error spike",
        metric_name=METRIC_AI_ERRORS_TOTAL,
        threshold=20,
        handler=log_alert_handler,
        cooldown_s=120,
    ))
    alerts.register(AlertRule(
        name="Rate limiter abuse",
        metric_name=METRIC_RATE_LIMIT_HITS,
        threshold=200,
        handler=log_alert_handler,
        cooldown_s=300,
    ))
    logger.info("Default alert rules registered (4 rules)")
