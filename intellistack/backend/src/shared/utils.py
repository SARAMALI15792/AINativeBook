"""Shared utility functions for IntelliStack backend."""

import hashlib
import secrets
import uuid
from datetime import datetime, timezone
from typing import Any


def generate_uuid() -> str:
    """Generate a new UUID v4 string."""
    return str(uuid.uuid4())


def generate_secret_token(length: int = 32) -> str:
    """Generate a cryptographically secure random token."""
    return secrets.token_urlsafe(length)


def utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


def hash_string(value: str, salt: str = "") -> str:
    """Create SHA-256 hash of a string with optional salt."""
    combined = f"{salt}{value}"
    return hashlib.sha256(combined.encode()).hexdigest()


def slugify(text: str) -> str:
    """Convert text to URL-safe slug."""
    import re

    # Convert to lowercase and replace spaces with hyphens
    slug = text.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[-\s]+", "-", slug)
    return slug.strip("-")


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate string to max length with suffix."""
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def calculate_percentage(completed: int, total: int) -> float:
    """Calculate percentage with safe division."""
    if total == 0:
        return 0.0
    return round((completed / total) * 100, 2)


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Deep merge two dictionaries, with override taking precedence."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def mask_email(email: str) -> str:
    """Mask email address for privacy (e.g., j***n@example.com)."""
    if "@" not in email:
        return email

    local, domain = email.split("@", 1)
    if len(local) <= 2:
        masked_local = local[0] + "*"
    else:
        masked_local = local[0] + "*" * (len(local) - 2) + local[-1]

    return f"{masked_local}@{domain}"


def generate_certificate_number() -> str:
    """Generate a unique certificate number."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    random_part = secrets.token_hex(4).upper()
    return f"IS-{timestamp}-{random_part}"
