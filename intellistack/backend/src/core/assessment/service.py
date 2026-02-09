"""
Assessment Service Layer
FR-043 to FR-052: Assessment management, grading, peer review
"""

import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload

from .models import (
    Assessment,
    AssessmentQuestion,
    Submission,
    Rubric,
    RubricScore,
    PeerReview,
    AssessmentType,
    QuestionType,
    SubmissionStatus,
)
from .schemas import (
    AssessmentResultDTO,
    GradingFeedbackDTO,
)


class AssessmentService:
    """Service for assessment operations"""

    def __init__(self, db: AsyncSession):
        self.db = db

    # ========================================================================
    # Assessment Management
    # ========================================================================

    async def create_assessment(
        self,
        stage_id: uuid.UUID,
        title: str,
        assessment_type: AssessmentType,
        created_by: uuid.UUID,
        **kwargs,
    ) -> Assessment:
        """Create a new assessment (FR-043)"""
        assessment = Assessment(
            stage_id=stage_id,
            title=title,
            assessment_type=assessment_type,
            created_by=created_by,
            **kwargs,
        )
        self.db.add(assessment)
        await self.db.commit()
        await self.db.refresh(assessment)
        return assessment

    async def get_assessment(
        self, assessment_id: uuid.UUID, include_questions: bool = True
    ) -> Optional[Assessment]:
        """Get assessment by ID"""
        query = select(Assessment).where(Assessment.id == assessment_id)

        if include_questions:
            query = query.options(selectinload(Assessment.questions))

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def add_question(
        self, assessment_id: uuid.UUID, question_data: Dict[str, Any]
    ) -> AssessmentQuestion:
        """Add question to assessment"""
        question = AssessmentQuestion(
            assessment_id=assessment_id,
            **question_data,
        )
        self.db.add(question)
        await self.db.commit()
        await self.db.refresh(question)
        return question

    async def list_assessments(
        self,
        stage_id: Optional[uuid.UUID] = None,
        assessment_type: Optional[AssessmentType] = None,
    ) -> List[Assessment]:
        """List assessments with filters"""
        query = select(Assessment)

        if stage_id:
            query = query.where(Assessment.stage_id == stage_id)
        if assessment_type:
            query = query.where(Assessment.assessment_type == assessment_type)

        query = query.order_by(Assessment.created_at.desc())

        result = await self.db.execute(query)
        return list(result.scalars().all())

    # ========================================================================
    # Submission Management
    # ========================================================================

    async def start_submission(
        self, assessment_id: uuid.UUID, user_id: uuid.UUID
    ) -> Submission:
        """Start a new submission attempt"""
        # Check existing attempts
        existing_count = await self._count_user_attempts(assessment_id, user_id)

        # Get assessment to check max_attempts
        assessment = await self.get_assessment(assessment_id, include_questions=False)
        if assessment.max_attempts and existing_count >= assessment.max_attempts:
            raise ValueError(f"Maximum attempts ({assessment.max_attempts}) reached")

        submission = Submission(
            assessment_id=assessment_id,
            user_id=user_id,
            status=SubmissionStatus.DRAFT,
            attempt_number=existing_count + 1,
            answers={},
            started_at=datetime.utcnow(),
        )
        self.db.add(submission)
        await self.db.commit()
        await self.db.refresh(submission)
        return submission

    async def submit_answers(
        self, submission_id: uuid.UUID, user_id: uuid.UUID, answers: Dict[str, Any]
    ) -> Submission:
        """Submit assessment answers (FR-043)"""
        # Get submission
        submission = await self._get_submission(submission_id, user_id)
        if submission.status != SubmissionStatus.DRAFT:
            raise ValueError("Submission already submitted")

        # Update submission
        submission.answers = answers
        submission.status = SubmissionStatus.SUBMITTED
        submission.submitted_at = datetime.utcnow()

        if submission.started_at:
            time_spent = (datetime.utcnow() - submission.started_at).total_seconds() / 60
            submission.time_spent_minutes = int(time_spent)

        # Get assessment
        assessment = await self.get_assessment(submission.assessment_id)

        # Auto-grade if possible (FR-047)
        if assessment.assessment_type == AssessmentType.QUIZ:
            await self._auto_grade_submission(submission, assessment)

        await self.db.commit()
        await self.db.refresh(submission)

        return submission

    async def get_submission(
        self, submission_id: uuid.UUID, user_id: uuid.UUID
    ) -> Optional[Submission]:
        """Get submission by ID"""
        return await self._get_submission(submission_id, user_id)

    async def list_user_submissions(
        self,
        user_id: uuid.UUID,
        assessment_id: Optional[uuid.UUID] = None,
    ) -> List[Submission]:
        """List user's submissions"""
        query = select(Submission).where(Submission.user_id == user_id)

        if assessment_id:
            query = query.where(Submission.assessment_id == assessment_id)

        query = query.order_by(Submission.created_at.desc())

        result = await self.db.execute(query)
        return list(result.scalars().all())

    # ========================================================================
    # Grading
    # ========================================================================

    async def grade_submission(
        self,
        submission_id: uuid.UUID,
        grader_id: uuid.UUID,
        score: float,
        feedback: Optional[str] = None,
        rubric_scores: Optional[List[Dict[str, Any]]] = None,
    ) -> GradingFeedbackDTO:
        """Grade a submission manually (FR-045)"""
        # Get submission
        query = select(Submission).where(Submission.id == submission_id)
        result = await self.db.execute(query)
        submission = result.scalar_one_or_none()

        if not submission:
            raise ValueError("Submission not found")

        # Get assessment
        assessment = await self.get_assessment(submission.assessment_id, include_questions=False)

        # Update submission
        submission.score = score
        submission.passed = score >= assessment.passing_score
        submission.status = SubmissionStatus.GRADED
        submission.graded_by = grader_id
        submission.graded_at = datetime.utcnow()
        submission.feedback = feedback

        # Save rubric scores if provided
        if rubric_scores and assessment.rubric:
            for score_data in rubric_scores:
                rubric_score = RubricScore(
                    submission_id=submission_id,
                    rubric_id=assessment.rubric.id,
                    **score_data,
                )
                self.db.add(rubric_score)

        await self.db.commit()

        # Generate feedback DTO
        return GradingFeedbackDTO(
            submission_id=submission_id,
            score=score,
            passed=submission.passed,
            feedback=feedback or "No feedback provided",
            rubric_scores=rubric_scores,
            strengths=["Good effort"] if score >= 80 else [],
            areas_for_improvement=["Review the material"] if score < assessment.passing_score else [],
        )

    async def get_assessment_result(
        self, submission_id: uuid.UUID, user_id: uuid.UUID
    ) -> AssessmentResultDTO:
        """Get detailed assessment result (FR-048)"""
        # Get submission with assessment
        submission = await self._get_submission(submission_id, user_id)
        assessment = await self.get_assessment(submission.assessment_id)

        # Check attempts remaining
        attempts_count = await self._count_user_attempts(assessment.id, user_id)
        attempts_remaining = None
        if assessment.max_attempts:
            attempts_remaining = assessment.max_attempts - attempts_count

        can_retake = (
            not submission.passed
            and (assessment.max_attempts is None or attempts_remaining > 0)
        )

        # Build answers with feedback
        answers_with_feedback = []
        if submission.status == SubmissionStatus.GRADED:
            for question in assessment.questions:
                q_id = str(question.id)
                student_answer = submission.answers.get(q_id)

                feedback_item = {
                    "question_id": q_id,
                    "question_text": question.question_text,
                    "student_answer": student_answer,
                    "correct_answer": question.correct_answer if submission.passed else None,
                    "explanation": question.explanation,
                    "points": question.points,
                }
                answers_with_feedback.append(feedback_item)

        return AssessmentResultDTO(
            submission=submission,
            assessment=assessment,
            answers_with_feedback=answers_with_feedback,
            passed=submission.passed or False,
            attempts_remaining=attempts_remaining,
            can_retake=can_retake,
        )

    # ========================================================================
    # Rubric Management
    # ========================================================================

    async def create_rubric(
        self, assessment_id: uuid.UUID, title: str, criteria: List[Dict[str, Any]]
    ) -> Rubric:
        """Create rubric for assessment (FR-045)"""
        rubric = Rubric(
            assessment_id=assessment_id,
            title=title,
            criteria=criteria,
        )
        self.db.add(rubric)
        await self.db.commit()
        await self.db.refresh(rubric)
        return rubric

    # ========================================================================
    # Peer Review (FR-051)
    # ========================================================================

    async def assign_peer_review(
        self, submission_id: uuid.UUID, reviewer_id: uuid.UUID
    ) -> PeerReview:
        """Assign peer review"""
        # Check if already assigned
        query = select(PeerReview).where(
            and_(
                PeerReview.submission_id == submission_id,
                PeerReview.reviewer_id == reviewer_id,
            )
        )
        result = await self.db.execute(query)
        existing = result.scalar_one_or_none()

        if existing:
            return existing

        peer_review = PeerReview(
            submission_id=submission_id,
            reviewer_id=reviewer_id,
        )
        self.db.add(peer_review)
        await self.db.commit()
        await self.db.refresh(peer_review)
        return peer_review

    async def submit_peer_review(
        self,
        peer_review_id: uuid.UUID,
        reviewer_id: uuid.UUID,
        rating: Optional[int],
        strengths: Optional[str],
        areas_for_improvement: Optional[str],
        overall_feedback: Optional[str],
        rubric_scores: Optional[Dict[str, Any]],
    ) -> PeerReview:
        """Submit peer review"""
        query = select(PeerReview).where(
            and_(
                PeerReview.id == peer_review_id,
                PeerReview.reviewer_id == reviewer_id,
            )
        )
        result = await self.db.execute(query)
        peer_review = result.scalar_one_or_none()

        if not peer_review:
            raise ValueError("Peer review not found")

        peer_review.rating = rating
        peer_review.strengths = strengths
        peer_review.areas_for_improvement = areas_for_improvement
        peer_review.overall_feedback = overall_feedback
        peer_review.rubric_scores = rubric_scores
        peer_review.completed = True
        peer_review.submitted_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(peer_review)

        return peer_review

    async def list_peer_reviews_for_submission(
        self, submission_id: uuid.UUID
    ) -> List[PeerReview]:
        """Get peer reviews for a submission"""
        query = select(PeerReview).where(PeerReview.submission_id == submission_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    # ========================================================================
    # Similarity Detection (FR-050)
    # ========================================================================

    async def check_similarity(
        self, submission_id: uuid.UUID
    ) -> Tuple[float, List[uuid.UUID]]:
        """
        Check submission similarity (placeholder)
        FR-050: Similarity detection

        In production: Use algorithms like:
        - Code: MOSS, JPlag, or AST-based comparison
        - Text: Cosine similarity, Levenshtein distance
        """
        # Placeholder: Random similarity score
        import random

        similarity_score = random.uniform(0, 100)

        # Flag if >80% similar
        if similarity_score > 80:
            query = select(Submission).where(Submission.id == submission_id)
            result = await self.db.execute(query)
            submission = result.scalar_one()

            submission.similarity_score = similarity_score
            submission.flagged_for_review = True
            await self.db.commit()

        return similarity_score, []

    # ========================================================================
    # Helper Methods
    # ========================================================================

    async def _get_submission(
        self, submission_id: uuid.UUID, user_id: uuid.UUID
    ) -> Submission:
        """Get submission with user validation"""
        query = (
            select(Submission)
            .where(
                and_(
                    Submission.id == submission_id,
                    Submission.user_id == user_id,
                )
            )
            .options(selectinload(Submission.assessment))
        )
        result = await self.db.execute(query)
        submission = result.scalar_one_or_none()

        if not submission:
            raise ValueError("Submission not found")

        return submission

    async def _count_user_attempts(
        self, assessment_id: uuid.UUID, user_id: uuid.UUID
    ) -> int:
        """Count user's attempts for an assessment"""
        query = select(func.count(Submission.id)).where(
            and_(
                Submission.assessment_id == assessment_id,
                Submission.user_id == user_id,
            )
        )
        result = await self.db.execute(query)
        return result.scalar() or 0

    async def _auto_grade_submission(
        self, submission: Submission, assessment: Assessment
    ) -> None:
        """
        Auto-grade quiz submission (FR-047)
        """
        total_points = 0.0
        earned_points = 0.0

        for question in assessment.questions:
            q_id = str(question.id)
            student_answer = submission.answers.get(q_id)

            total_points += question.points

            # Multiple choice auto-grading
            if question.question_type == QuestionType.MULTIPLE_CHOICE:
                if student_answer == question.correct_answer:
                    earned_points += question.points

            # Code auto-grading (placeholder - needs test execution)
            elif question.question_type == QuestionType.CODE:
                # In production: execute code against test cases
                # For now, assume partial credit
                if student_answer and len(str(student_answer)) > 10:
                    earned_points += question.points * 0.5

        # Calculate score
        submission.total_points = total_points
        submission.earned_points = earned_points
        submission.score = (earned_points / total_points * 100) if total_points > 0 else 0
        submission.passed = submission.score >= assessment.passing_score
        submission.auto_graded = True
        submission.graded_at = datetime.utcnow()
        submission.status = SubmissionStatus.GRADED
