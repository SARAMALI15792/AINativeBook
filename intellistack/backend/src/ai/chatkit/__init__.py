"""ChatKit integration module for AI tutor."""

from .models import ChatKitThread, ChatKitThreadItem, ChatKitRateLimit, AiUsageMetric, AuthEventLog
from .store import PostgresChatKitStore
from .context import RequestContext, PageContext
from .rate_limiter import RateLimiter, RateLimitResult
from .agent import SocraticTutorAgent, ChatKitTutorAgent
from .server import IntelliStackChatKitServer
from .routes import router

__all__ = [
    # Models
    "ChatKitThread",
    "ChatKitThreadItem",
    "ChatKitRateLimit",
    "AiUsageMetric",
    "AuthEventLog",
    # Store
    "PostgresChatKitStore",
    # Context
    "RequestContext",
    "PageContext",
    # Rate Limiter
    "RateLimiter",
    "RateLimitResult",
    # Agent
    "SocraticTutorAgent",
    "ChatKitTutorAgent",
    # Server
    "IntelliStackChatKitServer",
    # Routes
    "router",
]
