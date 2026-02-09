/**
 * Code Review Panel Component
 * Code review without solutions (FR-031)
 */

'use client';

import { useState } from 'react';
import { CodeReview } from '@/hooks/useAITutor';
import { Button } from '../ui/button';
import { Textarea } from '../ui/textarea';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Alert, AlertDescription } from '../ui/alert';
import { Badge } from '../ui/badge';
import { FileCode, Lightbulb, CheckCircle, AlertCircle, Loader2, BookOpen } from 'lucide-react';

interface CodeReviewPanelProps {
  conversationId: string;
  onRequestReview: (data: any) => void;
  isLoading: boolean;
  review?: CodeReview;
}

const LANGUAGES = [
  'Python',
  'JavaScript',
  'TypeScript',
  'C++',
  'Java',
  'Go',
  'Rust',
  'Other',
];

const SEVERITY_CONFIG = {
  low: { color: 'text-blue-600', bgColor: 'bg-blue-50', icon: AlertCircle },
  medium: { color: 'text-yellow-600', bgColor: 'bg-yellow-50', icon: AlertCircle },
  high: { color: 'text-red-600', bgColor: 'bg-red-50', icon: AlertCircle },
};

export function CodeReviewPanel({
  conversationId,
  onRequestReview,
  isLoading,
  review,
}: CodeReviewPanelProps) {
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('Python');
  const [context, setContext] = useState('');

  const handleSubmit = () => {
    if (!code || !language || !context) {
      alert('Please fill in all fields');
      return;
    }

    onRequestReview({
      conversation_id: conversationId,
      code,
      language,
      context,
    });
  };

  return (
    <div className="space-y-6">
      {/* Input Form */}
      {!review && (
        <div className="space-y-4">
          <div>
            <Label htmlFor="code">Your Code *</Label>
            <Textarea
              id="code"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="Paste the code you want reviewed..."
              className="font-mono text-sm min-h-[200px] mt-2"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="language">Programming Language *</Label>
              <Select value={language} onValueChange={setLanguage}>
                <SelectTrigger id="language" className="mt-2">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {LANGUAGES.map((lang) => (
                    <SelectItem key={lang} value={lang}>
                      {lang}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="context">Purpose/Context *</Label>
              <Input
                id="context"
                value={context}
                onChange={(e) => setContext(e.target.value)}
                placeholder="What should this code do?"
                className="mt-2"
              />
            </div>
          </div>

          <Button onClick={handleSubmit} disabled={isLoading} className="w-full">
            {isLoading ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Reviewing...
              </>
            ) : (
              <>
                <FileCode className="w-4 h-4 mr-2" />
                Get Code Review
              </>
            )}
          </Button>
        </div>
      )}

      {/* Review Display */}
      {review && (
        <div className="space-y-6">
          {/* Confirmation that no solution provided */}
          <Alert className="border-green-500 bg-green-50">
            <CheckCircle className="h-4 w-4 text-green-600" />
            <AlertDescription className="text-green-800">
              <strong>No Solutions Provided:</strong> This review highlights issues and provides
              hints, but you'll implement the fixes yourself. This is how you learn!
            </AlertDescription>
          </Alert>

          {/* Strengths */}
          {review.strengths.length > 0 && (
            <Card className="border-green-200">
              <CardHeader>
                <CardTitle className="text-lg flex items-center text-green-700">
                  <CheckCircle className="w-5 h-5 mr-2" />
                  What You Did Well
                </CardTitle>
                <CardDescription>Positive aspects of your code</CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {review.strengths.map((strength, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-green-500 mr-2">✓</span>
                      <span className="text-sm">{strength}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )}

          {/* Issues Found */}
          {review.issues.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center">
                  <AlertCircle className="w-5 h-5 mr-2" />
                  Issues to Address ({review.issues.length})
                </CardTitle>
                <CardDescription>
                  Each issue includes a hint to guide your fix
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {review.issues.map((issue, index) => {
                    const config = SEVERITY_CONFIG[issue.severity as keyof typeof SEVERITY_CONFIG] || SEVERITY_CONFIG.medium;
                    const Icon = config.icon;

                    return (
                      <div key={index} className={`border-l-4 ${config.bgColor} border-l-${issue.severity === 'high' ? 'red' : issue.severity === 'medium' ? 'yellow' : 'blue'}-500 p-4 rounded-r`}>
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center space-x-2 mb-2">
                              <Badge variant="outline" className="text-xs">
                                Line {issue.line}
                              </Badge>
                              <Badge variant="secondary" className="text-xs">
                                {issue.category}
                              </Badge>
                              <Badge
                                variant="secondary"
                                className={`text-xs ${config.color}`}
                              >
                                {issue.severity}
                              </Badge>
                            </div>
                            <p className="text-sm font-medium mb-2">{issue.description}</p>
                            <div className="bg-white p-3 rounded border mt-2">
                              <p className="text-sm text-muted-foreground">
                                <strong className="text-blue-600">💡 Hint:</strong> {issue.hint}
                              </p>
                            </div>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Improvement Questions */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center">
                <Lightbulb className="w-5 h-5 mr-2" />
                Questions to Consider
              </CardTitle>
              <CardDescription>
                Think about these as you improve your code
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {review.improvement_questions.map((question, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-blue-500 mr-2">?</span>
                    <span className="text-sm">{question}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>

          {/* Concepts to Review */}
          {review.concepts_to_review.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center">
                  <BookOpen className="w-5 h-5 mr-2" />
                  Concepts to Review
                </CardTitle>
                <CardDescription>
                  These concepts will help you understand the improvements
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {review.concepts_to_review.map((concept, index) => (
                    <Badge key={index} variant="outline" className="text-sm">
                      {concept}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Best Practices */}
          {review.best_practices.length > 0 && (
            <Card className="border-dashed">
              <CardHeader>
                <CardTitle className="text-sm font-medium">
                  Best Practices to Apply
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-1 text-sm">
                  {review.best_practices.map((practice, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-blue-500 mr-2">•</span>
                      <span>{practice}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )}

          {/* Next Steps */}
          <Alert>
            <AlertDescription className="text-sm">
              <strong>Next Steps:</strong>
              <ol className="list-decimal list-inside mt-2 space-y-1">
                <li>Address the issues above using the hints</li>
                <li>Review the concepts mentioned</li>
                <li>Apply the best practices</li>
                <li>Test your improved code</li>
                <li>Submit again for another review if needed!</li>
              </ol>
            </AlertDescription>
          </Alert>

          {/* Reset Button */}
          <Button
            variant="outline"
            className="w-full"
            onClick={() => window.location.reload()}
          >
            Review Another Code
          </Button>
        </div>
      )}

      {/* Teaching Note */}
      <Alert className="border-dashed">
        <AlertDescription className="text-xs">
          <strong>Why no direct fixes?</strong> Code review is most effective when you implement
          the improvements yourself. This builds your skills in writing better code from the start,
          not just fixing existing code.
        </AlertDescription>
      </Alert>
    </div>
  );
}
