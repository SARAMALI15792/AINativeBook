import factory
from datetime import datetime, timezone
from uuid import uuid4

from src.core.auth.models import User, Role, UserRole, Session, OAuthAccount, PasswordResetToken, LoginAttempt
from src.core.learning.models import Stage, ContentItem, Badge, Progress, ContentCompletion, UserBadge, Certificate
from src.core.institution.models import Institution, Cohort, CohortEnrollment


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.LazyFunction(lambda: str(uuid4()))
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    password_hash = "hashed_password"
    name = factory.Sequence(lambda n: f"User {n}")
    avatar_url = factory.Faker("image_url")
    bio = factory.Faker("text", max_nb_chars=200)
    locale = factory.Faker("language_code")
    notification_settings = factory.Dict({"email_notifications": True, "push_notifications": False})
    preferences = factory.Dict({"theme": "dark", "notifications_enabled": True})
    is_active = True
    is_verified = factory.Faker("boolean")
    email_verified = factory.Faker("boolean")
    onboarding_completed = factory.Faker("boolean")
    current_stage = 1
    role = "student"


class RoleFactory(factory.Factory):
    class Meta:
        model = Role

    id = factory.LazyFunction(lambda: str(uuid4()))
    name = factory.Faker("word")
    description = factory.Faker("text", max_nb_chars=100)
    permissions = factory.Dict({"read": True, "write": False})


class UserRoleFactory(factory.Factory):
    class Meta:
        model = UserRole

    id = factory.LazyFunction(lambda: str(uuid4()))
    user = factory.SubFactory(UserFactory)
    role = factory.SubFactory(RoleFactory)
    granted_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class StageFactory(factory.Factory):
    class Meta:
        model = Stage

    id = factory.LazyFunction(lambda: str(uuid4()))
    number = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: f"Stage {n}")
    slug = factory.Sequence(lambda n: f"stage-{n}")
    description = factory.Faker("text", max_nb_chars=200)
    learning_objectives = factory.List([factory.Faker("sentence") for _ in range(3)])
    estimated_hours = 40
    content_count = 0
    assessment_count = 0
    is_active = True


class ContentItemFactory(factory.Factory):
    class Meta:
        model = ContentItem

    id = factory.LazyFunction(lambda: str(uuid4()))
    stage = factory.SubFactory(StageFactory)
    title = factory.Faker("sentence", nb_words=4)
    slug = factory.Sequence(lambda n: f"content-{n}")
    content_type = "lesson"
    order = factory.Sequence(lambda n: n)
    estimated_minutes = 30
    is_required = True
    is_active = True


class BadgeFactory(factory.Factory):
    class Meta:
        model = Badge

    id = factory.LazyFunction(lambda: str(uuid4()))
    name = factory.Faker("word")
    description = factory.Faker("text", max_nb_chars=100)
    icon_url = factory.Faker("image_url")
    criteria = factory.Dict({"completion_percentage": 100})
    is_active = True


class ProgressFactory(factory.Factory):
    class Meta:
        model = Progress

    id = factory.LazyFunction(lambda: str(uuid4()))
    user = factory.SubFactory(UserFactory)
    overall_percentage = 0.0
    total_time_spent_minutes = 0
    stage_progress = factory.Dict({})
    started_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    last_activity_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class ContentCompletionFactory(factory.Factory):
    class Meta:
        model = ContentCompletion

    id = factory.LazyFunction(lambda: str(uuid4()))
    progress = factory.SubFactory(ProgressFactory)
    content_item = factory.SubFactory(ContentItemFactory)
    time_spent_minutes = 30


class UserBadgeFactory(factory.Factory):
    class Meta:
        model = UserBadge

    id = factory.LazyFunction(lambda: str(uuid4()))
    user = factory.SubFactory(UserFactory)
    badge = factory.SubFactory(BadgeFactory)
    awarded_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class CertificateFactory(factory.Factory):
    class Meta:
        model = Certificate

    id = factory.LazyFunction(lambda: str(uuid4()))
    user = factory.SubFactory(UserFactory)
    certificate_number = factory.Sequence(lambda n: f"CERT-{n:06d}")
    total_time_spent_hours = 200