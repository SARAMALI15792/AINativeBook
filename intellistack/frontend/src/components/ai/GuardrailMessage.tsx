/**
 * Guardrail Message Component
 * Shows when guardrails are triggered (FR-027, FR-028)
 */

'use client';

import { Alert, AlertDescription, AlertTitle } from '../ui/alert';
import { Shield, AlertTriangle, Info } from 'lucide-react';

interface GuardrailMessageProps {
  type: string;
  reason: string;
  className?: string;
}

const guardrailConfig = {
  socratic_redirect: {
    icon: Shield,
    title: 'Guided Learning Active',
    variant: 'default' as const,
    color: 'text-blue-600',
    bgColor: 'bg-blue-50 border-blue-200',
  },
  code_solution_blocked: {
    icon: AlertTriangle,
    title: 'Solution Blocked',
    variant: 'default' as const,
    color: 'text-orange-600',
    bgColor: 'bg-orange-50 border-orange-200',
  },
  escalation_triggered: {
    icon: Info,
    title: 'Escalation Available',
    variant: 'default' as const,
    color: 'text-purple-600',
    bgColor: 'bg-purple-50 border-purple-200',
  },
  understanding_check: {
    icon: Info,
    title: 'Understanding Verification',
    variant: 'default' as const,
    color: 'text-green-600',
    bgColor: 'bg-green-50 border-green-200',
  },
  hint_only: {
    icon: Info,
    title: 'Hint Provided',
    variant: 'default' as const,
    color: 'text-indigo-600',
    bgColor: 'bg-indigo-50 border-indigo-200',
  },
};

export function GuardrailMessage({ type, reason, className }: GuardrailMessageProps) {
  const config = guardrailConfig[type as keyof typeof guardrailConfig] || guardrailConfig.hint_only;
  const Icon = config.icon;

  return (
    <Alert className={`mt-2 ${config.bgColor} ${className}`}>
      <Icon className={`h-4 w-4 ${config.color}`} />
      <AlertTitle className={config.color}>{config.title}</AlertTitle>
      <AlertDescription className="text-sm">
        {reason}
        <div className="mt-2 text-xs text-muted-foreground">
          {type === 'socratic_redirect' && (
            <p>
              🎓 <strong>Why?</strong> Learning through guided discovery helps you develop
              problem-solving skills that last beyond this specific question.
            </p>
          )}
          {type === 'code_solution_blocked' && (
            <p>
              💡 <strong>Why?</strong> Providing complete solutions prevents learning. I'll guide
              you so you can solve it yourself!
            </p>
          )}
          {type === 'escalation_triggered' && (
            <p>
              👨‍🏫 <strong>Note:</strong> You may benefit from instructor support for this
              question.
            </p>
          )}
        </div>
      </AlertDescription>
    </Alert>
  );
}
