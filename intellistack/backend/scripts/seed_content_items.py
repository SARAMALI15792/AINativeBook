"""Seed content_items table from Docusaurus markdown files."""

import asyncio
import os
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.database import _async_session_factory
from src.core.learning.models import ContentItem, Stage


async def seed_content_items():
    """Populate content_items table from Docusaurus docs directory."""
    if _async_session_factory is None:
        print("Error: Database not initialized")
        return

    # Define content structure based on actual files
    content_structure = {
        "stage-1": [
            {"title": "Introduction to Stage 1", "slug": "intro", "path": "stage-1/intro", "order": 1, "type": "lesson", "minutes": 15},
            {"title": "Linux Theory", "slug": "linux-theory", "path": "stage-1/linux/1-1-linux-theory", "order": 2, "type": "lesson", "minutes": 45},
            {"title": "File Systems", "slug": "file-systems", "path": "stage-1/linux/1-2-file-systems", "order": 3, "type": "lesson", "minutes": 40},
            {"title": "Process Management", "slug": "process-management", "path": "stage-1/linux/1-3-process-management", "order": 4, "type": "lesson", "minutes": 40},
            {"title": "Python Axioms", "slug": "python-axioms", "path": "stage-1/python/1-2-python-axioms", "order": 5, "type": "lesson", "minutes": 50},
            {"title": "Async Theory", "slug": "async-theory", "path": "stage-1/python/1-3-async-theory", "order": 6, "type": "lesson", "minutes": 60},
            {"title": "Linear Algebra", "slug": "linear-algebra", "path": "stage-1/math/1-4-linear-algebra", "order": 7, "type": "lesson", "minutes": 90},
            {"title": "Calculus & Dynamics", "slug": "calculus-dynamics", "path": "stage-1/math/1-5-calculus-dynamics", "order": 8, "type": "lesson", "minutes": 90},
            {"title": "Git History", "slug": "git-history", "path": "stage-1/git/1-6-git-history", "order": 9, "type": "lesson", "minutes": 35},
            {"title": "Bash Shell", "slug": "bash-shell", "path": "stage-1/linux/1-7-bash-shell", "order": 10, "type": "lesson", "minutes": 45},
        ],
        "stage-2": [
            {"title": "Introduction to Stage 2", "slug": "intro", "path": "stage-2/intro", "order": 1, "type": "lesson", "minutes": 15},
            {"title": "Distributed Mind", "slug": "distributed-mind", "path": "stage-2/graph-theory/2-1-distributed-mind", "order": 2, "type": "lesson", "minutes": 60},
            {"title": "Pub/Sub Pattern", "slug": "pub-sub", "path": "stage-2/middleware/2-2-pub-sub", "order": 3, "type": "lesson", "minutes": 50},
            {"title": "Services & Actions", "slug": "services-actions", "path": "stage-2/services/2-3-services-actions", "order": 4, "type": "lesson", "minutes": 55},
            {"title": "Coordinate Frames", "slug": "coordinate-frames", "path": "stage-2/tf2/2-4-coordinate-frames", "order": 5, "type": "lesson", "minutes": 70},
            {"title": "ROS 2 Setup", "slug": "ros2-setup", "path": "stage-2/ros2-setup", "order": 6, "type": "lesson", "minutes": 40},
            {"title": "Gazebo Simulation", "slug": "gazebo-simulation", "path": "stage-2/gazebo-simulation", "order": 7, "type": "lesson", "minutes": 50},
        ],
        "stage-3": [
            {"title": "Introduction to Stage 3", "slug": "intro", "path": "stage-3/intro", "order": 1, "type": "lesson", "minutes": 15},
            {"title": "Computer Vision", "slug": "computer-vision", "path": "stage-3/computer-vision", "order": 2, "type": "lesson", "minutes": 90},
        ],
        "stage-4": [
            {"title": "Introduction to Stage 4", "slug": "intro", "path": "stage-4/intro", "order": 1, "type": "lesson", "minutes": 15},
            {"title": "Machine Learning Basics", "slug": "machine-learning-basics", "path": "stage-4/machine-learning-basics", "order": 2, "type": "lesson", "minutes": 120},
        ],
        "stage-5": [
            {"title": "Introduction to Stage 5", "slug": "intro", "path": "stage-5/intro", "order": 1, "type": "lesson", "minutes": 15},
            {"title": "Project Guidelines", "slug": "project-guidelines", "path": "stage-5/project-guidelines", "order": 2, "type": "lesson", "minutes": 60},
        ],
    }

    async with _async_session_factory() as session:
        # Check if content already exists
        result = await session.execute(select(ContentItem).limit(1))
        if result.scalar_one_or_none():
            print("Content items already exist. Skipping seed.")
            return

        # Get all stages
        result = await session.execute(select(Stage).order_by(Stage.number))
        stages = result.scalars().all()
        
        if not stages:
            print("Error: No stages found. Please seed stages first.")
            return

        stage_map = {f"stage-{stage.number}": stage.id for stage in stages}
        
        print(f"Found {len(stages)} stages")
        print("Seeding content items...")

        total_items = 0
        for stage_key, items in content_structure.items():
            if stage_key not in stage_map:
                print(f"Warning: Stage {stage_key} not found in database")
                continue

            stage_id = stage_map[stage_key]
            for item_data in items:
                content_item = ContentItem(
                    stage_id=stage_id,
                    title=item_data["title"],
                    slug=item_data["slug"],
                    content_path=item_data["path"],
                    content_type=item_data["type"],
                    order=item_data["order"],
                    estimated_minutes=item_data["minutes"],
                    is_required=True,
                    is_active=True,
                )
                session.add(content_item)
                total_items += 1

        await session.commit()
        print(f"✓ Successfully seeded {total_items} content items")


if __name__ == "__main__":
    # Initialize database
    from src.config.settings import get_settings
    from src.shared.database import init_db
    
    settings = get_settings()
    init_db(settings)
    
    asyncio.run(seed_content_items())
