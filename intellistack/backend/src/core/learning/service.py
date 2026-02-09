"""Learning service - business logic for stages, progress, badges."""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.config.logging import get_logger
from src.shared.exceptions import NotFoundError, PrerequisiteNotMetError
from src.shared.utils import calculate_percentage, generate_certificate_number, utc_now

from .models import (
    Badge,
    Certificate,
    ContentCompletion,
    ContentItem,
    Progress,
    Stage,
    StageStatus,
    UserBadge,
)
from .schemas import (
    CompleteContentResponse,
    LearningPathResponse,
    StageWithStatus,
    TimeEstimateResponse,
)

logger = get_logger(__name__)


class LearningService:
    """Service for learning management operations."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # === Stage Operations ===

    async def get_all_stages(self) -> list[Stage]:
        """Get all active stages ordered by number."""
        result = await self.session.execute(
            select(Stage)
            .where(Stage.is_active == True)
            .order_by(Stage.number)
        )
        return list(result.scalars().all())

    async def get_stage_by_id(self, stage_id: str) -> Stage:
        """Get a stage by ID."""
        result = await self.session.execute(
            select(Stage)
            .options(selectinload(Stage.content_items))
            .where(Stage.id == stage_id)
        )
        stage = result.scalar_one_or_none()
        if not stage:
            raise NotFoundError(resource="Stage", resource_id=stage_id)
        return stage

    async def get_stage_with_content(self, stage_id: str) -> Stage:
        """Get a stage with its content items."""
        result = await self.session.execute(
            select(Stage)
            .options(selectinload(Stage.content_items))
            .where(Stage.id == stage_id, Stage.is_active == True)
        )
        stage = result.scalar_one_or_none()
        if not stage:
            raise NotFoundError(resource="Stage", resource_id=stage_id)
        return stage

    # === Prerequisite Checking (FR-001) ===

    async def check_prerequisites(self, user_id: str, stage_id: str) -> bool:
        """Check if user can access a stage based on prerequisites."""
        stage = await self.get_stage_by_id(stage_id)

        # Stage 1 has no prerequisites
        if stage.prerequisite_stage_id is None:
            return True

        # Get user's progress
        progress = await self.get_or_create_progress(user_id)

        # Check if prerequisite stage is completed
        prereq_progress = progress.stage_progress.get(stage.prerequisite_stage_id, {})
        prereq_status = prereq_progress.get("status", StageStatus.LOCKED.value)

        return prereq_status == StageStatus.COMPLETED.value

    async def verify_stage_access(self, user_id: str, stage_id: str) -> None:
        """Verify and raise if user cannot access stage."""
        can_access = await self.check_prerequisites(user_id, stage_id)
        if not can_access:
            stage = await self.get_stage_by_id(stage_id)
            prereq = await self.get_stage_by_id(stage.prerequisite_stage_id)
            raise PrerequisiteNotMetError(
                stage_name=stage.name,
                required_stage=prereq.name,
            )

    # === Progress Operations (FR-003) ===

    async def get_or_create_progress(self, user_id: str) -> Progress:
        """Get or create progress record for user."""
        result = await self.session.execute(
            select(Progress).where(Progress.user_id == user_id)
        )
        progress = result.scalar_one_or_none()

        if not progress:
            # Get first stage
            stages = await self.get_all_stages()
            first_stage_id = stages[0].id if stages else None

            progress = Progress(
                user_id=user_id,
                current_stage_id=first_stage_id,
                stage_progress={},
            )
            self.session.add(progress)
            await self.session.flush()

        return progress

    async def get_progress(self, user_id: str) -> Progress:
        """Get user's progress with related data."""
        result = await self.session.execute(
            select(Progress)
            .options(
                selectinload(Progress.content_completions),
                selectinload(Progress.current_stage),
            )
            .where(Progress.user_id == user_id)
        )
        progress = result.scalar_one_or_none()

        if not progress:
            progress = await self.get_or_create_progress(user_id)

        return progress

    async def _calculate_stage_percentage(
        self, progress: Progress, stage_id: str
    ) -> float:
        """Calculate completion percentage for a stage."""
        # Get total required content items in stage
        result = await self.session.execute(
            select(ContentItem)
            .where(
                ContentItem.stage_id == stage_id,
                ContentItem.is_required == True,
                ContentItem.is_active == True,
            )
        )
        total_items = len(result.scalars().all())

        if total_items == 0:
            return 100.0

        # Count completed items
        result = await self.session.execute(
            select(ContentCompletion)
            .join(ContentItem)
            .where(
                ContentCompletion.progress_id == progress.id,
                ContentItem.stage_id == stage_id,
                ContentItem.is_required == True,
            )
        )
        completed_items = len(result.scalars().all())

        return calculate_percentage(completed_items, total_items)

    # === Content Completion ===

    async def complete_content(
        self,
        user_id: str,
        content_id: str,
        time_spent_minutes: int = 0,
        score: Optional[float] = None,
    ) -> CompleteContentResponse:
        """Mark content as complete and update progress."""
        # Get content item
        result = await self.session.execute(
            select(ContentItem)
            .options(selectinload(ContentItem.stage))
            .where(ContentItem.id == content_id)
        )
        content_item = result.scalar_one_or_none()
        if not content_item:
            raise NotFoundError(resource="Content", resource_id=content_id)

        # Verify access
        await self.verify_stage_access(user_id, content_item.stage_id)

        # Get or create progress
        progress = await self.get_or_create_progress(user_id)

        # Check if already completed
        existing = await self.session.execute(
            select(ContentCompletion).where(
                ContentCompletion.progress_id == progress.id,
                ContentCompletion.content_item_id == content_id,
            )
        )
        if existing.scalar_one_or_none():
            # Already completed - just return current state
            stage_pct = await self._calculate_stage_percentage(progress, content_item.stage_id)
            return CompleteContentResponse(
                content_id=content_id,
                completed_at=utc_now(),
                stage_percentage=stage_pct,
                overall_percentage=progress.overall_percentage,
                stage_completed=stage_pct >= 100.0,
            )

        # Create completion record
        completion = ContentCompletion(
            progress_id=progress.id,
            content_item_id=content_id,
            time_spent_minutes=time_spent_minutes,
            score=score,
        )
        self.session.add(completion)

        # Update progress
        progress.total_time_spent_minutes += time_spent_minutes
        progress.last_activity_at = utc_now()

        # Calculate new percentages
        stage_pct = await self._calculate_stage_percentage(progress, content_item.stage_id)

        # Update stage progress
        stage_data = progress.stage_progress.get(content_item.stage_id, {})
        stage_data["percentage"] = stage_pct
        stage_data["last_activity_at"] = utc_now().isoformat()

        if "started_at" not in stage_data:
            stage_data["started_at"] = utc_now().isoformat()
            stage_data["status"] = StageStatus.IN_PROGRESS.value

        # Check if stage completed
        stage_completed = stage_pct >= 100.0
        badge_earned = None

        if stage_completed:
            stage_data["status"] = StageStatus.COMPLETED.value
            stage_data["completed_at"] = utc_now().isoformat()

            # Check and issue badge
            badge_earned = await self._check_and_issue_badge(
                user_id, content_item.stage_id
            )

        progress.stage_progress[content_item.stage_id] = stage_data

        # Recalculate overall percentage
        stages = await self.get_all_stages()
        total_pct = sum(
            progress.stage_progress.get(s.id, {}).get("percentage", 0)
            for s in stages
        )
        progress.overall_percentage = total_pct / len(stages) if stages else 0

        # Get next content
        next_content = await self._get_next_content(content_item)

        await self.session.flush()

        logger.info(
            "Content completed",
            user_id=user_id,
            content_id=content_id,
            stage_percentage=stage_pct,
        )

        return CompleteContentResponse(
            content_id=content_id,
            completed_at=utc_now(),
            stage_percentage=stage_pct,
            overall_percentage=progress.overall_percentage,
            badge_earned=badge_earned,
            stage_completed=stage_completed,
            next_content_id=next_content.id if next_content else None,
        )

    async def _get_next_content(self, current: ContentItem) -> Optional[ContentItem]:
        """Get next content item in sequence."""
        result = await self.session.execute(
            select(ContentItem)
            .where(
                ContentItem.stage_id == current.stage_id,
                ContentItem.order > current.order,
                ContentItem.is_active == True,
            )
            .order_by(ContentItem.order)
            .limit(1)
        )
        return result.scalar_one_or_none()

    # === Badge Operations (FR-005) ===

    async def _check_and_issue_badge(
        self, user_id: str, stage_id: str
    ) -> Optional[str]:
        """Check if user earned a badge and issue it."""
        # Get badge for stage
        result = await self.session.execute(
            select(Badge).where(Badge.stage_id == stage_id, Badge.is_active == True)
        )
        badge = result.scalar_one_or_none()

        if not badge:
            return None

        # Check if already awarded
        existing = await self.session.execute(
            select(UserBadge).where(
                UserBadge.user_id == user_id,
                UserBadge.badge_id == badge.id,
            )
        )
        if existing.scalar_one_or_none():
            return None

        # Award badge
        user_badge = UserBadge(
            user_id=user_id,
            badge_id=badge.id,
            awarded_for=f"Completed Stage: {stage_id}",
        )
        self.session.add(user_badge)

        logger.info("Badge awarded", user_id=user_id, badge_name=badge.name)
        return badge.name

    async def get_user_badges(self, user_id: str) -> list[UserBadge]:
        """Get all badges earned by user."""
        result = await self.session.execute(
            select(UserBadge)
            .options(selectinload(UserBadge.badge))
            .where(UserBadge.user_id == user_id)
            .order_by(UserBadge.awarded_at.desc())
        )
        return list(result.scalars().all())

    # === Learning Path Visualization (FR-012) ===

    async def get_learning_path(self, user_id: str) -> LearningPathResponse:
        """Get learning path visualization with stage statuses."""
        progress = await self.get_progress(user_id)
        stages = await self.get_all_stages()
        badges = await self.get_user_badges(user_id)

        stages_with_status: list[StageWithStatus] = []
        current_stage = None
        remaining_hours = 0

        for stage in stages:
            stage_data = progress.stage_progress.get(stage.id, {})
            status = stage_data.get("status", StageStatus.LOCKED.value)
            percentage = stage_data.get("percentage", 0.0)

            # Determine accessibility
            can_access = await self.check_prerequisites(user_id, stage.id)

            # If can access but not started, mark as available
            if can_access and status == StageStatus.LOCKED.value:
                status = StageStatus.AVAILABLE.value

            stage_with_status = StageWithStatus(
                id=stage.id,
                number=stage.number,
                name=stage.name,
                slug=stage.slug,
                description=stage.description,
                learning_objectives=stage.learning_objectives,
                estimated_hours=stage.estimated_hours,
                content_count=stage.content_count,
                prerequisite_stage_id=stage.prerequisite_stage_id,
                is_active=stage.is_active,
                status=status,
                percentage_complete=percentage,
                is_accessible=can_access,
            )
            stages_with_status.append(stage_with_status)

            # Track current stage
            if status == StageStatus.IN_PROGRESS.value:
                current_stage = stage_with_status

            # Calculate remaining hours
            if status != StageStatus.COMPLETED.value:
                hours_done = (percentage / 100) * stage.estimated_hours
                remaining_hours += stage.estimated_hours - hours_done

        return LearningPathResponse(
            user_id=user_id,
            overall_percentage=progress.overall_percentage,
            current_stage=current_stage,
            stages=stages_with_status,
            total_badges_earned=len(badges),
            estimated_hours_remaining=int(remaining_hours),
        )

    # === Time Estimation (FR-007) ===

    async def calculate_time_estimate(
        self, user_id: str, stage_id: str
    ) -> TimeEstimateResponse:
        """Calculate estimated time to complete a stage."""
        stage = await self.get_stage_by_id(stage_id)
        progress = await self.get_progress(user_id)

        stage_data = progress.stage_progress.get(stage_id, {})
        percentage = stage_data.get("percentage", 0.0)

        remaining_pct = 100 - percentage
        remaining_hours = (remaining_pct / 100) * stage.estimated_hours

        return TimeEstimateResponse(
            stage_id=stage_id,
            estimated_hours_remaining=round(remaining_hours, 1),
            based_on_user_pace=False,
            average_completion_rate=1.0,
        )

    # === Certificate Generation (FR-014) ===

    async def generate_certificate(self, user_id: str) -> Certificate:
        """Generate completion certificate after all stages complete."""
        progress = await self.get_progress(user_id)

        # Verify all stages completed
        if progress.overall_percentage < 100:
            raise ValueError("Cannot generate certificate - course not completed")

        # Check if certificate already exists
        result = await self.session.execute(
            select(Certificate).where(Certificate.user_id == user_id)
        )
        existing = result.scalar_one_or_none()
        if existing:
            return existing

        # Create certificate
        certificate = Certificate(
            user_id=user_id,
            certificate_number=generate_certificate_number(),
            total_time_spent_hours=progress.total_time_spent_minutes // 60,
        )
        self.session.add(certificate)
        await self.session.flush()

        logger.info(
            "Certificate generated",
            user_id=user_id,
            certificate_number=certificate.certificate_number,
        )

        return certificate

    async def get_certificate(self, user_id: str) -> Optional[Certificate]:
        """Get user's certificate if exists."""
        result = await self.session.execute(
            select(Certificate).where(Certificate.user_id == user_id)
        )
        return result.scalar_one_or_none()
