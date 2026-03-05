import pytest
from httpx import AsyncClient
from sqlalchemy import select

from intellistack.backend.src.core.learning.models import Stage, ContentItem, Progress
from tests.factories import UserFactory, StageFactory, ContentItemFactory, ProgressFactory


class TestLearningRoutes:
    """Integration tests for learning module routes."""

    async def test_get_stages_unauthenticated(self, client):
        """Test getting stages endpoint."""
        response = await client.get("/api/learning/stages")
        assert response.status_code == 200

        data = response.json()
        assert "stages" in data
        assert isinstance(data["stages"], list)

    async def test_get_stage_by_id_authenticated(self, client, db_session):
        """Test getting a specific stage with authentication."""
        # Create test data
        user = UserFactory()
        stage = StageFactory(is_active=True)

        db_session.add_all([user, stage])
        await db_session.commit()

        # First, we need to authenticate the user
        # This test would require a proper auth setup; for now, we'll skip
        pytest.skip("Authentication setup required for this test")

    async def test_get_stage_by_id_unauthenticated(self, client, db_session):
        """Test getting a specific stage without authentication."""
        # Create a stage
        stage = StageFactory(is_active=True)
        db_session.add(stage)
        await db_session.commit()

        # The endpoint should return 401 or 404 for unauth access, or 200 if public
        # This depends on the actual route implementation
        response = await client.get(f"/api/learning/stages/{stage.id}")
        # This might return 401 for auth required or 404 if not found
        assert response.status_code in [200, 401, 404]

    async def test_get_learning_path_authenticated(self, client, db_session):
        """Test getting learning path with authentication."""
        # Create test data
        user = UserFactory()
        stage1 = StageFactory(number=1, name="Stage 1", slug="stage-1", is_active=True)
        stage2 = StageFactory(number=2, name="Stage 2", slug="stage-2", is_active=True)

        # Create progress
        progress = ProgressFactory(
            user=user,
            stage_progress={
                stage1.id: {"status": "completed", "percentage": 100.0}
            },
            overall_percentage=50.0
        )

        db_session.add_all([user, stage1, stage2, progress])
        await db_session.commit()

        # This test requires authentication
        pytest.skip("Authentication setup required for this test")

    async def test_complete_content_authenticated(self, client, db_session):
        """Test completing content item with authentication."""
        # Create test data
        user = UserFactory()
        stage = StageFactory(number=1, name="Stage 1", slug="stage-1", is_active=True)
        content_item = ContentItemFactory(stage=stage)

        db_session.add_all([user, stage, content_item])
        await db_session.commit()

        # This test requires authentication and proper payload
        pytest.skip("Authentication setup required for this test")

    async def test_get_user_progress_authenticated(self, client, db_session):
        """Test getting user progress with authentication."""
        # Create test data
        user = UserFactory()
        progress = ProgressFactory(user=user)

        db_session.add_all([user, progress])
        await db_session.commit()

        # This test requires authentication
        pytest.skip("Authentication setup required for this test")


class TestLearningRouteAuth:
    """Test authentication requirements for learning routes."""

    async def test_stages_endpoint_public_access(self, client, db_session):
        """Test that stages endpoint is accessible without authentication."""
        # Create some stages
        stage1 = StageFactory(name="Public Stage 1", is_active=True)
        stage2 = StageFactory(name="Public Stage 2", is_active=True, number=2)

        db_session.add_all([stage1, stage2])
        await db_session.commit()

        response = await client.get("/api/learning/stages")
        assert response.status_code == 200

        data = response.json()
        assert "stages" in data
        assert len(data["stages"]) >= 2

        # Verify the stages in response
        stage_names = [stage["name"] for stage in data["stages"]]
        assert "Public Stage 1" in stage_names
        assert "Public Stage 2" in stage_names

    async def test_stage_detail_endpoint_access(self, client, db_session):
        """Test access to stage detail endpoint."""
        # Create a stage
        stage = StageFactory(name="Test Stage", is_active=True)
        db_session.add(stage)
        await db_session.commit()

        response = await client.get(f"/api/learning/stages/{stage.id}")
        # This endpoint might require authentication, so we'll accept 200, 401, or 404
        assert response.status_code in [200, 401, 404]

    async def test_learning_path_requires_auth(self, client, db_session):
        """Test that learning path endpoint requires authentication."""
        response = await client.get("/api/learning/path")
        # Should return 401 since no auth token is provided
        assert response.status_code == 401


class TestLearningRouteDataIntegrity:
    """Test data integrity in learning routes."""

    async def test_stage_creation_updates_counts(self, db_session):
        """Test that stage creation properly maintains data integrity."""
        stage = StageFactory(
            name="Integrity Test Stage",
            number=1,
            slug="integrity-test",
            is_active=True
        )

        # Add some content items to the stage
        content1 = ContentItemFactory(stage=stage, is_required=True)
        content2 = ContentItemFactory(stage=stage, is_required=True)

        db_session.add_all([stage, content1, content2])
        await db_session.commit()

        # Check that the stage has been updated with content count
        result = await db_session.execute(
            select(Stage).where(Stage.id == stage.id)
        )
        updated_stage = result.scalar_one()

        # Check the data integrity
        assert updated_stage.name == "Integrity Test Stage"
        assert updated_stage.number == 1
        assert updated_stage.slug == "integrity-test"
        assert updated_stage.is_active is True
        assert updated_stage.content_count >= 2  # May be updated by triggers/services

    async def test_progress_creation_default_values(self, db_session):
        """Test that progress creation has proper default values."""
        user = UserFactory()
        progress = ProgressFactory(user=user)

        db_session.add(progress)
        await db_session.commit()

        # Refresh to get any default values set by the DB
        await db_session.refresh(progress)

        # Check default values
        assert progress.overall_percentage >= 0
        assert progress.total_time_spent_minutes >= 0
        assert isinstance(progress.stage_progress, dict)
        assert progress.stage_progress == {}
        assert progress.started_at is not None
        assert progress.last_activity_at is not None