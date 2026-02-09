/**
 * Peer Review Form Component
 * Submit peer review for submissions (FR-051)
 */

'use client';

import { useState } from 'react';
import { Button } from '../ui/button';
import { Textarea } from '../ui/textarea';
import { Label } from '../ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { RadioGroup, RadioGroupItem } from '../ui/radio-group';
import { Star, Loader2 } from 'lucide-react';

interface PeerReviewFormProps {
  submissionId: string;
  onSubmit: (data: {
    rating?: number;
    strengths?: string;
    areas_for_improvement?: string;
    overall_feedback?: string;
  }) => void;
  isSubmitting: boolean;
}

export function PeerReviewForm({ submissionId, onSubmit, isSubmitting }: PeerReviewFormProps) {
  const [rating, setRating] = useState<number | undefined>(undefined);
  const [strengths, setStrengths] = useState('');
  const [areasForImprovement, setAreasForImprovement] = useState('');
  const [overallFeedback, setOverallFeedback] = useState('');

  const handleSubmit = () => {
    if (!rating || !strengths || !areasForImprovement || !overallFeedback) {
      alert('Please fill in all fields');
      return;
    }

    onSubmit({
      rating,
      strengths,
      areas_for_improvement: areasForImprovement,
      overall_feedback: overallFeedback,
    });
  };

  return (
    <div className="space-y-6">
      {/* Instructions */}
      <Card>
        <CardHeader>
          <CardTitle>Peer Review Guidelines</CardTitle>
          <CardDescription>
            Provide constructive feedback to help your peer improve
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground">
            <li>Be specific and constructive in your feedback</li>
            <li>Highlight both strengths and areas for improvement</li>
            <li>Focus on the work, not the person</li>
            <li>Provide actionable suggestions</li>
            <li>Be respectful and professional</li>
          </ul>
        </CardContent>
      </Card>

      {/* Rating */}
      <Card>
        <CardHeader>
          <Label>Overall Rating *</Label>
          <CardDescription>Rate the overall quality of the submission</CardDescription>
        </CardHeader>
        <CardContent>
          <RadioGroup
            value={rating?.toString()}
            onValueChange={(v) => setRating(parseInt(v))}
            className="space-y-3"
          >
            {[5, 4, 3, 2, 1].map((value) => (
              <div key={value} className="flex items-center space-x-3 border rounded-lg p-3">
                <RadioGroupItem value={value.toString()} id={`rating-${value}`} />
                <Label htmlFor={`rating-${value}`} className="flex items-center space-x-2 flex-1 cursor-pointer">
                  <div className="flex">
                    {Array.from({ length: value }).map((_, i) => (
                      <Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                    ))}
                    {Array.from({ length: 5 - value }).map((_, i) => (
                      <Star key={i} className="w-4 h-4 text-gray-300" />
                    ))}
                  </div>
                  <span className="text-sm">
                    {value === 5 && 'Excellent'}
                    {value === 4 && 'Good'}
                    {value === 3 && 'Satisfactory'}
                    {value === 2 && 'Needs Improvement'}
                    {value === 1 && 'Poor'}
                  </span>
                </Label>
              </div>
            ))}
          </RadioGroup>
        </CardContent>
      </Card>

      {/* Strengths */}
      <Card>
        <CardHeader>
          <Label htmlFor="strengths">Strengths *</Label>
          <CardDescription>What did the student do well?</CardDescription>
        </CardHeader>
        <CardContent>
          <Textarea
            id="strengths"
            value={strengths}
            onChange={(e) => setStrengths(e.target.value)}
            placeholder="List specific strengths in the submission..."
            className="min-h-[100px]"
          />
        </CardContent>
      </Card>

      {/* Areas for Improvement */}
      <Card>
        <CardHeader>
          <Label htmlFor="improvement">Areas for Improvement *</Label>
          <CardDescription>What could be improved?</CardDescription>
        </CardHeader>
        <CardContent>
          <Textarea
            id="improvement"
            value={areasForImprovement}
            onChange={(e) => setAreasForImprovement(e.target.value)}
            placeholder="Provide constructive suggestions for improvement..."
            className="min-h-[100px]"
          />
        </CardContent>
      </Card>

      {/* Overall Feedback */}
      <Card>
        <CardHeader>
          <Label htmlFor="feedback">Overall Feedback *</Label>
          <CardDescription>Summarize your review</CardDescription>
        </CardHeader>
        <CardContent>
          <Textarea
            id="feedback"
            value={overallFeedback}
            onChange={(e) => setOverallFeedback(e.target.value)}
            placeholder="Provide overall feedback and suggestions..."
            className="min-h-[120px]"
          />
        </CardContent>
      </Card>

      {/* Submit */}
      <div className="flex justify-end space-x-4">
        <Button variant="outline" disabled={isSubmitting}>
          Save Draft
        </Button>
        <Button onClick={handleSubmit} disabled={isSubmitting}>
          {isSubmitting ? (
            <>
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              Submitting...
            </>
          ) : (
            'Submit Review'
          )}
        </Button>
      </div>
    </div>
  );
}
