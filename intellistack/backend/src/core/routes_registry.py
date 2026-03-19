"""
Centralised router registry for IntelliStack.

All APIRouter instances and their mount configuration are declared here.
``main.py`` calls ``register_all_routers(app)`` instead of calling
``app.include_router(...)`` individually, which means:

  * Adding a new router = one entry in this file only.
  * Mount prefixes are visible in a single place (easier to audit).
  * Tests can import ``ROUTER_CONFIGS`` to enumerate expected route prefixes.

Registry schema
---------------
Each entry is a dict with keys:

  router  : APIRouter  — the router instance to register
  prefix  : str        — path prefix **added by main.py** (empty string if the
                         router already carries its full prefix internally)
  tags    : list[str]  — optional extra OpenAPI tags (usually empty — the
                         router itself declares its own tags)
  note    : str        — human-readable description of the final route base path

The ``prefix`` column documents the two-tier prefix pattern:

  Tier A — "bare" routers: their ``prefix`` attribute in the router definition
  is only the sub-path (e.g. ``/learning``).  ``main.py`` supplies ``/api/v1``
  so the effective path is ``/api/v1/learning/...``.

  Tier B — "full" routers: their prefix is already the complete path
  (e.g. ``/api/v1/chatkit``).  ``main.py`` supplies ``""`` (empty).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from fastapi import FastAPI
from fastapi import APIRouter


@dataclass
class RouterConfig:
    """Configuration for a single router mount."""

    router: APIRouter
    prefix: str = "/api/v1"
    tags: List[str] = field(default_factory=list)
    note: str = ""


def _build_registry() -> List[RouterConfig]:
    """
    Lazily import and assemble the full router registry.

    Imports are deferred so that loading this module does NOT trigger the full
    application initialisation chain (settings validation, DB connection, etc.).
    This keeps tests that only need the registry list fast and side-effect-free.
    """
    # --- Tier A: bare-path routers (main.py supplies /api/v1) ---------------
    from src.ai.rag.routes import router as rag_router
    from src.ai.tutor.routes import router as tutor_router
    from src.core.content.routes import router as content_router
    from src.core.institution.routes import router as institution_router
    from src.core.learning.routes import router as learning_router

    # --- Tier B: full-path routers (already include /api/v1 in their prefix) -
    from src.ai.chatkit.routes import router as chatkit_router
    from src.ai.code_execution.routes import router as code_execution_router
    from src.ai.personalization.routes import router as personalization_router
    from src.ai.translation.routes import router as translation_router
    from src.core.content.enhanced_routes import router as enhanced_content_router
    from src.core.users.preferences_routes import router as preferences_router
    from src.core.users.routes import router as users_router

    return [
        # ------------------------------------------------------------------
        # Tier A — main.py prepends /api/v1
        # ------------------------------------------------------------------
        RouterConfig(
            router=content_router,
            prefix="/api/v1",
            note="/api/v1/content/...",
        ),
        RouterConfig(
            router=institution_router,
            prefix="/api/v1",
            note="/api/v1/institution/...",
        ),
        RouterConfig(
            router=learning_router,
            prefix="/api/v1",
            note="/api/v1/learning/...",
        ),
        RouterConfig(
            router=rag_router,
            prefix="/api/v1",
            note="/api/v1/ai/rag/...",
        ),
        RouterConfig(
            router=tutor_router,
            prefix="/api/v1",
            note="/api/v1/ai/tutor/...",
        ),
        # ------------------------------------------------------------------
        # Tier B — routers carry their own full /api/v1/... prefix
        # ------------------------------------------------------------------
        RouterConfig(
            router=chatkit_router,
            prefix="",
            note="/api/v1/chatkit/...",
        ),
        RouterConfig(
            router=users_router,
            prefix="",
            note="/api/v1/users/...",
        ),
        RouterConfig(
            router=preferences_router,
            prefix="",
            note="/api/v1/users/preferences/...",
        ),
        RouterConfig(
            router=personalization_router,
            prefix="",
            note="/api/v1/personalization/...",
        ),
        RouterConfig(
            router=translation_router,
            prefix="",
            note="/api/v1/translation/...",
        ),
        RouterConfig(
            router=code_execution_router,
            prefix="",
            note="/api/v1/code/...",
        ),
        RouterConfig(
            router=enhanced_content_router,
            prefix="",
            note="/api/v1/enhanced-content/...",
        ),
    ]


def register_all_routers(app: FastAPI) -> None:
    """
    Register every router in the registry with the FastAPI application.

    Called once from ``create_app()`` in ``main.py``.
    """
    for cfg in _build_registry():
        app.include_router(cfg.router, prefix=cfg.prefix)
