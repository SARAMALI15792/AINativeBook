/**
 * Assessments List Page
 * View available assessments and submissions
 */

'use client';

import { useAssessment } from '@/hooks/useAssessment';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useRouter } from 'next/navigation';
import {
  FileText,
  Code,
  Users,
  Shield,
  Clock,
  Target,
  CheckCircle,
  XCircle,
  Loader2,
  AlertTriangle,
} from 'lucide-react';

const assessmentTypeConfig = {
  quiz: { icon: FileText, label: 'Quiz', color: 'text-blue-600', bgColor: 'bg-blue-50' },
  project: { icon: Code, label: 'Project', color: 'text-purple-600', bgColor: 'bg-purple-50' },
  peer_review: { icon: Users, label: 'Peer Review', color: 'text-green-600', bgColor: 'bg-green-50' },
  safety: { icon: Shield, label: 'Safety', color: 'text-red-600', bgColor: 'bg-red-50' },
};

export default function AssessmentsPage() {
  const router = useRouter();
  const { assessments, mySubmissions, assessmentsLoading, submissionsLoading } = useAssessment();

  if (assessmentsLoading || submissionsLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
        <span className="ml-3 text-lg">Loading assessments...</span>
      </div>
    );
  }

  const getSubmissionStatus = (assessmentId: string) => {
    const submissions = mySubmissions?.filter((s) => s.assessment_id === assessmentId) || [];
    if (submissions.length === 0) return { status: 'not_started', lastSubmission: null };

    const lastSubmission = submissions[0]; // Most recent
    return { status: lastSubmission.status, lastSubmission };
  };

  return (
    <div className="container mx-auto p-6 max-w-6xl">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold mb-2">Assessments</h1>
        <p className="text-muted-foreground">
          Complete assessments to demonstrate your understanding and progress through stages
        </p>
      </div>

      <Tabs defaultValue="available" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="available">Available Assessments</TabsTrigger>
          <TabsTrigger value="submissions">My Submissions</TabsTrigger>
        </TabsList>

        {/* Available Assessments */}
        <TabsContent value="available" className="mt-6 space-y-4">
          {assessments?.length === 0 ? (
            <Alert>
              <AlertDescription>No assessments available at this time.</AlertDescription>
            </Alert>
          ) : (
            assessments?.map((assessment) => {
              const config = assessmentTypeConfig[assessment.assessment_type];
              const Icon = config.icon;
              const { status, lastSubmission } = getSubmissionStatus(assessment.id);

              return (
                <Card key={assessment.id} className="hover:shadow-md transition-shadow">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-2">
                          <div className={`p-2 rounded ${config.bgColor}`}>
                            <Icon className={`w-5 h-5 ${config.color}`} />
                          </div>
                          <Badge variant="outline">{config.label}</Badge>
                          {assessment.is_required && (
                            <Badge variant="destructive">Required</Badge>
                          )}
                          {assessment.is_safety_assessment && (
                            <Badge variant="destructive">
                              <Shield className="w-3 h-3 mr-1" />
                              Safety
                            </Badge>
                          )}
                        </div>
                        <CardTitle className="text-xl">{assessment.title}</CardTitle>
                        <CardDescription className="mt-1">
                          {assessment.description || 'No description provided'}
                        </CardDescription>
                      </div>

                      {/* Status Badge */}
                      <div className="ml-4">
                        {status === 'not_started' && (
                          <Badge variant="secondary">Not Started</Badge>
                        )}
                        {status === 'draft' && (
                          <Badge variant="outline">In Progress</Badge>
                        )}
                        {status === 'submitted' && (
                          <Badge variant="secondary">
                            <Clock className="w-3 h-3 mr-1" />
                            Under Review
                          </Badge>
                        )}
                        {status === 'graded' && lastSubmission?.passed && (
                          <Badge variant="default" className="bg-green-600">
                            <CheckCircle className="w-3 h-3 mr-1" />
                            Passed
                          </Badge>
                        )}
                        {status === 'graded' && !lastSubmission?.passed && (
                          <Badge variant="destructive">
                            <XCircle className="w-3 h-3 mr-1" />
                            Not Passed
                          </Badge>
                        )}
                      </div>
                    </div>
                  </CardHeader>

                  <CardContent>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4 text-sm">
                      <div className="flex items-center space-x-2">
                        <Target className="w-4 h-4 text-muted-foreground" />
                        <span>Passing: {assessment.passing_score}%</span>
                      </div>
                      {assessment.time_limit_minutes && (
                        <div className="flex items-center space-x-2">
                          <Clock className="w-4 h-4 text-muted-foreground" />
                          <span>{assessment.time_limit_minutes} min</span>
                        </div>
                      )}
                      {assessment.max_attempts && (
                        <div className="flex items-center space-x-2">
                          <AlertTriangle className="w-4 h-4 text-muted-foreground" />
                          <span>Max {assessment.max_attempts} attempts</span>
                        </div>
                      )}
                      <div className="flex items-center space-x-2">
                        <FileText className="w-4 h-4 text-muted-foreground" />
                        <span>{assessment.questions.length} questions</span>
                      </div>
                    </div>

                    {/* Last Submission Info */}
                    {lastSubmission && (
                      <Alert className="mb-4">
                        <AlertDescription>
                          Last attempt: {lastSubmission.attempt_number} •{' '}
                          {lastSubmission.score !== null
                            ? `Score: ${lastSubmission.score.toFixed(1)}%`
                            : 'Pending grading'}
                        </AlertDescription>
                      </Alert>
                    )}

                    {/* Action Button */}
                    <div className="flex justify-end">
                      {status === 'not_started' && (
                        <Button
                          onClick={() => router.push(`/assessments/${assessment.id}`)}
                        >
                          Start Assessment
                        </Button>
                      )}
                      {status === 'draft' && (
                        <Button
                          onClick={() => router.push(`/assessments/${assessment.id}`)}
                          variant="outline"
                        >
                          Continue
                        </Button>
                      )}
                      {(status === 'submitted' || status === 'graded') && (
                        <Button
                          onClick={() =>
                            router.push(
                              `/assessments/${assessment.id}/results?submission=${lastSubmission?.id}`
                            )
                          }
                          variant="outline"
                        >
                          View Results
                        </Button>
                      )}
                    </div>
                  </CardContent>
                </Card>
              );
            })
          )}
        </TabsContent>

        {/* My Submissions */}
        <TabsContent value="submissions" className="mt-6 space-y-4">
          {mySubmissions?.length === 0 ? (
            <Alert>
              <AlertDescription>You haven't submitted any assessments yet.</AlertDescription>
            </Alert>
          ) : (
            mySubmissions?.map((submission) => {
              const assessment = assessments?.find((a) => a.id === submission.assessment_id);
              if (!assessment) return null;

              const config = assessmentTypeConfig[assessment.assessment_type];
              const Icon = config.icon;

              return (
                <Card key={submission.id}>
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-2">
                          <Icon className={`w-5 h-5 ${config.color}`} />
                          <Badge variant="outline">{config.label}</Badge>
                        </div>
                        <CardTitle className="text-lg">{assessment.title}</CardTitle>
                        <CardDescription>
                          Attempt {submission.attempt_number} •{' '}
                          {new Date(submission.created_at).toLocaleDateString()}
                        </CardDescription>
                      </div>

                      {/* Score */}
                      {submission.score !== null && (
                        <div className="text-right">
                          <div
                            className={`text-2xl font-bold ${
                              submission.passed ? 'text-green-600' : 'text-red-600'
                            }`}
                          >
                            {submission.score.toFixed(1)}%
                          </div>
                          <div className="text-sm text-muted-foreground">
                            {submission.earned_points?.toFixed(1)}/
                            {submission.total_points?.toFixed(1)} pts
                          </div>
                        </div>
                      )}
                    </div>
                  </CardHeader>

                  <CardContent>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                        <span>Status: {submission.status.replace('_', ' ')}</span>
                        {submission.time_spent_minutes && (
                          <span>Time: {submission.time_spent_minutes} min</span>
                        )}
                        {submission.flagged_for_review && (
                          <Badge variant="destructive">
                            <AlertTriangle className="w-3 h-3 mr-1" />
                            Flagged
                          </Badge>
                        )}
                      </div>

                      <Button
                        variant="outline"
                        onClick={() =>
                          router.push(
                            `/assessments/${assessment.id}/results?submission=${submission.id}`
                          )
                        }
                      >
                        View Details
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              );
            })
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}
