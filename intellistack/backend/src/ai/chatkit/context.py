"""
ChatKit Request Context

Dataclass containing all context information for a ChatKit request,
including user identity, page context, and metadata.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class PageContext:
    """Context from the current page/lesson."""

    url: str
    title: str
    headings: List[str] = field(default_factory=list)
    selected_text: Optional[str] = None
    course_id: Optional[str] = None
    lesson_id: Optional[str] = None
    stage: Optional[int] = None

    @classmethod
    def from_headers(cls, headers: Dict[str, str]) -> "PageContext":
        """
        Create PageContext from request headers.

        Expected headers:
        - X-Page-Url
        - X-Page-Title
        - X-Page-Headings (JSON array)
        - X-Selected-Text
        - X-Course-Id
        - X-Lesson-Id
        - X-User-Stage
        """
        import json

        headings = []
        if headings_json := headers.get("x-page-headings"):
            try:
                headings = json.loads(headings_json)
            except json.JSONDecodeError:
                pass

        return cls(
            url=headers.get("x-page-url", ""),
            title=headers.get("x-page-title", ""),
            headings=headings,
            selected_text=headers.get("x-selected-text") or None,
            course_id=headers.get("x-course-id") or None,
            lesson_id=headers.get("x-lesson-id") or None,
            stage=int(headers.get("x-user-stage", "1")),
        )


@dataclass
class RequestContext:
    """
    Complete context for a ChatKit request.

    Contains user identity, page context, and additional metadata
    needed for RAG retrieval and response generation.
    """

    # User identity (from JWT)
    user_id: str
    user_email: str
    user_name: Optional[str] = None
    user_role: str = "student"
    user_stage: int = 1  # Current unlocked learning stage (1-5)
    email_verified: bool = False

    # Page context
    page_context: PageContext = field(default_factory=lambda: PageContext(url="", title=""))

    # Thread context
    thread_id: Optional[str] = None
    is_new_thread: bool = False

    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Rate limit info (populated after check)
    rate_limit_remaining: Optional[int] = None
    rate_limit_reset: Optional[str] = None

    @property
    def accessible_stages(self) -> List[int]:
        """
        Get list of stages the user can access.

        Returns stages 1 through user_stage (inclusive).
        """
        return list(range(1, self.user_stage + 1))

    @property
    def accessible_stage_ids(self) -> List[str]:
        """
        Get stage IDs as strings for filtering.
        """
        return [f"stage-{i}" for i in self.accessible_stages]

    def to_system_context(self) -> str:
        """
        Generate system context string for AI prompt.

        Includes relevant page and user information.
        """
        parts = []

        if self.page_context.title:
            parts.append(f"Current page: {self.page_context.title}")

        if self.page_context.url:
            parts.append(f"URL: {self.page_context.url}")

        if self.page_context.headings:
            parts.append(f"Page sections: {', '.join(self.page_context.headings[:5])}")

        if self.page_context.selected_text:
            # Truncate selected text if too long
            text = self.page_context.selected_text[:500]
            if len(self.page_context.selected_text) > 500:
                text += "..."
            parts.append(f"Selected text: \"{text}\"")

        parts.append(f"User stage: {self.user_stage} (can access stages 1-{self.user_stage})")
        parts.append(f"User role: {self.user_role}")

        return "\n".join(parts)

    @classmethod
    def from_request(
        cls,
        user_id: str,
        user_email: str,
        headers: Dict[str, str],
        user_name: Optional[str] = None,
        user_role: str = "student",
        user_stage: int = 1,
        email_verified: bool = False,
        thread_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "RequestContext":
        """
        Create RequestContext from request data.

        Args:
            user_id: User ID from JWT
            user_email: User email from JWT
            headers: Request headers dict
            user_name: User name from JWT
            user_role: User role from JWT
            user_stage: User's current unlocked stage
            email_verified: Whether email is verified
            thread_id: Thread ID if continuing conversation
            metadata: Additional metadata

        Returns:
            RequestContext instance
        """
        return cls(
            user_id=user_id,
            user_email=user_email,
            user_name=user_name,
            user_role=user_role,
            user_stage=user_stage,
            email_verified=email_verified,
            page_context=PageContext.from_headers(headers),
            thread_id=thread_id,
            is_new_thread=thread_id is None,
            metadata=metadata or {},
        )
