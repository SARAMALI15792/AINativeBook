"""Custom exception classes for IntelliStack application."""

from typing import Any


class IntelliStackError(Exception):
    """Base exception for all IntelliStack errors."""

    error_code: str = "INTELLISTACK_ERROR"
    status_code: int = 500
    message: str = "An unexpected error occurred"

    def __init__(
        self,
        message: str | None = None,
        error_code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.message = message or self.message
        self.error_code = error_code or self.error_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary for JSON response."""
        return {
            "error": {
                "code": self.error_code,
                "message": self.message,
                "details": self.details,
            }
        }


class NotFoundError(IntelliStackError):
    """Resource not found error."""

    error_code = "NOT_FOUND"
    status_code = 404
    message = "The requested resource was not found"

    def __init__(
        self,
        resource: str = "Resource",
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        message = f"{resource} not found"
        if resource_id:
            message = f"{resource} with id '{resource_id}' not found"
        super().__init__(message=message, **kwargs)


class UnauthorizedError(IntelliStackError):
    """Authentication required error."""

    error_code = "UNAUTHORIZED"
    status_code = 401
    message = "Authentication required"


class ForbiddenError(IntelliStackError):
    """Access denied error."""

    error_code = "FORBIDDEN"
    status_code = 403
    message = "You don't have permission to access this resource"

    def __init__(
        self,
        required_role: str | None = None,
        **kwargs: Any,
    ) -> None:
        message = self.message
        if required_role:
            message = f"This action requires the '{required_role}' role"
        super().__init__(message=message, **kwargs)


class ValidationError(IntelliStackError):
    """Input validation error."""

    error_code = "VALIDATION_ERROR"
    status_code = 422
    message = "Invalid input data"

    def __init__(
        self,
        field: str | None = None,
        reason: str | None = None,
        **kwargs: Any,
    ) -> None:
        message = self.message
        if field and reason:
            message = f"Validation failed for '{field}': {reason}"
        elif field:
            message = f"Invalid value for field '{field}'"
        super().__init__(message=message, **kwargs)


class ConflictError(IntelliStackError):
    """Resource conflict error (e.g., duplicate)."""

    error_code = "CONFLICT"
    status_code = 409
    message = "Resource conflict"

    def __init__(
        self,
        resource: str = "Resource",
        field: str | None = None,
        **kwargs: Any,
    ) -> None:
        message = f"{resource} already exists"
        if field:
            message = f"{resource} with this {field} already exists"
        super().__init__(message=message, **kwargs)


class RateLimitError(IntelliStackError):
    """Rate limit exceeded error."""

    error_code = "RATE_LIMIT_EXCEEDED"
    status_code = 429
    message = "Too many requests. Please try again later."


class ServiceUnavailableError(IntelliStackError):
    """External service unavailable error."""

    error_code = "SERVICE_UNAVAILABLE"
    status_code = 503
    message = "Service temporarily unavailable"

    def __init__(
        self,
        service: str = "External service",
        **kwargs: Any,
    ) -> None:
        message = f"{service} is temporarily unavailable"
        super().__init__(message=message, **kwargs)


class AuthenticationError(IntelliStackError):
    """Authentication failed error."""

    error_code = "AUTHENTICATION_FAILED"
    status_code = 401
    message = "Authentication failed"


class AuthorizationError(IntelliStackError):
    """Authorization failed error."""

    error_code = "AUTHORIZATION_FAILED"
    status_code = 403
    message = "Authorization failed"


class PrerequisiteNotMetError(IntelliStackError):
    """Learning prerequisite not met error."""

    error_code = "PREREQUISITE_NOT_MET"
    status_code = 403
    message = "Prerequisite requirements not met"

    def __init__(
        self,
        stage_name: str,
        required_stage: str,
        **kwargs: Any,
    ) -> None:
        message = f"Cannot access '{stage_name}'. Complete '{required_stage}' first."
        details = {
            "target_stage": stage_name,
            "required_stage": required_stage,
        }
        super().__init__(message=message, details=details, **kwargs)
