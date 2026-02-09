/**
 * Assessment Taking Page
 * Start and complete assessments
 */

'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useAssessment } from '@/hooks/useAssessment';
import { QuizForm } from '@/components/assessment/QuizForm';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Loader2, AlertTriangle, Clock, Target, FileText } from 'lucide-react';

export default function AssessmentPage() {
  const params = useParams();
  const router = useRouter();
  const assessmentId = params.assessmentId as string;

  const {
    assessment,
    assessmentLoading,
    mySubmissions,
    startSubmission,
    submitAnswers,
    isStarting,
    isSubmitting,
    setCurrentAssessmentId,
  } = useAssessment();

  const [hasStarted, setHasStarted] = useState(false);
  const [currentSubmission, setCurrentSubmission] = useState<any>(null);
  const [timeRemaining, setTimeRemaining] = useState<number | undefined>(undefined);

  // Set current assessment ID
  useEffect(() => {
    setCurrentAssessmentId(assessmentId);
  }, [assessmentId, setCurrentAssessmentId]);

  // Check for existing draft submission
  useEffect(() => {
    if (mySubmissions) {
      const draft = mySubmissions.find(
        (s) => s.assessment_id === assessmentId && s.status === 'draft'
      );
      if (draft) {
        setCurrentSubmission(draft);
        setHasStarted(true);

        // Calculate time remaining if timed
        if (assessment?.time_limit_minutes && draft.started_at) {
          const elapsed = Math.floor(
            (Date.now() - new Date(draft.started_at).getTime()) / 1000
          );
          const limit = assessment.time_limit_minutes * 60;
          const remaining = Math.max(0, limit - elapsed);
          setTimeRemaining(remaining);
        }
      }
    }
  }, [mySubmissions, assessmentId, assessment]);

  // Countdown timer
  useEffect(() => {
    if (timeRemaining === undefined || timeRemaining === 0) return;

    const interval = setInterval(() => {
      setTimeRemaining((prev) => {
        if (prev === undefined || prev <= 0) return 0;
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [timeRemaining]);

  const handleStart = async () => {
    try {
      const submission = await startSubmission.mutateAsync(assessmentId);
      setCurrentSubmission(submission);
      setHasStarted(true);

      // Start timer if timed
      if (assessment?.time_limit_minutes) {
        setTimeRemaining(assessment.time_limit_minutes * 60);
      }
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to start assessment');
    }
  };

  const handleSubmit = async (answers: Record<string, any>) => {
    if (!currentSubmission) return;

    try {
      await submitAnswers.mutateAsync({
        submissionId: currentSubmission.id,
        answers,
      });

      // Navigate to results
      router.push(`/assessments/${assessmentId}/results?submission=${currentSubmission.id}`);
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to submit assessment');
    }
  };

  if (assessmentLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
        <span className="ml-3 text-lg">Loading assessment...</span>
      </div>
    );
  }

  if (!assessment) {
    return (
      <div className="container mx-auto p-6">
        <Alert variant="destructive">
          <AlertDescription>Assessment not found.</AlertDescription>
        </Alert>
      </div>
    );
  }

  // Check attempts
  const attempts = mySubmissions?.filter((s) => s.assessment_id === assessmentId).length || 0;
  const canAttempt =
    !assessment.max_attempts || attempts < assessment.max_attempts;

  if (!hasStarted) {
    return (
      <div className="container mx-auto p-6 max-w-3xl">
        {/* Assessment Info */}
        <Card>
          <CardHeader>
            <div className="flex items-center space-x-2 mb-2">
              <Badge variant="outline">{assessment.assessment_type}</Badge>
              {assessment.is_required && <Badge variant="destructive">Required</Badge>}
            </div>
            <CardTitle className="text-2xl">{assessment.title}</CardTitle>
            <CardDescription>{assessment.description}</CardDescription>
          </CardHeader>

          <CardContent className="space-y-6">
            {/* Details */}
            <div className="grid grid-cols-2 gap-4">
              <div className="flex items-center space-x-3">
                <FileText className="w-5 h-5 text-muted-foreground" />
                <div>
                  <div className="text-sm font-medium">Questions</div>
                  <div className="text-sm text-muted-foreground">
                    {assessment.questions.length} questions
                  </div>
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <Target className="w-5 h-5 text-muted-foreground" />
                <div>
                  <div className="text-sm font-medium">Passing Score</div>
                  <div className="text-sm text-muted-foreground">
                    {assessment.passing_score}%
                  </div>
                </div>
              </div>

              {assessment.time_limit_minutes && (
                <div className="flex items-center space-x-3">
                  <Clock className="w-5 h-5 text-muted-foreground" />
                  <div>
                    <div className="text-sm font-medium">Time Limit</div>
                    <div className="text-sm text-muted-foreground">
                      {assessment.time_limit_minutes} minutes
                    </div>
                  </div>
                </div>
              )}

              {assessment.max_attempts && (
                <div className="flex items-center space-x-3">
                  <AlertTriangle className="w-5 h-5 text-muted-foreground" />
                  <div>
                    <div className="text-sm font-medium">Attempts</div>
                    <div className="text-sm text-muted-foreground">
                      {attempts} / {assessment.max_attempts} used
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Instructions */}
            <Alert>
              <AlertDescription>
                <strong>Instructions:</strong>
                <ul className="list-disc list-inside mt-2 space-y-1">
                  <li>Answer all questions to the best of your ability</li>
                  <li>You can navigate between questions using Previous/Next buttons</li>
                  {assessment.time_limit_minutes && (
                    <li>Your assessment will auto-submit when time runs out</li>
                  )}
                  <li>Review your answers before final submission</li>
                  {assessment.assessment_type === 'quiz' && (
                    <li>Quiz will be auto-graded immediately upon submission</li>
                  )}
                </ul>
              </AlertDescription>
            </Alert>

            {/* Max Attempts Warning */}
            {!canAttempt && (
              <Alert variant="destructive">
                <AlertTriangle className="h-4 w-4" />
                <AlertDescription>
                  You have used all {assessment.max_attempts} attempts for this assessment.
                </AlertDescription>
              </Alert>
            )}

            {/* Start Button */}
            <div className="flex justify-end space-x-4">
              <Button variant="outline" onClick={() => router.back()}>
                Cancel
              </Button>
              <Button onClick={handleStart} disabled={isStarting || !canAttempt}>
                {isStarting ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Starting...
                  </>
                ) : (
                  'Start Assessment'
                )}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6 max-w-4xl">
      <QuizForm
        assessment={assessment}
        onSubmit={handleSubmit}
        isSubmitting={isSubmitting}
        timeRemaining={timeRemaining}
      />
    </div>
  );
}
