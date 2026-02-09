/**
 * Assessment Hook
 * Manages assessments, submissions, and grading
 * FR-043 to FR-052
 */

import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../lib/api';

export interface Assessment {
  id: string;
  stage_id: string;
  content_id?: string;
  title: string;
  description?: string;
  assessment_type: 'quiz' | 'project' | 'peer_review' | 'safety';
  passing_score: number;
  time_limit_minutes?: number;
  max_attempts?: number;
  is_required: boolean;
  is_safety_assessment: boolean;
  available_from?: string;
  available_until?: string;
  created_at: string;
  questions: AssessmentQuestion[];
}

export interface AssessmentQuestion {
  id: string;
  question_text: string;
  question_type: 'multiple_choice' | 'code' | 'essay' | 'file_upload';
  points: number;
  order_index: number;
  options?: Array<{ id: string; text: string }>;
  starter_code?: string;
}

export interface Submission {
  id: string;
  assessment_id: string;
  user_id: string;
  status: 'draft' | 'submitted' | 'under_review' | 'graded' | 'returned';
  attempt_number: number;
  score?: number;
  total_points?: number;
  earned_points?: number;
  passed?: boolean;
  auto_graded: boolean;
  graded_at?: string;
  feedback?: string;
  similarity_score?: number;
  flagged_for_review: boolean;
  started_at?: string;
  submitted_at?: string;
  time_spent_minutes?: number;
  created_at: string;
}

export interface AssessmentResult {
  submission: Submission;
  assessment: Assessment;
  answers_with_feedback: Array<{
    question_id: string;
    question_text: string;
    student_answer: any;
    correct_answer?: string;
    explanation?: string;
    points: number;
  }>;
  passed: boolean;
  attempts_remaining?: number;
  can_retake: boolean;
}

export interface PeerReview {
  id: string;
  submission_id: string;
  reviewer_id: string;
  rating?: number;
  strengths?: string;
  areas_for_improvement?: string;
  overall_feedback?: string;
  rubric_scores?: Record<string, any>;
  completed: boolean;
  submitted_at?: string;
  created_at: string;
}

export function useAssessment() {
  const queryClient = useQueryClient();
  const [currentAssessmentId, setCurrentAssessmentId] = useState<string | null>(null);
  const [currentSubmissionId, setCurrentSubmissionId] = useState<string | null>(null);

  // List assessments
  const { data: assessments, isLoading: assessmentsLoading } = useQuery({
    queryKey: ['assessments'],
    queryFn: async () => {
      const response = await apiClient.get('/assessments');
      return response.data as Assessment[];
    },
  });

  // Get specific assessment
  const { data: assessment, isLoading: assessmentLoading } = useQuery({
    queryKey: ['assessment', currentAssessmentId],
    queryFn: async () => {
      if (!currentAssessmentId) return null;
      const response = await apiClient.get(`/assessments/${currentAssessmentId}`);
      return response.data as Assessment;
    },
    enabled: !!currentAssessmentId,
  });

  // Get my submissions
  const { data: mySubmissions, isLoading: submissionsLoading } = useQuery({
    queryKey: ['my-submissions', currentAssessmentId],
    queryFn: async () => {
      const params = currentAssessmentId ? `?assessment_id=${currentAssessmentId}` : '';
      const response = await apiClient.get(`/assessments/my-submissions${params}`);
      return response.data as Submission[];
    },
  });

  // Start submission
  const startSubmission = useMutation({
    mutationFn: async (assessmentId: string) => {
      const response = await apiClient.post(`/assessments/${assessmentId}/submissions`);
      return response.data as Submission;
    },
    onSuccess: (submission) => {
      setCurrentSubmissionId(submission.id);
      queryClient.invalidateQueries({ queryKey: ['my-submissions'] });
    },
  });

  // Submit answers
  const submitAnswers = useMutation({
    mutationFn: async (data: { submissionId: string; answers: Record<string, any> }) => {
      const response = await apiClient.post(
        `/assessments/submissions/${data.submissionId}/submit`,
        { answers: data.answers }
      );
      return response.data as Submission;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['my-submissions'] });
      queryClient.invalidateQueries({ queryKey: ['assessment-result'] });
    },
  });

  // Get assessment result
  const { data: assessmentResult, isLoading: resultLoading } = useQuery({
    queryKey: ['assessment-result', currentSubmissionId],
    queryFn: async () => {
      if (!currentSubmissionId) return null;
      const response = await apiClient.get(`/assessments/submissions/${currentSubmissionId}/result`);
      return response.data as AssessmentResult;
    },
    enabled: !!currentSubmissionId,
  });

  // Submit peer review
  const submitPeerReview = useMutation({
    mutationFn: async (data: {
      peerReviewId: string;
      rating?: number;
      strengths?: string;
      areas_for_improvement?: string;
      overall_feedback?: string;
      rubric_scores?: Record<string, any>;
    }) => {
      const response = await apiClient.post(
        `/assessments/peer-reviews/${data.peerReviewId}/submit`,
        data
      );
      return response.data as PeerReview;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['peer-reviews'] });
    },
  });

  // Get peer reviews for submission
  const getPeerReviews = async (submissionId: string) => {
    const response = await apiClient.get(`/assessments/submissions/${submissionId}/peer-reviews`);
    return response.data as PeerReview[];
  };

  return {
    // State
    assessments,
    assessment,
    mySubmissions,
    assessmentResult,
    currentAssessmentId,
    setCurrentAssessmentId,
    currentSubmissionId,
    setCurrentSubmissionId,

    // Loading states
    assessmentsLoading,
    assessmentLoading,
    submissionsLoading,
    resultLoading,

    // Mutations
    startSubmission,
    submitAnswers,
    submitPeerReview,
    getPeerReviews,

    // Mutation states
    isStarting: startSubmission.isPending,
    isSubmitting: submitAnswers.isPending,
    isSubmittingPeerReview: submitPeerReview.isPending,
  };
}
