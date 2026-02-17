"""
Summary Generation Service
Auto-generate chapter summaries with key points
Sprint 6: Summary Generation
"""

from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import structlog
import json

from src.core.content.models import Content
from src.core.content.enhanced_models import ContentSummary, SummaryType
from src.ai.shared.llm_client import LLMClient

logger = structlog.get_logger()


class SummaryService:
    """
    Generate content summaries using LLM
    Implements automated summary generation for chapters
    """

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    async def generate_summary(
        self,
        content: Content,
        content_text: str,
        summary_type: str = "brief",
        language_code: str = "en",
        db: Optional[AsyncSession] = None,
    ) -> ContentSummary:
        """
        Generate summary using GPT-4
        Types: brief (2-3 sentences), detailed (paragraph), key_points (bullets)

        Args:
            content: Content object
            content_text: Full content text to summarize
            summary_type: Type of summary ('brief', 'detailed', 'key_points')
            language_code: Language for summary
            db: Database session for persistence

        Returns:
            ContentSummary object
        """
        try:
            # Build summary prompt
            prompt = self._build_summary_prompt(
                content_text=content_text,
                content_title=content.title,
                summary_type=summary_type,
            )

            # Call LLM
            response = await self.llm_client.generate(
                prompt=prompt,
                temperature=0.5,
                max_tokens=1500,
            )

            # Parse JSON response
            summary_data = json.loads(response)

            # Create ContentSummary object
            summary = ContentSummary(
                content_id=content.id,
                summary_type=SummaryType(summary_type),
                language_code=language_code,
                summary_text=summary_data.get("summary", ""),
                key_concepts=summary_data.get("key_concepts", []),
                learning_objectives=summary_data.get("learning_objectives", []),
                prerequisites=summary_data.get("prerequisites", []),
                auto_generated=True,
                generated_by="gpt-4",
            )

            # Persist to database if session provided
            if db:
                db.add(summary)
                await db.commit()
                await db.refresh(summary)

            logger.info(
                "summary_generated",
                content_id=content.id,
                summary_type=summary_type,
                language_code=language_code,
            )

            return summary

        except Exception as e:
            logger.error(
                "summary_generation_error",
                error=str(e),
                content_id=content.id,
            )
            raise

    async def extract_key_concepts(
        self,
        content_text: str,
        max_concepts: int = 5,
    ) -> List[str]:
        """
        Extract main concepts from content

        Args:
            content_text: Full content text
            max_concepts: Maximum number of concepts to extract

        Returns:
            List of key concept strings
        """
        try:
            prompt = f"""Analyze this robotics educational content and extract the {max_concepts} most important concepts.

Content:
{content_text[:3000]}  # Limit to first 3000 chars for efficiency

Return ONLY a JSON array of concept strings:
["Concept 1", "Concept 2", ...]"""

            response = await self.llm_client.generate(
                prompt=prompt,
                temperature=0.3,
                max_tokens=500,
            )

            concepts = json.loads(response)
            return concepts[:max_concepts]

        except Exception as e:
            logger.error("concept_extraction_error", error=str(e))
            return []

    async def generate_learning_objectives(
        self,
        content_text: str,
        content_title: str,
    ) -> List[str]:
        """
        Auto-generate learning objectives from content

        Args:
            content_text: Full content text
            content_title: Content title for context

        Returns:
            List of learning objective strings
        """
        try:
            prompt = f"""Analyze this robotics educational content and generate 3-5 measurable learning objectives.

Title: {content_title}

Content:
{content_text[:3000]}

Learning objectives should:
1. Start with action verbs (Understand, Explain, Apply, Analyze, etc.)
2. Be specific and measurable
3. Focus on what students will be able to do after completing this content

Return ONLY a JSON array of objective strings:
["Objective 1", "Objective 2", ...]"""

            response = await self.llm_client.generate(
                prompt=prompt,
                temperature=0.4,
                max_tokens=800,
            )

            objectives = json.loads(response)
            return objectives

        except Exception as e:
            logger.error("objective_generation_error", error=str(e))
            return []

    def _build_summary_prompt(
        self,
        content_text: str,
        content_title: str,
        summary_type: str,
    ) -> str:
        """
        Build prompt for summary generation
        """
        type_instructions = {
            "brief": "Generate a 2-3 sentence summary that captures the essence of the content.",
            "detailed": "Generate a comprehensive paragraph (5-7 sentences) that covers all major topics.",
            "key_points": "Generate a bulleted list of 5-7 key points from the content.",
        }

        instruction = type_instructions.get(
            summary_type, type_instructions["brief"]
        )

        prompt = f"""Analyze this robotics educational content and generate a summary.

Title: {content_title}

Content:
{content_text}

{instruction}

Generate:
1. Summary (based on type: {summary_type})
2. Key concepts (3-5 main ideas as short phrases)
3. Learning objectives (what students will learn - 3-5 items)
4. Prerequisites (what students should know first - 2-4 items)
5. Time estimate (reading + exercises in minutes)

Format as JSON:
{{
  "summary": "...",
  "key_concepts": ["Concept 1", "Concept 2", ...],
  "learning_objectives": ["Objective 1", "Objective 2", ...],
  "prerequisites": ["Prereq 1", "Prereq 2", ...],
  "estimated_time_minutes": 45
}}"""

        return prompt
