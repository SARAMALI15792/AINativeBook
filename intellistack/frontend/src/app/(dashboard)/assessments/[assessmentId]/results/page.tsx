/**
 * Assessment Results Page
 * Display assessment feedback and results (FR-048)
 */

'use client';

import { useEffect } from 'react';
import { useParams, useRouter, useSearchParams } from 'next/navigation';
import { useAssessment } from '@/hooks/useAssessment';
import { FeedbackDisplay } from '@/components/assessment/FeedbackDisplay';
import { Button } from '@/components/ui/button';
import { Loader2, ArrowLeft, RotateCcw } from 'lucide-react';

export default function AssessmentResultsPage() {
  const params = useParams();
  const router = useRouter();
  const searchParams = useSearchParams();

  const assessmentId = params.assessmentId as string;
  const submissionId = searchParams.get('submission');

  const {
    assessmentResult,
    resultLoading,
    setCurrentAssessmentId,
    setCurrentSubmissionId,
  } = useAssessment();

  useEffect(() => {
    setCurrentAssessmentId(assessmentId);
    if (submissionId) {
      setCurrentSubmissionId(submissionId);
    }
  }, [assessmentId, submissionId, setCurrentAssessmentId, setCurrentSubmissionId]);

  if (resultLoading || !assessmentResult) {
    return (
      <div className="flex items-center justify-center h-screen">
        <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
        <span className="ml-3 text-lg">Loading results...</span>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6 max-w-5xl">
      {/* Header */}
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">Assessment Results</h1>
          <p className="text-muted-foreground">{assessmentResult.assessment.title}</p>
        </div>

        <div className="flex space-x-2">
          <Button variant="outline" onClick={() => router.push('/assessments')}>
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Assessments
          </Button>

          {assessmentResult.can_retake && (
            <Button onClick={() => router.push(`/assessments/${assessmentId}`)}>
              <RotateCcw className="w-4 h-4 mr-2" />
              Retake Assessment
            </Button>
          )}
        </div>
      </div>

      {/* Feedback */}
      <FeedbackDisplay result={assessmentResult} />
    </div>
  );
}
