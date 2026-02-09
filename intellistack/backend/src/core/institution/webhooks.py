"""Webhook notification service for institution events (FR-039)."""

import asyncio
import hashlib
import hmac
import json
from datetime import datetime
from typing import Optional, Dict, Any
import logging

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.institution.models import Institution

logger = logging.getLogger(__name__)

# Webhook event types
WEBHOOK_EVENT_ENROLLMENT = "student.enrolled"
WEBHOOK_EVENT_PROGRESS = "student.progress_milestone"
WEBHOOK_EVENT_COMPLETION = "student.stage_completed"
WEBHOOK_EVENT_ASSESSMENT = "student.assessment_completed"
WEBHOOK_EVENT_CERTIFICATE = "student.certificate_issued"


async def send_webhook_event(
    db: AsyncSession,
    institution_id: str,
    event_type: str,
    event_data: Dict[str, Any],
    retry_count: int = 0,
    max_retries: int = 3,
) -> bool:
    """
    Send webhook notification to institution with automatic retry on failure (FR-039).

    Args:
        db: Database session
        institution_id: Institution ID
        event_type: Event type (e.g., "student.enrolled")
        event_data: Event payload data
        retry_count: Current retry attempt
        max_retries: Maximum retry attempts

    Returns:
        bool: True if webhook sent successfully, False otherwise
    """
    # Get institution webhook config
    result = await db.execute(
        select(Institution).where(Institution.id == institution_id)
    )
    institution = result.scalar_one_or_none()

    if not institution or not institution.webhook_url:
        logger.debug(f"No webhook configured for institution {institution_id}")
        return False

    # Build payload
    payload = {
        "event_type": event_type,
        "institution_id": institution_id,
        "timestamp": datetime.utcnow().isoformat(),
        "data": event_data,
    }

    # Generate signature if secret configured
    signature = None
    if institution.webhook_secret:
        payload_json = json.dumps(payload, sort_keys=True)
        signature = hmac.new(
            institution.webhook_secret.encode(),
            payload_json.encode(),
            hashlib.sha256,
        ).hexdigest()

    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "IntelliStack-Webhook/1.0",
        "X-IntelliStack-Event": event_type,
        "X-IntelliStack-Delivery-ID": f"{institution_id}-{int(datetime.utcnow().timestamp())}",
    }
    if signature:
        headers["X-IntelliStack-Signature"] = f"sha256={signature}"

    # Send webhook with timeout and retry
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                institution.webhook_url,
                json=payload,
                headers=headers,
            )

            if response.status_code in (200, 201, 202, 204):
                logger.info(
                    f"Webhook sent successfully to {institution.webhook_url} "
                    f"for event {event_type}"
                )
                return True
            else:
                logger.warning(
                    f"Webhook failed with status {response.status_code} "
                    f"for institution {institution_id}, event {event_type}"
                )

                # Retry on 5xx errors
                if response.status_code >= 500 and retry_count < max_retries:
                    await asyncio.sleep(2 ** retry_count)  # Exponential backoff
                    return await send_webhook_event(
                        db,
                        institution_id,
                        event_type,
                        event_data,
                        retry_count + 1,
                        max_retries,
                    )

                return False

    except httpx.TimeoutException:
        logger.error(
            f"Webhook timeout for institution {institution_id}, event {event_type}"
        )
        if retry_count < max_retries:
            await asyncio.sleep(2 ** retry_count)
            return await send_webhook_event(
                db,
                institution_id,
                event_type,
                event_data,
                retry_count + 1,
                max_retries,
            )
        return False

    except Exception as e:
        logger.error(
            f"Webhook error for institution {institution_id}, event {event_type}: {e}"
        )
        return False


async def fire_enrollment_webhook(
    db: AsyncSession,
    institution_id: str,
    cohort_id: str,
    user_id: str,
    enrolled_at: datetime,
) -> None:
    """
    Fire webhook when student is enrolled in cohort.

    Args:
        db: Database session
        institution_id: Institution ID
        cohort_id: Cohort ID
        user_id: Student user ID
        enrolled_at: Enrollment timestamp
    """
    event_data = {
        "cohort_id": cohort_id,
        "user_id": user_id,
        "enrolled_at": enrolled_at.isoformat(),
    }

    await send_webhook_event(
        db,
        institution_id,
        WEBHOOK_EVENT_ENROLLMENT,
        event_data,
    )


async def fire_progress_milestone_webhook(
    db: AsyncSession,
    institution_id: str,
    user_id: str,
    stage_id: str,
    progress_percentage: float,
    milestone: str,
) -> None:
    """
    Fire webhook when student reaches progress milestone.

    Args:
        db: Database session
        institution_id: Institution ID
        user_id: Student user ID
        stage_id: Stage ID
        progress_percentage: Current progress percentage
        milestone: Milestone reached (e.g., "25%", "50%", "75%", "100%")
    """
    event_data = {
        "user_id": user_id,
        "stage_id": stage_id,
        "progress_percentage": progress_percentage,
        "milestone": milestone,
        "timestamp": datetime.utcnow().isoformat(),
    }

    await send_webhook_event(
        db,
        institution_id,
        WEBHOOK_EVENT_PROGRESS,
        event_data,
    )


async def fire_assessment_completion_webhook(
    db: AsyncSession,
    institution_id: str,
    user_id: str,
    assessment_id: str,
    score: float,
    passed: bool,
) -> None:
    """
    Fire webhook when student completes assessment.

    Args:
        db: Database session
        institution_id: Institution ID
        user_id: Student user ID
        assessment_id: Assessment ID
        score: Assessment score
        passed: Whether student passed
    """
    event_data = {
        "user_id": user_id,
        "assessment_id": assessment_id,
        "score": score,
        "passed": passed,
        "timestamp": datetime.utcnow().isoformat(),
    }

    await send_webhook_event(
        db,
        institution_id,
        WEBHOOK_EVENT_ASSESSMENT,
        event_data,
    )
