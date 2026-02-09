/**
 * Debugging Helper Component
 * Systematic debugging guidance (FR-030)
 */

'use client';

import { useState } from 'react';
import { DebuggingGuidance } from '@/hooks/useAITutor';
import { Button } from '../ui/button';
import { Textarea } from '../ui/textarea';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Alert, AlertDescription } from '../ui/alert';
import { Badge } from '../ui/badge';
import { Bug, Lightbulb, CheckSquare, Loader2, HelpCircle } from 'lucide-react';

interface DebuggingHelperProps {
  conversationId: string;
  onRequestHelp: (data: any) => void;
  isLoading: boolean;
  guidance?: DebuggingGuidance;
}

export function DebuggingHelper({
  conversationId,
  onRequestHelp,
  isLoading,
  guidance,
}: DebuggingHelperProps) {
  const [code, setCode] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [expectedBehavior, setExpectedBehavior] = useState('');
  const [actualBehavior, setActualBehavior] = useState('');

  const handleSubmit = () => {
    if (!code || !expectedBehavior || !actualBehavior) {
      alert('Please fill in all required fields');
      return;
    }

    onRequestHelp({
      conversation_id: conversationId,
      code,
      error_message: errorMessage || undefined,
      expected_behavior: expectedBehavior,
      actual_behavior: actualBehavior,
    });
  };

  return (
    <div className="space-y-6">
      {/* Input Form */}
      {!guidance && (
        <div className="space-y-4">
          <div>
            <Label htmlFor="code">Code with Issue *</Label>
            <Textarea
              id="code"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="Paste the code that's not working..."
              className="font-mono text-sm min-h-[150px] mt-2"
            />
          </div>

          <div>
            <Label htmlFor="error">Error Message (Optional)</Label>
            <Input
              id="error"
              value={errorMessage}
              onChange={(e) => setErrorMessage(e.target.value)}
              placeholder="Copy the error message if there is one"
              className="mt-2"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="expected">Expected Behavior *</Label>
              <Textarea
                id="expected"
                value={expectedBehavior}
                onChange={(e) => setExpectedBehavior(e.target.value)}
                placeholder="What should happen?"
                className="mt-2 min-h-[80px]"
              />
            </div>

            <div>
              <Label htmlFor="actual">Actual Behavior *</Label>
              <Textarea
                id="actual"
                value={actualBehavior}
                onChange={(e) => setActualBehavior(e.target.value)}
                placeholder="What actually happens?"
                className="mt-2 min-h-[80px]"
              />
            </div>
          </div>

          <Button onClick={handleSubmit} disabled={isLoading} className="w-full">
            {isLoading ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Bug className="w-4 h-4 mr-2" />
                Get Debugging Guidance
              </>
            )}
          </Button>
        </div>
      )}

      {/* Guidance Display */}
      {guidance && (
        <div className="space-y-6">
          {/* Observation */}
          <Alert>
            <Bug className="h-4 w-4" />
            <AlertDescription>
              <strong>Observation:</strong> {guidance.observation}
            </AlertDescription>
          </Alert>

          {/* Hypotheses */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center">
                <HelpCircle className="w-5 h-5 mr-2" />
                Possible Causes to Investigate
              </CardTitle>
              <CardDescription>
                These are hypotheses - you'll verify which one is correct
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {guidance.hypothesis.map((hyp, index) => (
                  <li key={index} className="flex items-start">
                    <Badge variant="outline" className="mr-2 mt-0.5">
                      {index + 1}
                    </Badge>
                    <span>{hyp}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>

          {/* Verification Steps */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center">
                <CheckSquare className="w-5 h-5 mr-2" />
                Systematic Verification Steps
              </CardTitle>
              <CardDescription>Follow these steps to find the root cause</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {guidance.verification_steps.map((step, index) => (
                  <div key={index} className="border-l-4 border-blue-500 pl-4 py-2">
                    <h4 className="font-semibold text-sm">{step.step}</h4>
                    <p className="text-sm text-muted-foreground mt-1">
                      <strong>Action:</strong> {step.action}
                    </p>
                    <p className="text-sm text-green-600 mt-1">
                      <strong>Expected Result:</strong> {step.expected_result}
                    </p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Guiding Questions */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center">
                <Lightbulb className="w-5 h-5 mr-2" />
                Questions to Guide Your Thinking
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {guidance.guiding_questions.map((question, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-blue-500 mr-2">?</span>
                    <span className="text-sm">{question}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>

          {/* Hints */}
          {guidance.hints.length > 0 && (
            <Card className="border-dashed">
              <CardHeader>
                <CardTitle className="text-sm font-medium">Hints (No Spoilers!)</CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-1 text-sm text-muted-foreground">
                  {guidance.hints.map((hint, index) => (
                    <li key={index}>💡 {hint}</li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )}

          {/* Relevant Concepts */}
          {guidance.relevant_concepts.length > 0 && (
            <div>
              <h4 className="text-sm font-medium mb-2">Concepts to Review:</h4>
              <div className="flex flex-wrap gap-2">
                {guidance.relevant_concepts.map((concept, index) => (
                  <Badge key={index} variant="secondary">
                    {concept}
                  </Badge>
                ))}
              </div>
            </div>
          )}

          {/* Reset Button */}
          <Button
            variant="outline"
            className="w-full"
            onClick={() => window.location.reload()}
          >
            Debug Another Issue
          </Button>
        </div>
      )}

      {/* Teaching Note */}
      <Alert className="border-dashed">
        <AlertDescription className="text-xs">
          <strong>Teaching Philosophy:</strong> Debugging is a skill. By following systematic steps
          and asking the right questions, you'll learn to debug on your own. The goal isn't just to
          fix this bug - it's to teach you how to fix any bug!
        </AlertDescription>
      </Alert>
    </div>
  );
}
