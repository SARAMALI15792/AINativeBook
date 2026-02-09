/**
 * Feedback Display Component
 * Shows assessment results and feedback (FR-048)
 */

'use client';

import { AssessmentResult } from '@/hooks/useAssessment';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Alert, AlertDescription } from '../ui/alert';
import { Badge } from '../ui/badge';
import { Progress } from '../ui/progress';
import {
  CheckCircle,
  XCircle,
  AlertCircle,
  TrendingUp,
  Award,
  Clock,
  Target,
} from 'lucide-react';

interface FeedbackDisplayProps {
  result: AssessmentResult;
}

export function FeedbackDisplay({ result }: FeedbackDisplayProps) {
  const { submission, assessment, answers_with_feedback, passed, attempts_remaining, can_retake } =
    result;

  const scorePercentage = submission.score || 0;
  const isAutoGraded = submission.auto_graded;

  return (
    <div className="space-y-6">
      {/* Overall Result */}
      <Card className={passed ? 'border-green-500 bg-green-50' : 'border-red-500 bg-red-50'}>
        <CardContent className="pt-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              {passed ? (
                <CheckCircle className="w-12 h-12 text-green-600" />
              ) : (
                <XCircle className="w-12 h-12 text-red-600" />
              )}
              <div>
                <h2
                  className={`text-2xl font-bold ${
                    passed ? 'text-green-700' : 'text-red-700'
                  }`}
                >
                  {passed ? 'Passed!' : 'Not Passed'}
                </h2>
                <p className="text-sm text-muted-foreground">
                  {passed
                    ? 'Congratulations on passing this assessment!'
                    : 'Keep learning and try again!'}
                </p>
              </div>
            </div>

            <div className="text-right">
              <div className={`text-4xl font-bold ${passed ? 'text-green-600' : 'text-red-600'}`}>
                {scorePercentage.toFixed(1)}%
              </div>
              <div className="text-sm text-muted-foreground">
                {submission.earned_points?.toFixed(1)} / {submission.total_points?.toFixed(1)}{' '}
                points
              </div>
            </div>
          </div>

          {/* Progress Bar */}
          <div className="mt-6">
            <div className="flex justify-between text-sm mb-2">
              <span>Your Score</span>
              <span>Passing: {assessment.passing_score}%</span>
            </div>
            <Progress
              value={scorePercentage}
              className="h-3"
              indicatorClassName={passed ? 'bg-green-600' : 'bg-red-600'}
            />
          </div>
        </CardContent>
      </Card>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-3">
              <Award className="w-8 h-8 text-blue-600" />
              <div>
                <div className="text-2xl font-bold">{scorePercentage.toFixed(0)}%</div>
                <div className="text-xs text-muted-foreground">Score</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-3">
              <Target className="w-8 h-8 text-green-600" />
              <div>
                <div className="text-2xl font-bold">{assessment.passing_score}%</div>
                <div className="text-xs text-muted-foreground">Passing</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-3">
              <Clock className="w-8 h-8 text-purple-600" />
              <div>
                <div className="text-2xl font-bold">{submission.time_spent_minutes || 0}</div>
                <div className="text-xs text-muted-foreground">Minutes</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-3">
              <TrendingUp className="w-8 h-8 text-orange-600" />
              <div>
                <div className="text-2xl font-bold">#{submission.attempt_number}</div>
                <div className="text-xs text-muted-foreground">Attempt</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Retake Info */}
      {!passed && can_retake && (
        <Alert>
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            <strong>You can retake this assessment.</strong>
            {attempts_remaining !== undefined && attempts_remaining > 0 && (
              <span> You have {attempts_remaining} attempt(s) remaining.</span>
            )}
            <br />
            Review the feedback below and try again when ready.
          </AlertDescription>
        </Alert>
      )}

      {!passed && !can_retake && (
        <Alert variant="destructive">
          <AlertDescription>
            You have used all available attempts for this assessment.
          </AlertDescription>
        </Alert>
      )}

      {/* General Feedback */}
      {submission.feedback && (
        <Card>
          <CardHeader>
            <CardTitle>Instructor Feedback</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm whitespace-pre-wrap">{submission.feedback}</p>
          </CardContent>
        </Card>
      )}

      {/* Auto-graded Notice */}
      {isAutoGraded && (
        <Alert>
          <AlertDescription>
            <strong>Note:</strong> This assessment was automatically graded. Detailed feedback is
            shown below for each question.
          </AlertDescription>
        </Alert>
      )}

      {/* Question-by-Question Feedback */}
      {answers_with_feedback.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Question Feedback</CardTitle>
            <CardDescription>Review your answers and learn from mistakes</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {answers_with_feedback.map((item, index) => {
              const isCorrect =
                item.correct_answer && item.student_answer === item.correct_answer;

              return (
                <div key={item.question_id} className="border-b pb-6 last:border-b-0 last:pb-0">
                  {/* Question Header */}
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-2">
                        <Badge variant="outline">Question {index + 1}</Badge>
                        <Badge variant="secondary">{item.points} pts</Badge>
                        {isCorrect !== undefined && (
                          <Badge
                            variant={isCorrect ? 'default' : 'destructive'}
                            className={isCorrect ? 'bg-green-600' : ''}
                          >
                            {isCorrect ? (
                              <>
                                <CheckCircle className="w-3 h-3 mr-1" />
                                Correct
                              </>
                            ) : (
                              <>
                                <XCircle className="w-3 h-3 mr-1" />
                                Incorrect
                              </>
                            )}
                          </Badge>
                        )}
                      </div>
                      <p className="font-medium">{item.question_text}</p>
                    </div>
                  </div>

                  {/* Your Answer */}
                  <div className="bg-gray-50 p-4 rounded mb-3">
                    <div className="text-sm font-medium text-muted-foreground mb-1">
                      Your Answer:
                    </div>
                    <div className="text-sm">
                      {item.student_answer || (
                        <span className="text-muted-foreground italic">No answer provided</span>
                      )}
                    </div>
                  </div>

                  {/* Correct Answer (only if passed or for review) */}
                  {item.correct_answer && passed && (
                    <div className="bg-green-50 p-4 rounded mb-3">
                      <div className="text-sm font-medium text-green-700 mb-1">
                        Correct Answer:
                      </div>
                      <div className="text-sm text-green-800">{item.correct_answer}</div>
                    </div>
                  )}

                  {/* Explanation */}
                  {item.explanation && (
                    <Alert>
                      <AlertDescription className="text-sm">{item.explanation}</AlertDescription>
                    </Alert>
                  )}
                </div>
              );
            })}
          </CardContent>
        </Card>
      )}

      {/* Similarity Warning */}
      {submission.flagged_for_review && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            <strong>Similarity Detected:</strong> This submission has been flagged for review due
            to high similarity with other submissions (
            {submission.similarity_score?.toFixed(1)}%). An instructor will review this assessment.
          </AlertDescription>
        </Alert>
      )}
    </div>
  );
}
