/**
 * Quiz Form Component
 * Interactive quiz taking interface (FR-043)
 */

'use client';

import { useState, useEffect } from 'react';
import { Assessment, AssessmentQuestion } from '@/hooks/useAssessment';
import { Button } from '../ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { RadioGroup, RadioGroupItem } from '../ui/radio-group';
import { Textarea } from '../ui/textarea';
import { Label } from '../ui/label';
import { Progress } from '../ui/progress';
import { Alert, AlertDescription } from '../ui/alert';
import { Badge } from '../ui/badge';
import { CheckCircle, Clock, AlertTriangle, Code, FileText } from 'lucide-react';

interface QuizFormProps {
  assessment: Assessment;
  onSubmit: (answers: Record<string, any>) => void;
  isSubmitting: boolean;
  timeRemaining?: number; // seconds
}

export function QuizForm({ assessment, onSubmit, isSubmitting, timeRemaining }: QuizFormProps) {
  const [answers, setAnswers] = useState<Record<string, any>>({});
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [showValidation, setShowValidation] = useState(false);

  const questions = assessment.questions.sort((a, b) => a.order_index - b.order_index);
  const currentQuestion = questions[currentQuestionIndex];
  const progress = ((currentQuestionIndex + 1) / questions.length) * 100;

  // Format time remaining
  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  // Auto-submit when time runs out
  useEffect(() => {
    if (timeRemaining === 0) {
      handleSubmit();
    }
  }, [timeRemaining]);

  const handleAnswerChange = (questionId: string, value: any) => {
    setAnswers((prev) => ({
      ...prev,
      [questionId]: value,
    }));
    setShowValidation(false);
  };

  const isQuestionAnswered = (questionId: string) => {
    const answer = answers[questionId];
    if (answer === undefined || answer === null) return false;
    if (typeof answer === 'string') return answer.trim().length > 0;
    return true;
  };

  const getAnsweredCount = () => {
    return questions.filter((q) => isQuestionAnswered(q.id)).length;
  };

  const handleNext = () => {
    if (!isQuestionAnswered(currentQuestion.id)) {
      setShowValidation(true);
      return;
    }

    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex((prev) => prev + 1);
      setShowValidation(false);
    }
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex((prev) => prev - 1);
      setShowValidation(false);
    }
  };

  const handleSubmit = () => {
    const unanswered = questions.filter((q) => !isQuestionAnswered(q.id));

    if (unanswered.length > 0 && timeRemaining !== 0) {
      const confirm = window.confirm(
        `You have ${unanswered.length} unanswered question(s). Submit anyway?`
      );
      if (!confirm) return;
    }

    onSubmit(answers);
  };

  return (
    <div className="space-y-6">
      {/* Header with Progress */}
      <Card>
        <CardContent className="pt-6">
          <div className="space-y-4">
            {/* Progress Bar */}
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="font-medium">
                  Question {currentQuestionIndex + 1} of {questions.length}
                </span>
                <span className="text-muted-foreground">
                  {getAnsweredCount()} / {questions.length} answered
                </span>
              </div>
              <Progress value={progress} className="h-2" />
            </div>

            {/* Time and Stats */}
            <div className="flex items-center justify-between text-sm">
              <div className="flex items-center space-x-4">
                <Badge variant="outline">
                  <FileText className="w-3 h-3 mr-1" />
                  {assessment.questions.length} Questions
                </Badge>
                <Badge variant="outline">Target: {assessment.passing_score}%</Badge>
              </div>

              {timeRemaining !== undefined && (
                <div
                  className={`flex items-center space-x-2 font-mono ${
                    timeRemaining < 300 ? 'text-red-600 font-bold' : ''
                  }`}
                >
                  <Clock className="w-4 h-4" />
                  <span>{formatTime(timeRemaining)}</span>
                </div>
              )}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Current Question */}
      <Card>
        <CardHeader>
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center space-x-2 mb-2">
                <Badge variant="secondary">
                  {currentQuestion.question_type.replace('_', ' ')}
                </Badge>
                <Badge variant="outline">{currentQuestion.points} pts</Badge>
              </div>
              <CardTitle className="text-lg">{currentQuestion.question_text}</CardTitle>
            </div>

            {isQuestionAnswered(currentQuestion.id) && (
              <CheckCircle className="w-5 h-5 text-green-600" />
            )}
          </div>
        </CardHeader>

        <CardContent className="space-y-4">
          {/* Multiple Choice */}
          {currentQuestion.question_type === 'multiple_choice' && currentQuestion.options && (
            <RadioGroup
              value={answers[currentQuestion.id] || ''}
              onValueChange={(value) => handleAnswerChange(currentQuestion.id, value)}
            >
              <div className="space-y-3">
                {currentQuestion.options.map((option: any) => (
                  <div
                    key={option.id}
                    className="flex items-center space-x-3 border rounded-lg p-4 hover:bg-gray-50 cursor-pointer"
                  >
                    <RadioGroupItem value={option.id} id={option.id} />
                    <Label htmlFor={option.id} className="flex-1 cursor-pointer">
                      {option.text}
                    </Label>
                  </div>
                ))}
              </div>
            </RadioGroup>
          )}

          {/* Code Question */}
          {currentQuestion.question_type === 'code' && (
            <div className="space-y-3">
              {currentQuestion.starter_code && (
                <div>
                  <Label className="text-sm text-muted-foreground mb-2 block">
                    Starter Code:
                  </Label>
                  <pre className="bg-gray-100 p-4 rounded font-mono text-sm overflow-x-auto">
                    {currentQuestion.starter_code}
                  </pre>
                </div>
              )}
              <div>
                <Label htmlFor={`code-${currentQuestion.id}`} className="mb-2 block">
                  Your Code:
                </Label>
                <Textarea
                  id={`code-${currentQuestion.id}`}
                  value={answers[currentQuestion.id] || ''}
                  onChange={(e) => handleAnswerChange(currentQuestion.id, e.target.value)}
                  placeholder="Write your code here..."
                  className="font-mono text-sm min-h-[200px]"
                />
              </div>
            </div>
          )}

          {/* Essay Question */}
          {currentQuestion.question_type === 'essay' && (
            <div>
              <Textarea
                value={answers[currentQuestion.id] || ''}
                onChange={(e) => handleAnswerChange(currentQuestion.id, e.target.value)}
                placeholder="Type your answer here..."
                className="min-h-[150px]"
              />
              <p className="text-sm text-muted-foreground mt-2">
                {answers[currentQuestion.id]?.length || 0} characters
              </p>
            </div>
          )}

          {/* Validation Warning */}
          {showValidation && !isQuestionAnswered(currentQuestion.id) && (
            <Alert variant="destructive">
              <AlertTriangle className="h-4 w-4" />
              <AlertDescription>Please answer this question before proceeding.</AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>

      {/* Navigation */}
      <div className="flex justify-between">
        <Button variant="outline" onClick={handlePrevious} disabled={currentQuestionIndex === 0}>
          Previous
        </Button>

        <div className="flex space-x-2">
          {currentQuestionIndex < questions.length - 1 ? (
            <Button onClick={handleNext}>Next</Button>
          ) : (
            <Button onClick={handleSubmit} disabled={isSubmitting} className="bg-green-600">
              {isSubmitting ? 'Submitting...' : 'Submit Assessment'}
            </Button>
          )}
        </div>
      </div>

      {/* Question Navigator */}
      <Card>
        <CardHeader>
          <CardTitle className="text-sm">Question Navigator</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-10 gap-2">
            {questions.map((q, index) => (
              <Button
                key={q.id}
                variant={index === currentQuestionIndex ? 'default' : 'outline'}
                size="sm"
                className={`w-full ${
                  isQuestionAnswered(q.id) && index !== currentQuestionIndex
                    ? 'border-green-500 bg-green-50'
                    : ''
                }`}
                onClick={() => {
                  setCurrentQuestionIndex(index);
                  setShowValidation(false);
                }}
              >
                {index + 1}
                {isQuestionAnswered(q.id) && (
                  <CheckCircle className="w-3 h-3 ml-1 text-green-600" />
                )}
              </Button>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
