/**
 * ConfidenceIndicator Component
 *
 * Shows AI response confidence level (FR-072).
 */

'use client';

import { AlertCircle, CheckCircle, AlertTriangle } from 'lucide-react';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';

interface ConfidenceIndicatorProps {
  confidence: number; // 0.0 to 1.0
}

export function ConfidenceIndicator({ confidence }: ConfidenceIndicatorProps) {
  const getConfidenceInfo = (score: number) => {
    if (score >= 0.8) {
      return {
        icon: CheckCircle,
        label: 'High Confidence',
        color: 'text-green-600',
        description: 'Strong evidence from course materials',
      };
    } else if (score >= 0.6) {
      return {
        icon: AlertTriangle,
        label: 'Medium Confidence',
        color: 'text-yellow-600',
        description: 'Moderate evidence, consider verifying',
      };
    } else {
      return {
        icon: AlertCircle,
        label: 'Low Confidence',
        color: 'text-red-600',
        description: 'Limited evidence, please verify with instructor',
      };
    }
  };

  const info = getConfidenceInfo(confidence);
  const Icon = info.icon;

  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <div className="flex items-center gap-1">
            <Icon className={`h-3 w-3 ${info.color}`} />
            <span className={`text-xs ${info.color}`}>
              {(confidence * 100).toFixed(0)}%
            </span>
          </div>
        </TooltipTrigger>
        <TooltipContent>
          <div className="space-y-1">
            <p className="font-semibold">{info.label}</p>
            <p className="text-xs text-muted-foreground">{info.description}</p>
          </div>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}
