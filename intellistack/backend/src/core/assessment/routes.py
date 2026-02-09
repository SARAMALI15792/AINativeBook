"""
Assessment API Routes
FR-043 to FR-052: Assessment system endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import uuid

from ...shared.database import get_db
from ...shared.middleware import require_role
from .service import AssessmentService
from .schemas import (
    CreateAssessmentRequest,
    CreateQuestionRequest,
    SubmitAnswersRequest,
    GradeSubmissionRequest,
    CreatePeerReviewRequest,
    CreateRubricRequest,
    AssessmentResponse,
    SubmissionResponse,
    RubricResponse,
    PeerReviewResponse,
    AssessmentResultDTO,
    GradingFeedbackDTO,
)
from .models import AssessmentType

router = APIRouter(prefix="/assessments", tags=["Assessments"])


# ============================================================================
# Assessment Management (Instructors)
# ============================================================================

@router.post("", response_model=AssessmentResponse, status_code=status.HTTP_201_CREATED)
async def create_assessment(
    request: CreateAssessmentRequest,
    current_user=Depends(require_role("instructor")),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new assessment (FR-043)

    Assessment types:
    - quiz: Auto-graded multiple choice
    - project: Code/hardware project with rubric
    - peer_review: Peer-reviewed submissions
    - safety: Safety assessment (FR-052)
    """
    service = AssessmentService(db)

    assessment = await service.create_assessment(
        stage_id=request.stage_id,
        content_id=request.content_id,
        title=request.title,
        description=request.description,
        assessment_type=request.assessment_type,
        passing_score=request.passing_score,
        time_limit_minutes=request.time_limit_minutes,
        max_attempts=request.max_attempts,
        is_required=request.is_required,
        is_safety_assessment=request.is_safety_assessment,
        available_from=request.available_from,
        available_until=request.available_until,
        created_by=current_user.id,
    )

    return assessment


@router.get("", response_model=List[AssessmentResponse])
async def list_assessments(
    stage_id: Optional[uuid.UUID] = None,
    assessment_type: Optional[AssessmentType] = None,
    current_user=Depends(require_role("student")),
    db: AsyncSession = Depends(get_db),
):
    """List assessments with optional filters"""
    service = AssessmentService(db)
    assessments = await service.list_assessments(
        stage_id=stage_id,
        assessment_type=assessment_type,
    )
    return assessments


@router.get("/{assessment_id}", response_model=AssessmentResponse)
async def get_assessment(
    assessment_id: uuid.UUID,
    current_user=Depends(require_role("student")),
    db: AsyncSession = Depends(get_db),
):
    """Get assessment details"""
    service = AssessmentService(db)
    assessment = await service.get_assessment(assessment_id)

    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    return assessment


@router.post("/{assessment_id}/questions", status_code=status.HTTP_201_CREATED)
async def add_question(
    assessment_id: uuid.UUID,
    request: CreateQuestionRequest,
    current_user=Depends(require_role("instructor")),
    db: AsyncSession = Depends(get_db),
):
    """Add question to assessment"""
    service = AssessmentService(db)

    try:
        question = await service.add_question(
            assessment_id=assessment_id,
            question_data=request.model_dump(),
        )
        return question
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# Submissions (Students)
# ============================================================================

@router.post("/{assessment_id}/submissions", response_model=SubmissionResponse, status_code=status.HTTP_201_CREATED)
async def start_submission(
    assessment_id: uuid.UUID,
    current_user=Depends(require_role("student")),
    db: AsyncSession = Depends(get_db),
):
    """
    Start a new assessment attempt
    Creates a draft submission
    """
    service = AssessmentService(db)

    try:
        submission = await service.start_submission(
            assessment_id=assessment_id,
            user_id=current_user.id,
        )
        return submission
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/submissions/{submission_id}/submit", response_model=SubmissionResponse)
async def submit_answers(
    submission_id: uuid.UUID,
    request: SubmitAnswersRequest,
    current_user=Depends(require_role("student")),
    db: AsyncSession = Depends(get_db),
):
    """
    Submit assessment answers (FR-043)

    For quizzes: Auto-graded immediately (FR-047)
    For projects: Sent to instructor for grading (FR-045)
    """
    service = AssessmentService(db)

    try:
        submission = await service.submit_answers(
            submission_id=submission_id,
            user_id=current_user.id,
            answers=request.answers,
        )

        # Check similarity (FR-050)
        await service.check_similarity(submission_id)

        return submission
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/submissions/{submission_id}", response_model=SubmissionResponse)
async def get_submission(
    submission_id: uuid.UUID,
    current_user=Depends(require_role("student")),
    db: AsyncSession = Depends(get_db),
):
    """Get submission details"""
    service = AssessmentService(db)

    try:
        submission = await service.get_submission(
            submission_id=submission_id,
            user_id=current_user.id,
        )
        return submission
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/submissions/{submission_id}/result", response_model=AssessmentResultDTO)
async def get_assessment_result(
    submission_id: uuid.UUID,
    current_user=Depends(require_role("student")),
    db: AsyncSession = Depends(get_db),
):
    """
    Get detailed assessment result with feedback (FR-048)

    Includes:
    - Score and pass/fail status
    - Correct answers (if passed)
    - Explanations
    - Attempts remaining
    """
    service = AssessmentService(db)

    try:
        result = await service.get_assessment_result(
            submission_id=submission_id,
            user_id=current_user.id,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/my-submissions", response_model=List[SubmissionResponse])
async def list_my_submissions(
    assessment_id: Optional[uuid.UUID] = None,
    current_user=Depends(require_role("student")),
    db: AsyncSession = Depends(get_db),
):
    """List current user's submissions"""
    service = AssessmentService(db)
    submissions = await service.list_user_submissions(
        user_id=current_user.id,
        assessment_id=assessment_id,
    )
    return submissions


# ============================================================================
# Grading (Instructors)
# ============================================================================

@router.post("/submissions/{submission_id}/grade", response_model=GradingFeedbackDTO)
async def grade_submission(
    submission_id: uuid.UUID,
    request: GradeSubmissionRequest,
    current_user=Depends(require_role("instructor")),
    db: AsyncSession = Depends(get_db),
):
    """
    Grade a submission manually (FR-045)

    Used for:
    - Projects with rubrics
    - Code reviews
    - Manual grading
    """
    service = AssessmentService(db)

    try:
        feedback = await service.grade_submission(
            submission_id=submission_id,
            grader_id=current_user.id,
            score=request.score,
            feedback=request.feedback,
            rubric_scores=request.rubric_scores,
        )
        return feedback
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ============================================================================
# Rubrics (Instructors)
# ============================================================================

@router.post("/{assessment_id}/rubric", response_model=RubricResponse, status_code=status.HTTP_201_CREATED)
async def create_rubric(
    assessment_id: uuid.UUID,
    request: CreateRubricRequest,
    current_user=Depends(require_role("instructor")),
    db: AsyncSession = Depends(get_db),
):
    """
    Create rubric for project assessment (FR-045)

    Rubric structure:
    - Criteria with point values
    - Performance levels (1-5)
    - Descriptions for each level
    """
    service = AssessmentService(db)

    try:
        rubric = await service.create_rubric(
            assessment_id=assessment_id,
            title=request.title,
            criteria=request.criteria,
        )
        return rubric
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# Peer Review (FR-051)
# ============================================================================

@router.post("/submissions/{submission_id}/peer-reviews", response_model=PeerReviewResponse, status_code=status.HTTP_201_CREATED)
async def assign_peer_review(
    submission_id: uuid.UUID,
    reviewer_id: uuid.UUID,
    current_user=Depends(require_role("instructor")),
    db: AsyncSession = Depends(get_db),
):
    """Assign peer review (instructor only)"""
    service = AssessmentService(db)

    peer_review = await service.assign_peer_review(
        submission_id=submission_id,
        reviewer_id=reviewer_id,
    )
    return peer_review


@router.post("/peer-reviews/{peer_review_id}/submit", response_model=PeerReviewResponse)
async def submit_peer_review(
    peer_review_id: uuid.UUID,
    request: CreatePeerReviewRequest,
    current_user=Depends(require_role("student")),
    db: AsyncSession = Depends(get_db),
):
    """
    Submit peer review (FR-051)

    Students review peer submissions with:
    - Rating (1-5 stars)
    - Strengths
    - Areas for improvement
    - Overall feedback
    - Optional rubric scores
    """
    service = AssessmentService(db)

    try:
        peer_review = await service.submit_peer_review(
            peer_review_id=peer_review_id,
            reviewer_id=current_user.id,
            rating=request.rating,
            strengths=request.strengths,
            areas_for_improvement=request.areas_for_improvement,
            overall_feedback=request.overall_feedback,
            rubric_scores=request.rubric_scores,
        )
        return peer_review
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/submissions/{submission_id}/peer-reviews", response_model=List[PeerReviewResponse])
async def list_peer_reviews(
    submission_id: uuid.UUID,
    current_user=Depends(require_role("student")),
    db: AsyncSession = Depends(get_db),
):
    """Get peer reviews for a submission"""
    service = AssessmentService(db)
    reviews = await service.list_peer_reviews_for_submission(submission_id)
    return reviews


# ============================================================================
# Safety Assessment (FR-052)
# ============================================================================

@router.get("/{assessment_id}/safety-check")
async def verify_safety_assessment(
    assessment_id: uuid.UUID,
    current_user=Depends(require_role("student")),
    db: AsyncSession = Depends(get_db),
):
    """
    Verify safety assessment requirements (FR-052)

    Safety assessments must:
    - Have exactly 10 questions
    - Be completed before hardware access
    - Cover stage-appropriate safety topics
    """
    service = AssessmentService(db)
    assessment = await service.get_assessment(assessment_id)

    if not assessment or not assessment.is_safety_assessment:
        raise HTTPException(status_code=404, detail="Safety assessment not found")

    # Check requirements
    question_count = len(assessment.questions)
    is_valid = question_count == 10

    return {
        "assessment_id": assessment_id,
        "is_safety_assessment": True,
        "question_count": question_count,
        "required_count": 10,
        "is_valid": is_valid,
        "message": "Safety assessment valid" if is_valid else f"Safety assessment must have exactly 10 questions (has {question_count})",
    }
