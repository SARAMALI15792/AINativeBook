"""Simple seed script without Unicode issues."""

import asyncio
import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).parent / "src"))

from sqlalchemy.ext.asyncio import AsyncSession
from src.config.settings import get_settings
from src.shared.database import init_db, get_session, Base, _engine
from src.core.auth.models import User, Role, UserRole, RoleName
from src.core.auth.service import get_password_hash


async def seed_roles(session: AsyncSession):
    """Create predefined roles."""
    role_definitions = [
        {"name": "student", "description": "Student role", "permissions": {"read:content": True}},
        {"name": "author", "description": "Author role", "permissions": {"write:content": True}},
        {"name": "instructor", "description": "Instructor role", "permissions": {"manage:cohort": True}},
        {"name": "institution_admin", "description": "Institution admin role", "permissions": {"manage:institution": True}},
        {"name": "platform_admin", "description": "Platform admin role", "permissions": {"admin": True}},
    ]

    for role_def in role_definitions:
        role = Role(**role_def)
        session.add(role)

    await session.flush()
    print("Created 5 roles")


async def seed_learning_stages(session: AsyncSession):
    """Create the 5 learning stages with content items and badges."""
    from src.core.learning.models import Stage, ContentItem, Badge

    stages_def = [
        {
            "number": 1,
            "name": "Foundations",
            "slug": "foundations",
            "description": "Build a strong base in mathematics, physics, and Python programming essential for robotics and AI development.",
            "learning_objectives": [
                "Apply linear algebra and calculus to robotics problems",
                "Understand Newtonian mechanics for rigid body dynamics",
                "Write proficient Python code with NumPy and SciPy",
                "Explain core AI/ML concepts at a conceptual level",
            ],
            "estimated_hours": 40,
            "content_items": [
                {"title": "Mathematics for Robotics", "slug": "math-basics", "content_type": "lesson", "order": 1, "estimated_minutes": 90},
                {"title": "Physics for Robotics", "slug": "physics-robotics", "content_type": "lesson", "order": 2, "estimated_minutes": 90},
                {"title": "Python Programming Essentials", "slug": "python-programming", "content_type": "lesson", "order": 3, "estimated_minutes": 120},
                {"title": "Introduction to AI Concepts", "slug": "intro-ai", "content_type": "lesson", "order": 4, "estimated_minutes": 60},
                {"title": "Foundations Assessment", "slug": "foundations-assessment", "content_type": "quiz", "order": 5, "estimated_minutes": 45},
            ],
            "badge_name": "Foundation Builder",
            "badge_desc": "Completed the Foundations stage, demonstrating solid math, physics, and programming fundamentals.",
        },
        {
            "number": 2,
            "name": "ROS 2 & Simulation",
            "slug": "ros2-simulation",
            "description": "Master ROS 2 concepts, Gazebo simulation, and NVIDIA Isaac Sim for virtual robot development.",
            "learning_objectives": [
                "Create and manage ROS 2 nodes, topics, and services",
                "Build robot models in Gazebo with URDF/SDF",
                "Run physics simulations in NVIDIA Isaac Sim",
                "Use TF2 for coordinate frame transformations",
            ],
            "estimated_hours": 50,
            "content_items": [
                {"title": "ROS 2 Core Concepts", "slug": "ros2-core", "content_type": "lesson", "order": 1, "estimated_minutes": 120},
                {"title": "Gazebo Simulation", "slug": "gazebo-sim", "content_type": "lesson", "order": 2, "estimated_minutes": 90},
                {"title": "NVIDIA Isaac Sim", "slug": "isaac-sim", "content_type": "lesson", "order": 3, "estimated_minutes": 90},
                {"title": "TF2 & Coordinate Frames", "slug": "tf2-frames", "content_type": "lesson", "order": 4, "estimated_minutes": 60},
                {"title": "ROS 2 & Simulation Assessment", "slug": "ros2-assessment", "content_type": "quiz", "order": 5, "estimated_minutes": 45},
            ],
            "badge_name": "Simulation Specialist",
            "badge_desc": "Completed the ROS 2 & Simulation stage with proficiency in ROS 2, Gazebo, and Isaac Sim.",
        },
        {
            "number": 3,
            "name": "Perception & Planning",
            "slug": "perception-planning",
            "description": "Develop skills in computer vision, SLAM, navigation, and motion planning for autonomous robots.",
            "learning_objectives": [
                "Implement computer vision pipelines with OpenCV",
                "Understand SLAM algorithms for mapping and localization",
                "Configure Nav2 for autonomous navigation",
                "Apply motion planning algorithms for manipulators",
            ],
            "estimated_hours": 45,
            "content_items": [
                {"title": "Computer Vision for Robotics", "slug": "computer-vision", "content_type": "lesson", "order": 1, "estimated_minutes": 90},
                {"title": "SLAM & Localization", "slug": "slam-localization", "content_type": "lesson", "order": 2, "estimated_minutes": 90},
                {"title": "Autonomous Navigation", "slug": "navigation", "content_type": "lesson", "order": 3, "estimated_minutes": 90},
                {"title": "Motion Planning", "slug": "motion-planning", "content_type": "lesson", "order": 4, "estimated_minutes": 60},
                {"title": "Perception & Planning Assessment", "slug": "perception-assessment", "content_type": "quiz", "order": 5, "estimated_minutes": 45},
            ],
            "badge_name": "Perception Expert",
            "badge_desc": "Completed the Perception & Planning stage with mastery of vision, SLAM, and navigation.",
        },
        {
            "number": 4,
            "name": "AI Integration",
            "slug": "ai-integration",
            "description": "Integrate machine learning, reinforcement learning, and LLMs into robotics systems.",
            "learning_objectives": [
                "Train and deploy ML models for robotic perception",
                "Apply reinforcement learning for robot control",
                "Integrate LLMs for natural language robot interaction",
                "Build end-to-end AI-powered robot pipelines",
            ],
            "estimated_hours": 50,
            "content_items": [
                {"title": "ML Fundamentals for Robotics", "slug": "ml-fundamentals", "content_type": "lesson", "order": 1, "estimated_minutes": 90},
                {"title": "Reinforcement Learning", "slug": "reinforcement-learning", "content_type": "lesson", "order": 2, "estimated_minutes": 120},
                {"title": "LLMs for Robotics", "slug": "llms-robotics", "content_type": "lesson", "order": 3, "estimated_minutes": 90},
                {"title": "Integration & Deployment", "slug": "integration-deployment", "content_type": "lesson", "order": 4, "estimated_minutes": 60},
                {"title": "AI Integration Assessment", "slug": "ai-assessment", "content_type": "quiz", "order": 5, "estimated_minutes": 45},
            ],
            "badge_name": "AI Integrator",
            "badge_desc": "Completed the AI Integration stage, capable of building intelligent robot systems.",
        },
        {
            "number": 5,
            "name": "Capstone Project",
            "slug": "capstone",
            "description": "Design, build, test, and demonstrate a complete humanoid robot system integrating all learned skills.",
            "learning_objectives": [
                "Design a complete robot system architecture",
                "Integrate perception, planning, and AI components",
                "Conduct systematic testing and validation",
                "Present and demonstrate the working system",
            ],
            "estimated_hours": 60,
            "content_items": [
                {"title": "Project Design & Architecture", "slug": "project-design", "content_type": "lesson", "order": 1, "estimated_minutes": 120},
                {"title": "Build & Integrate", "slug": "build-integrate", "content_type": "lesson", "order": 2, "estimated_minutes": 180},
                {"title": "Testing & Validation", "slug": "testing-validation", "content_type": "lesson", "order": 3, "estimated_minutes": 120},
                {"title": "Demo & Presentation", "slug": "demo-presentation", "content_type": "lesson", "order": 4, "estimated_minutes": 60},
                {"title": "Capstone Assessment", "slug": "capstone-assessment", "content_type": "quiz", "order": 5, "estimated_minutes": 60},
            ],
            "badge_name": "Robotics Master",
            "badge_desc": "Completed the Capstone Project, demonstrating end-to-end humanoid robotics mastery.",
        },
    ]

    prev_stage_id = None

    for s in stages_def:
        stage_id = str(uuid4())

        stage = Stage(
            id=stage_id,
            number=s["number"],
            name=s["name"],
            slug=s["slug"],
            description=s["description"],
            learning_objectives=s["learning_objectives"],
            estimated_hours=s["estimated_hours"],
            prerequisite_stage_id=prev_stage_id,
            content_count=len([c for c in s["content_items"] if c["content_type"] == "lesson"]),
            assessment_count=len([c for c in s["content_items"] if c["content_type"] == "quiz"]),
        )
        session.add(stage)

        for item in s["content_items"]:
            content = ContentItem(
                id=str(uuid4()),
                stage_id=stage_id,
                title=item["title"],
                slug=item["slug"],
                content_type=item["content_type"],
                order=item["order"],
                estimated_minutes=item["estimated_minutes"],
            )
            session.add(content)

        badge = Badge(
            id=str(uuid4()),
            stage_id=stage_id,
            name=s["badge_name"],
            description=s["badge_desc"],
            criteria={"stage_completed": True, "stage_number": s["number"]},
        )
        session.add(badge)

        prev_stage_id = stage_id

    await session.flush()
    total_items = sum(len(s["content_items"]) for s in stages_def)
    print(f"Created 5 learning stages with {total_items} content items and 5 badges")


async def main():
    """Run seed functions."""
    print("\nSeeding database...")

    settings = get_settings()
    init_db(settings)

    # Create tables
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created")

    # Seed data
    async for session in get_session():
        try:
            await seed_roles(session)
            await seed_learning_stages(session)
            await session.commit()
            print("Database seeding complete!")
            break
        except Exception as e:
            print(f"Error: {e}")
            await session.rollback()


if __name__ == "__main__":
    asyncio.run(main())
