"""Seed database with initial data for development and testing."""

import asyncio
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession

from src.config.settings import get_settings
from src.shared.database import init_db, get_session, Base, _engine
from src.core.auth.models import User, Role, UserRole, RoleName
from src.core.learning.models import Stage, ContentItem, Badge


async def seed_roles(session: AsyncSession) -> dict[str, Role]:
    """Create predefined roles."""
    roles = {}
    role_definitions = [
        {
            "name": RoleName.STUDENT.value,
            "description": "Learning access, community participation",
            "permissions": {"read:content": True, "submit:assessment": True},
        },
        {
            "name": RoleName.AUTHOR.value,
            "description": "Content creation, review participation",
            "permissions": {"read:content": True, "write:content": True, "review:content": True},
        },
        {
            "name": RoleName.INSTRUCTOR.value,
            "description": "Cohort management, assessment grading",
            "permissions": {"read:content": True, "grade:assessment": True, "manage:cohort": True},
        },
        {
            "name": RoleName.INSTITUTION_ADMIN.value,
            "description": "Institution management, analytics",
            "permissions": {"manage:institution": True, "read:analytics": True},
        },
        {
            "name": RoleName.PLATFORM_ADMIN.value,
            "description": "Full system access",
            "permissions": {"admin": True},
        },
    ]

    for role_def in role_definitions:
        role = Role(**role_def)
        session.add(role)
        roles[role_def["name"]] = role

    await session.flush()
    print(f"✓ Created {len(roles)} roles")
    return roles


async def seed_stages(session: AsyncSession) -> list[Stage]:
    """Create the 5 learning stages."""
    stages_data = [
        {
            "number": 1,
            "name": "Foundations",
            "slug": "foundations",
            "description": "Python programming, Linux basics, and introduction to robotics concepts",
            "learning_objectives": [
                "Master Python programming fundamentals",
                "Navigate Linux command line confidently",
                "Understand basic robotics terminology and concepts",
                "Set up a development environment",
            ],
            "estimated_hours": 40,
            "prerequisite_stage_id": None,
        },
        {
            "number": 2,
            "name": "ROS 2 & Simulation",
            "slug": "ros2-simulation",
            "description": "Robot Operating System 2 fundamentals and Gazebo simulation",
            "learning_objectives": [
                "Understand ROS 2 architecture and concepts",
                "Create and manage ROS 2 packages",
                "Work with topics, services, and actions",
                "Simulate robots in Gazebo",
            ],
            "estimated_hours": 60,
            "prerequisite_stage_id": None,  # Will be set after first stage created
        },
        {
            "number": 3,
            "name": "Perception & Planning",
            "slug": "perception-planning",
            "description": "Computer vision, sensor fusion, and motion planning algorithms",
            "learning_objectives": [
                "Implement computer vision algorithms",
                "Process and fuse sensor data",
                "Understand motion planning fundamentals",
                "Implement path planning algorithms",
            ],
            "estimated_hours": 80,
            "prerequisite_stage_id": None,
        },
        {
            "number": 4,
            "name": "AI Integration",
            "slug": "ai-integration",
            "description": "Machine learning for robotics and LLM integration",
            "learning_objectives": [
                "Apply ML models to robotics tasks",
                "Integrate large language models",
                "Implement reinforcement learning",
                "Build end-to-end AI pipelines",
            ],
            "estimated_hours": 80,
            "prerequisite_stage_id": None,
        },
        {
            "number": 5,
            "name": "Capstone Project",
            "slug": "capstone",
            "description": "Build a complete humanoid robot application from concept to deployment",
            "learning_objectives": [
                "Design a complete robotics system",
                "Integrate multiple subsystems",
                "Test and validate in simulation",
                "Prepare for real-world deployment",
            ],
            "estimated_hours": 100,
            "prerequisite_stage_id": None,
        },
    ]

    stages = []
    for data in stages_data:
        stage = Stage(**data)
        session.add(stage)
        stages.append(stage)

    await session.flush()

    # Set prerequisites
    for i, stage in enumerate(stages[1:], 1):
        stage.prerequisite_stage_id = stages[i - 1].id

    await session.flush()
    print(f"✓ Created {len(stages)} stages")
    return stages


async def seed_badges(session: AsyncSession, stages: list[Stage]) -> list[Badge]:
    """Create badges for each stage."""
    badges = []
    badge_data = [
        ("Foundation Builder", "Completed the Foundations stage", "🏗️"),
        ("ROS Master", "Completed ROS 2 & Simulation stage", "🤖"),
        ("Perception Pioneer", "Completed Perception & Planning stage", "👁️"),
        ("AI Integrator", "Completed AI Integration stage", "🧠"),
        ("Capstone Champion", "Completed the Capstone project", "🏆"),
    ]

    for i, (name, description, icon) in enumerate(badge_data):
        badge = Badge(
            name=name,
            description=description,
            icon_url=icon,
            stage_id=stages[i].id,
            criteria={"stage_completion": True},
        )
        session.add(badge)
        badges.append(badge)

    await session.flush()
    print(f"✓ Created {len(badges)} badges")
    return badges


async def seed_content(session: AsyncSession, stages: list[Stage]) -> None:
    """Create sample content items for stages."""
    content_templates = {
        0: [  # Foundations
            ("Introduction to Python", "lesson", 30),
            ("Variables and Data Types", "lesson", 45),
            ("Control Flow", "lesson", 45),
            ("Functions and Modules", "lesson", 60),
            ("Python Practice Exercises", "exercise", 90),
            ("Linux Command Line Basics", "lesson", 45),
            ("File System Navigation", "exercise", 30),
            ("Introduction to Robotics", "lesson", 30),
            ("Foundations Quiz", "quiz", 30),
        ],
        1: [  # ROS 2
            ("ROS 2 Architecture Overview", "lesson", 45),
            ("Installing ROS 2", "lesson", 30),
            ("Creating Your First Package", "exercise", 60),
            ("Topics and Publishers", "lesson", 45),
            ("Services and Clients", "lesson", 45),
            ("Actions", "lesson", 45),
            ("Launch Files", "lesson", 30),
            ("Introduction to Gazebo", "lesson", 45),
            ("Simulating a Robot", "exercise", 90),
            ("ROS 2 Assessment", "quiz", 45),
        ],
        2: [  # Perception
            ("Computer Vision Fundamentals", "lesson", 60),
            ("Image Processing with OpenCV", "exercise", 90),
            ("Object Detection", "lesson", 60),
            ("Sensor Types and Data", "lesson", 45),
            ("Sensor Fusion Basics", "lesson", 60),
            ("SLAM Introduction", "lesson", 60),
            ("Motion Planning Basics", "lesson", 60),
            ("Path Planning Algorithms", "exercise", 90),
            ("Perception Project", "exercise", 120),
        ],
        3: [  # AI
            ("ML for Robotics Overview", "lesson", 45),
            ("Training Vision Models", "exercise", 90),
            ("Reinforcement Learning Basics", "lesson", 60),
            ("RL for Robot Control", "exercise", 120),
            ("LLM Integration", "lesson", 60),
            ("Building AI Pipelines", "exercise", 90),
            ("AI Integration Project", "exercise", 180),
        ],
        4: [  # Capstone
            ("Project Planning", "lesson", 60),
            ("System Design", "exercise", 120),
            ("Integration Phase 1", "exercise", 240),
            ("Integration Phase 2", "exercise", 240),
            ("Testing and Validation", "exercise", 180),
            ("Final Presentation", "exercise", 120),
        ],
    }

    total_content = 0
    for stage_idx, items in content_templates.items():
        stage = stages[stage_idx]
        for order, (title, content_type, minutes) in enumerate(items):
            content = ContentItem(
                stage_id=stage.id,
                title=title,
                slug=title.lower().replace(" ", "-"),
                content_type=content_type,
                order=order,
                estimated_minutes=minutes,
                is_required=True,
            )
            session.add(content)
            total_content += 1

        # Update stage content count
        stage.content_count = len(items)

    await session.flush()
    print(f"✓ Created {total_content} content items")


async def seed_test_user(session: AsyncSession, roles: dict[str, Role]) -> User:
    """Create a test user for development."""
    from passlib.hash import bcrypt

    user = User(
        id="test-user-id",
        email="test@intellistack.dev",
        password_hash=bcrypt.hash("testpassword123"),
        name="Test Student",
        is_active=True,
        is_verified=True,
    )
    session.add(user)
    await session.flush()

    # Assign student role
    user_role = UserRole(
        user_id=user.id,
        role_id=roles[RoleName.STUDENT.value].id,
    )
    session.add(user_role)

    await session.flush()
    print(f"✓ Created test user: {user.email}")
    return user


async def main() -> None:
    """Run all seed functions."""
    print("\n🌱 Seeding IntelliStack database...\n")

    settings = get_settings()
    init_db(settings)

    # Create tables
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Database tables created\n")

    # Seed data
    async for session in get_session():
        roles = await seed_roles(session)
        stages = await seed_stages(session)
        await seed_badges(session, stages)
        await seed_content(session, stages)
        await seed_test_user(session, roles)
        await session.commit()

    print("\n✅ Database seeding complete!\n")


if __name__ == "__main__":
    asyncio.run(main())
