"""
Assessment Database Models
FR-043 to FR-052: Quizzes, Projects, Peer Review, Safety Assessment
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON, Integer, Float, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import enum

from ...shared.database import Base


class AssessmentType(str, enum.Enum):
    """Types of assessments"""
    QUIZ = "quiz"  # Multiple choice, auto-graded
    PROJECT = "project"  # Code/hardware project with rubric
    PEER_REVIEW = "peer_review"  # Peer-reviewed submission
    SAFETY = "safety"  # Safety assessment (FR-052)


class QuestionType(str, enum.Enum):
    """Question types"""
    MULTIPLE_CHOICE = "multiple_choice"
    CODE = "code"  # Code submission
    ESSAY = "essay"  # Text response
    FILE_UPLOAD = "file_upload"  # Document/video upload


class SubmissionStatus(str, enum.Enum):
    """Submission statuses"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    GRADED = "graded"
    RETURNED = "returned"


class Assessment(Base):
    """
    Assessments for stage progression
    FR-043: Assessment delivery
    FR-052: Safety assessment
    """
    __tablename__ = "assessments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    stage_id = Column(UUID(as_uuid=True), ForeignKey("stages.id", ondelete="CASCADE"), nullable=False)
    content_id = Column(UUID(as_uuid=True), ForeignKey("content_items.id", ondelete="SET NULL"), nullable=True)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    assessment_type = Column(SQLEnum(AssessmentType), nullable=False)

    # Configuration
    passing_score = Column(Float, nullable=False, default=70.0)  # Percentage
    time_limit_minutes = Column(Integer, nullable=True)  # Null = untimed
    max_attempts = Column(Integer, nullable=True)  # Null = unlimited
    is_required = Column(Boolean, default=True)  # Required for stage completion

    # Safety assessment specific (FR-052)
    is_safety_assessment = Column(Boolean, default=False)
    safety_item_count = Column(Integer, nullable=True)  # Must be 10 for safety assessments

    # Scheduling
    available_from = Column(DateTime, nullable=True)
    available_until = Column(DateTime, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Relationships
    stage = relationship("Stage", back_populates="assessments")
    content = relationship("ContentItem")
    questions = relationship("AssessmentQuestion", back_populates="assessment", cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="assessment", cascade="all, delete-orphan")
    rubric = relationship("Rubric", back_populates="assessment", uselist=False, cascade="all, delete-orphan")
    creator = relationship("User", foreign_keys=[created_by])

    def __repr__(self):
        return f"<Assessment(id={self.id}, title='{self.title}', type='{self.assessment_type}')>"


class AssessmentQuestion(Base):
    """
    Individual questions in an assessment
    """
    __tablename__ = "assessment_questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)

    question_text = Column(Text, nullable=False)
    question_type = Column(SQLEnum(QuestionType), nullable=False)
    points = Column(Float, nullable=False, default=1.0)
    order_index = Column(Integer, nullable=False, default=0)

    # Multiple choice options
    options = Column(JSON, nullable=True)  # [{"id": "a", "text": "...", "is_correct": true}, ...]

    # Code question config
    starter_code = Column(Text, nullable=True)
    test_cases = Column(JSON, nullable=True)  # [{"input": "...", "expected_output": "..."}]

    # Correct answer (for auto-grading)
    correct_answer = Column(Text, nullable=True)  # For MC: "a", for code: reference solution

    # Explanation
    explanation = Column(Text, nullable=True)  # Shown after submission

    # Relationships
    assessment = relationship("Assessment", back_populates="questions")

    def __repr__(self):
        return f"<AssessmentQuestion(id={self.id}, type='{self.question_type}')>"


class Submission(Base):
    """
    Student submissions for assessments
    FR-043: Assessment delivery
    FR-044: Project submission
    """
    __tablename__ = "submissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    status = Column(SQLEnum(SubmissionStatus), nullable=False, default=SubmissionStatus.DRAFT)
    attempt_number = Column(Integer, nullable=False, default=1)

    # Answers
    answers = Column(JSON, nullable=False)  # {"question_id": "answer_value", ...}

    # Scoring
    score = Column(Float, nullable=True)  # Percentage
    total_points = Column(Float, nullable=True)
    earned_points = Column(Float, nullable=True)
    passed = Column(Boolean, nullable=True)

    # Grading
    auto_graded = Column(Boolean, default=False)
    graded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    graded_at = Column(DateTime, nullable=True)
    feedback = Column(Text, nullable=True)

    # Similarity detection (FR-050)
    similarity_score = Column(Float, nullable=True)  # 0-100
    flagged_for_review = Column(Boolean, default=False)

    # Timing
    started_at = Column(DateTime, nullable=True)
    submitted_at = Column(DateTime, nullable=True)
    time_spent_minutes = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    assessment = relationship("Assessment", back_populates="submissions")
    user = relationship("User", foreign_keys=[user_id], back_populates="submissions")
    grader = relationship("User", foreign_keys=[graded_by])
    peer_reviews = relationship("PeerReview", back_populates="submission", cascade="all, delete-orphan")
    rubric_scores = relationship("RubricScore", back_populates="submission", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Submission(id={self.id}, user_id={self.user_id}, score={self.score})>"


class Rubric(Base):
    """
    Rubrics for project-based assessments
    FR-045: Rubric-based grading
    """
    __tablename__ = "rubrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False, unique=True)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # Criteria structure
    criteria = Column(JSON, nullable=False)
    # [
    #   {
    #     "id": "func",
    #     "name": "Functionality",
    #     "description": "...",
    #     "max_points": 30,
    #     "levels": [
    #       {"level": 5, "description": "Excellent", "points": 30},
    #       {"level": 4, "description": "Good", "points": 24},
    #       ...
    #     ]
    #   },
    #   ...
    # ]

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    assessment = relationship("Assessment", back_populates="rubric")
    rubric_scores = relationship("RubricScore", back_populates="rubric", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Rubric(id={self.id}, title='{self.title}')>"


class RubricScore(Base):
    """
    Scores for each rubric criterion in a submission
    """
    __tablename__ = "rubric_scores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    submission_id = Column(UUID(as_uuid=True), ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False)
    rubric_id = Column(UUID(as_uuid=True), ForeignKey("rubrics.id", ondelete="CASCADE"), nullable=False)

    criterion_id = Column(String(50), nullable=False)  # Matches criteria[].id
    level_awarded = Column(Integer, nullable=False)  # 1-5
    points_awarded = Column(Float, nullable=False)
    feedback = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    submission = relationship("Submission", back_populates="rubric_scores")
    rubric = relationship("Rubric", back_populates="rubric_scores")

    def __repr__(self):
        return f"<RubricScore(criterion='{self.criterion_id}', level={self.level_awarded})>"


class PeerReview(Base):
    """
    Peer reviews for submissions
    FR-051: Peer review workflow
    """
    __tablename__ = "peer_reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    submission_id = Column(UUID(as_uuid=True), ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False)
    reviewer_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Review content
    rating = Column(Integer, nullable=True)  # 1-5 stars
    strengths = Column(Text, nullable=True)
    areas_for_improvement = Column(Text, nullable=True)
    overall_feedback = Column(Text, nullable=True)

    # Rubric scores (if rubric exists)
    rubric_scores = Column(JSON, nullable=True)  # {"criterion_id": {"level": 4, "feedback": "..."}}

    # Status
    completed = Column(Boolean, default=False)
    submitted_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    submission = relationship("Submission", back_populates="peer_reviews")
    reviewer = relationship("User")

    def __repr__(self):
        return f"<PeerReview(id={self.id}, reviewer_id={self.reviewer_id}, completed={self.completed})>"
