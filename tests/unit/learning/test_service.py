import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

from sqlalchemy import select
from intellistack.backend.src.core.learning.service import LearningService
from intellistack.backend.src.core.learning.models import (
    Stage, ContentItem, Progress, ContentCompletion, Badge, UserBadge
)
from intellistack.backend.src.shared.exceptions import NotFoundError, PrerequisiteNotMetError
from tests.factories import (
    UserFactory, StageFactory, ContentItemFactory, ProgressFactory, ContentCompletionFactory
)


class TestLearningService:
    """Test the LearningService class methods."""

    async def test_get_all_stages(self, db_session):
        """Test getting all active stages."""
        # Create test stages
        stage1 = StageFactory(number=1, name="Stage 1", slug="stage-1", is_active=True)
        stage2 = StageFactory(number=2, name="Stage 2", slug="stage-2", is_active=True)
        inactive_stage = StageFactory(number=3, name="Inactive Stage", slug="inactive-stage", is_active=False)

        db_session.add_all([stage1, stage2, inactive_stage])
        await db_session.commit()

        service = LearningService(db_session)
        stages = await service.get_all_stages()

        assert len(stages) == 2  # Only active stages
        assert stages[0].number == 1
        assert stages[1].number == 2
        assert all(stage.is_active for stage in stages)

    async def test_get_stage_by_id(self, db_session):
        """Test getting a stage by ID."""
        stage = StageFactory()
        db_session.add(stage)
        await db_session.commit()

        service = LearningService(db_session)
        retrieved_stage = await service.get_stage_by_id(stage.id)

        assert retrieved_stage.id == stage.id
        assert retrieved_stage.name == stage.name
        assert retrieved_stage.number == stage.number

    async def test_get_stage_by_id_not_found(self, db_session):
        """Test getting a non-existent stage."""
        service = LearningService(db_session)

        with pytest.raises(NotFoundError):
            await service.get_stage_by_id("non-existent-id")

    async def test_check_prerequisites_no_prereq(self, db_session):
        """Test checking prerequisites for a stage with no prerequisites."""
        stage = StageFactory(prerequisite_stage_id=None)
        user = UserFactory()

        db_session.add_all([stage, user])
        await db_session.commit()

        service = LearningService(db_session)
        result = await service.check_prerequisites(user.id, stage.id)

        assert result is True

    async def test_check_prerequisites_with_prereq_completed(self, db_session):
        """Test checking prerequisites for a stage with completed prerequisite."""
        prereq_stage = StageFactory(number=1, name="Prerequisite Stage", slug="prereq")
        target_stage = StageFactory(
            number=2,
            name="Target Stage",
            slug="target",
            prerequisite_stage_id=prereq_stage.id
        )
        user = UserFactory()

        # Create progress with prerequisite stage completed
        progress = ProgressFactory(
            user=user,
            stage_progress={
                prereq_stage.id: {
                    "status": "completed",
                    "percentage": 100.0
                }
            }
        )

        db_session.add_all([prereq_stage, target_stage, user, progress])
        await db_session.commit()

        service = LearningService(db_session)
        result = await service.check_prerequisites(user.id, target_stage.id)

        assert result is True

    async def test_check_prerequisites_with_prereq_not_completed(self, db_session):
        """Test checking prerequisites for a stage with uncompleted prerequisite."""
        prereq_stage = StageFactory(number=1, name="Prerequisite Stage", slug="prereq")
        target_stage = StageFactory(
            number=2,
            name="Target Stage",
            slug="target",
            prerequisite_stage_id=prereq_stage.id
        )
        user = UserFactory()

        # Create progress with prerequisite stage not completed
        progress = ProgressFactory(
            user=user,
            stage_progress={
                prereq_stage.id: {
                    "status": "in_progress",
                    "percentage": 50.0
                }
            }
        )

        db_session.add_all([prereq_stage, target_stage, user, progress])
        await db_session.commit()

        service = LearningService(db_session)
        result = await service.check_prerequisites(user.id, target_stage.id)

        assert result is False

    async def test_get_or_create_progress(self, db_session):
        """Test getting or creating progress for a user."""
        user = UserFactory()
        db_session.add(user)
        await db_session.commit()

        service = LearningService(db_session)
        progress = await service.get_or_create_progress(user.id)

        assert progress.user_id == user.id
        assert progress.stage_progress == {}

    async def test_get_or_create_progress_existing(self, db_session):
        """Test getting existing progress for a user."""
        user = UserFactory()
        existing_progress = ProgressFactory(user=user)

        db_session.add_all([user, existing_progress])
        await db_session.commit()

        service = LearningService(db_session)
        progress = await service.get_or_create_progress(user.id)

        assert progress.id == existing_progress.id
        assert progress.user_id == user.id

    async def test_complete_content_success(self, db_session):
        """Test successfully completing content."""
        user = UserFactory()
        stage = StageFactory(number=1, name="Stage 1", slug="stage-1")
        content_item = ContentItemFactory(stage=stage)

        db_session.add_all([user, stage, content_item])
        await db_session.commit()

        service = LearningService(db_session)

        result = await service.complete_content(
            user_id=user.id,
            content_id=content_item.id,
            time_spent_minutes=30,
            score=85.0
        )

        # Check result
        assert result.content_id == content_item.id
        assert result.stage_percentage >= 0
        assert result.overall_percentage >= 0

        # Check that completion was created
        result = await db_session.execute(
            select(ContentCompletion).where(
                ContentCompletion.content_item_id == content_item.id
            )
        )
        completion = result.scalar_one_or_none()
        assert completion is not None
        assert completion.time_spent_minutes == 30
        assert completion.score == 85.0

    async def test_complete_content_not_found(self, db_session):
        """Test completing non-existent content raises error."""
        user = UserFactory()
        db_session.add(user)
        await db_session.commit()

        service = LearningService(db_session)

        with pytest.raises(NotFoundError):
            await service.complete_content(
                user_id=user.id,
                content_id="non-existent-id",
                time_spent_minutes=30
            )

    async def test_complete_content_prerequisite_not_met(self, db_session):
        """Test completing content when prerequisites aren't met."""
        user = UserFactory()
        prereq_stage = StageFactory(number=1, name="Prereq", slug="prereq")
        target_stage = StageFactory(
            number=2,
            name="Target",
            slug="target",
            prerequisite_stage_id=prereq_stage.id
        )
        content_item = ContentItemFactory(stage=target_stage)

        db_session.add_all([user, prereq_stage, target_stage, content_item])
        await db_session.commit()

        service = LearningService(db_session)

        with pytest.raises(PrerequisiteNotMetError):
            await service.complete_content(
                user_id=user.id,
                content_id=content_item.id,
                time_spent_minutes=30
            )

    async def test_get_learning_path(self, db_session):
        """Test getting the learning path for a user."""
        user = UserFactory()
        stage1 = StageFactory(number=1, name="Stage 1", slug="stage-1", is_active=True)
        stage2 = StageFactory(number=2, name="Stage 2", slug="stage-2", is_active=True, prerequisite_stage_id=stage1.id)

        # Create progress with some completion
        progress = ProgressFactory(
            user=user,
            overall_percentage=50.0,
            stage_progress={
                stage1.id: {
                    "status": "completed",
                    "percentage": 100.0
                },
                stage2.id: {
                    "status": "in_progress",
                    "percentage": 25.0
                }
            }
        )

        db_session.add_all([user, stage1, stage2, progress])
        await db_session.commit()

        service = LearningService(db_session)
        learning_path = await service.get_learning_path(user.id)

        assert learning_path.user_id == user.id
        assert learning_path.overall_percentage == 50.0
        assert len(learning_path.stages) == 2

        # Check the stages
        stage_data = {stage.id: stage for stage in learning_path.stages}
        assert stage_data[stage1.id].status == "completed"
        assert stage_data[stage1.id].percentage_complete == 100.0
        assert stage_data[stage2.id].status == "available"  # Should be available after first one is complete
        assert stage_data[stage2.id].percentage_complete == 25.0

    async def test_calculate_time_estimate(self, db_session):
        """Test calculating time estimate for stage completion."""
        user = UserFactory()
        stage = StageFactory(estimated_hours=40)

        # Create progress with some completion
        progress = ProgressFactory(
            user=user,
            stage_progress={
                stage.id: {
                    "percentage": 25.0  # 25% complete
                }
            }
        )

        db_session.add_all([user, stage, progress])
        await db_session.commit()

        service = LearningService(db_session)
        estimate = await service.calculate_time_estimate(user.id, stage.id)

        assert estimate.stage_id == stage.id
        assert estimate.estimated_hours_remaining == 30.0  # 75% of 40 hours
        assert estimate.based_on_user_pace is False

    async def test_get_user_badges(self, db_session):
        """Test getting user's earned badges."""
        user = UserFactory()
        stage = StageFactory()
        badge = BadgeFactory(stage=stage)

        user_badge = UserBadge(
            user_id=user.id,
            badge_id=badge.id,
            awarded_for="Completion"
        )

        db_session.add_all([user, stage, badge, user_badge])
        await db_session.commit()

        service = LearningService(db_session)
        user_badges = await service.get_user_badges(user.id)

        assert len(user_badges) == 1
        assert user_badges[0].user_id == user.id
        assert user_badges[0].badge_id == badge.id


class TestLearningServiceCalculateStagePercentage:
    """Test the _calculate_stage_percentage method."""

    async def test_calculate_stage_percentage_no_content(self, db_session):
        """Test calculating percentage when stage has no content."""
        user = UserFactory()
        stage = StageFactory()
        progress = ProgressFactory(user=user)

        db_session.add_all([user, stage, progress])
        await db_session.commit()

        service = LearningService(db_session)
        percentage = await service._calculate_stage_percentage(progress, stage.id)

        assert percentage == 100.0

    async def test_calculate_stage_percentage_with_content(self, db_session):
        """Test calculating percentage with content items."""
        user = UserFactory()
        stage = StageFactory()
        progress = ProgressFactory(user=user)

        # Create 4 required content items
        content1 = ContentItemFactory(stage=stage, is_required=True)
        content2 = ContentItemFactory(stage=stage, is_required=True)
        content3 = ContentItemFactory(stage=stage, is_required=True)
        content4 = ContentItemFactory(stage=stage, is_required=True)

        # Complete 2 of them
        completion1 = ContentCompletionFactory(progress=progress, content_item=content1)
        completion2 = ContentCompletionFactory(progress=progress, content_item=content2)

        db_session.add_all([user, stage, progress, content1, content2, content3, content4, completion1, completion2])
        await db_session.commit()

        service = LearningService(db_session)
        percentage = await service._calculate_stage_percentage(progress, stage.id)

        assert percentage == 50.0  # 2 out of 4 completed


class TestLearningServiceCheckAndIssueBadge:
    """Test the _check_and_issue_badge method."""

    async def test_check_and_issue_badge_new_badge(self, db_session):
        """Test issuing a new badge."""
        user = UserFactory()
        stage = StageFactory()
        badge = BadgeFactory(stage=stage, is_active=True)

        db_session.add_all([user, stage, badge])
        await db_session.commit()

        service = LearningService(db_session)
        badge_name = await service._check_and_issue_badge(user.id, stage.id)

        assert badge_name == badge.name

        # Verify the badge was actually awarded
        result = await db_session.execute(
            select(UserBadge).where(
                UserBadge.user_id == user.id,
                UserBadge.badge_id == badge.id
            )
        )
        user_badge = result.scalar_one_or_none()
        assert user_badge is not None
        assert user_badge.awarded_for == f"Completed Stage: {stage.id}"

    async def test_check_and_issue_badge_already_awarded(self, db_session):
        """Test not issuing a badge that's already been awarded."""
        user = UserFactory()
        stage = StageFactory()
        badge = BadgeFactory(stage=stage, is_active=True)

        # Award the badge first
        existing_user_badge = UserBadge(
            user_id=user.id,
            badge_id=badge.id,
            awarded_for="Previously awarded"
        )

        db_session.add_all([user, stage, badge, existing_user_badge])
        await db_session.commit()

        service = LearningService(db_session)
        badge_name = await service._check_and_issue_badge(user.id, stage.id)

        assert badge_name is None