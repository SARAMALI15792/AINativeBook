import pytest
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from intellistack.backend.src.core.learning.models import (
    Stage, ContentItem, Badge, Progress, ContentCompletion, UserBadge, Certificate
)
from tests.factories import (
    UserFactory, StageFactory, ContentItemFactory, BadgeFactory,
    ProgressFactory, ContentCompletionFactory, UserBadgeFactory, CertificateFactory
)


class TestStageModel:
    """Test the Stage model and its relationships."""

    async def test_stage_creation(self, db_session):
        """Test creating a stage with valid data."""
        stage = Stage(
            number=1,
            name="Foundations",
            slug="foundations",
            description="Basic concepts and foundations",
            learning_objectives=["Learn basic concepts", "Understand fundamentals"]
        )

        db_session.add(stage)
        await db_session.commit()
        await db_session.refresh(stage)

        assert stage.id is not None
        assert stage.number == 1
        assert stage.name == "Foundations"
        assert stage.slug == "foundations"
        assert stage.description == "Basic concepts and foundations"
        assert stage.learning_objectives == ["Learn basic concepts", "Understand fundamentals"]
        assert stage.is_active is True
        assert stage.created_at is not None

    async def test_stage_unique_constraints(self, db_session):
        """Test unique constraints on number and slug."""
        stage1 = Stage(
            number=1,
            name="Foundations",
            slug="foundations",
            description="Basic concepts"
        )
        db_session.add(stage1)
        await db_session.commit()

        # Try to create another stage with same number
        stage2 = Stage(
            number=1,  # Same number as stage1
            name="Duplicate Number",
            slug="duplicate-number",
            description="Should fail"
        )
        db_session.add(stage2)
        with pytest.raises(IntegrityError):
            await db_session.commit()

        # Rollback and try with same slug
        await db_session.rollback()
        stage3 = Stage(
            number=2,
            name="Duplicate Slug",
            slug="foundations",  # Same slug as stage1
            description="Should also fail"
        )
        db_session.add(stage3)
        with pytest.raises(IntegrityError):
            await db_session.commit()

    async def test_stage_prerequisites(self, db_session):
        """Test stage prerequisite relationships."""
        stage1 = StageFactory(number=1, name="Stage 1", slug="stage-1")
        stage2 = StageFactory(number=2, name="Stage 2", slug="stage-2")

        # Set stage1 as prerequisite for stage2
        stage2.prerequisite_stage_id = stage1.id

        db_session.add_all([stage1, stage2])
        await db_session.commit()

        # Refresh to get the relationships
        await db_session.refresh(stage1)
        await db_session.refresh(stage2)

        assert stage2.prerequisite.id == stage1.id
        assert stage1.id in [s.id for s in stage2.__dict__.get('_sa_instance_state').attrs.prerequisite.loaded_value.id]

    async def test_stage_relationships(self, db_session):
        """Test stage relationships with content items and badges."""
        stage = StageFactory()
        content_item = ContentItemFactory(stage=stage)
        badge = BadgeFactory(stage=stage)

        db_session.add_all([stage, content_item, badge])
        await db_session.commit()

        await db_session.refresh(stage, attribute_names=["content_items", "badges"])

        assert len(stage.content_items) == 1
        assert stage.content_items[0].id == content_item.id
        assert len(stage.badges) == 1
        assert stage.badges[0].id == badge.id


class TestContentItemModel:
    """Test the ContentItem model and its relationships."""

    async def test_content_item_creation(self, db_session):
        """Test creating a content item with valid data."""
        stage = StageFactory()

        content_item = ContentItem(
            stage_id=stage.id,
            title="Introduction to AI",
            slug="intro-ai",
            content_type="lesson",
            order=1,
            estimated_minutes=45,
            is_required=True,
            is_active=True
        )

        db_session.add(content_item)
        await db_session.commit()
        await db_session.refresh(content_item)

        assert content_item.id is not None
        assert content_item.stage_id == stage.id
        assert content_item.title == "Introduction to AI"
        assert content_item.slug == "intro-ai"
        assert content_item.content_type == "lesson"
        assert content_item.order == 1
        assert content_item.estimated_minutes == 45
        assert content_item.is_required is True
        assert content_item.is_active is True
        assert content_item.created_at is not None

    async def test_content_item_foreign_key_constraint(self, db_session):
        """Test that content item requires a valid stage."""
        content_item = ContentItem(
            stage_id="invalid-id",  # Non-existent stage
            title="Invalid Content",
            slug="invalid-content",
            content_type="lesson"
        )

        db_session.add(content_item)
        with pytest.raises(IntegrityError):
            await db_session.commit()


class TestBadgeModel:
    """Test the Badge model and its relationships."""

    async def test_badge_creation(self, db_session):
        """Test creating a badge with valid data."""
        stage = StageFactory()

        badge = Badge(
            stage_id=stage.id,
            name="Completion Badge",
            description="Awarded for completing a stage",
            icon_url="https://example.com/icon.png",
            criteria={"completion_percentage": 100}
        )

        db_session.add(badge)
        await db_session.commit()
        await db_session.refresh(badge)

        assert badge.id is not None
        assert badge.name == "Completion Badge"
        assert badge.description == "Awarded for completing a stage"
        assert badge.icon_url == "https://example.com/icon.png"
        assert badge.criteria == {"completion_percentage": 100}
        assert badge.is_active is True
        assert badge.created_at is not None


class TestProgressModel:
    """Test the Progress model and its relationships."""

    async def test_progress_creation(self, db_session):
        """Test creating a progress record with valid data."""
        user = UserFactory()
        stage = StageFactory()

        progress = Progress(
            user_id=user.id,
            current_stage_id=stage.id,
            overall_percentage=25.0,
            total_time_spent_minutes=120,
            stage_progress={"some_stage_id": {"percentage": 50.0, "status": "in_progress"}}
        )

        db_session.add(progress)
        await db_session.commit()
        await db_session.refresh(progress)

        assert progress.id is not None
        assert progress.user_id == user.id
        assert progress.current_stage_id == stage.id
        assert progress.overall_percentage == 25.0
        assert progress.total_time_spent_minutes == 120
        assert progress.stage_progress == {"some_stage_id": {"percentage": 50.0, "status": "in_progress"}}
        assert progress.started_at is not None
        assert progress.last_activity_at is not None


class TestContentCompletionModel:
    """Test the ContentCompletion model and its relationships."""

    async def test_content_completion_creation(self, db_session):
        """Test creating a content completion record."""
        progress = ProgressFactory()
        content_item = ContentItemFactory()

        completion = ContentCompletion(
            progress_id=progress.id,
            content_item_id=content_item.id,
            time_spent_minutes=30,
            score=85.0
        )

        db_session.add(completion)
        await db_session.commit()
        await db_session.refresh(completion)

        assert completion.id is not None
        assert completion.progress_id == progress.id
        assert completion.content_item_id == content_item.id
        assert completion.time_spent_minutes == 30
        assert completion.score == 85.0
        assert completion.completed_at is not None


class TestUserBadgeModel:
    """Test the UserBadge model and its relationships."""

    async def test_user_badge_creation(self, db_session):
        """Test creating a user badge record."""
        user = UserFactory()
        badge = BadgeFactory()

        user_badge = UserBadge(
            user_id=user.id,
            badge_id=badge.id,
            awarded_for="Completing stage 1"
        )

        db_session.add(user_badge)
        await db_session.commit()
        await db_session.refresh(user_badge)

        assert user_badge.id is not None
        assert user_badge.user_id == user.id
        assert user_badge.badge_id == badge.id
        assert user_badge.awarded_for == "Completing stage 1"
        assert user_badge.awarded_at is not None


class TestCertificateModel:
    """Test the Certificate model and its relationships."""

    async def test_certificate_creation(self, db_session):
        """Test creating a certificate with valid data."""
        user = UserFactory()

        certificate = Certificate(
            user_id=user.id,
            certificate_number="CERT-123456",
            total_time_spent_hours=200,
            final_assessment_score=95.0
        )

        db_session.add(certificate)
        await db_session.commit()
        await db_session.refresh(certificate)

        assert certificate.id is not None
        assert certificate.user_id == user.id
        assert certificate.certificate_number == "CERT-123456"
        assert certificate.total_time_spent_hours == 200
        assert certificate.final_assessment_score == 95.0
        assert certificate.issued_at is not None
        assert certificate.certificate_number is not None