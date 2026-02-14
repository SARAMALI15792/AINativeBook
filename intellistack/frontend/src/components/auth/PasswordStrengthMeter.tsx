'use client';

import { Check, Circle } from 'lucide-react';
import { cn } from '@/lib/utils';

const REQUIREMENTS = [
  { regex: /.{8,}/, label: 'At least 8 characters' },
  { regex: /[A-Z]/, label: 'One uppercase letter' },
  { regex: /[a-z]/, label: 'One lowercase letter' },
  { regex: /[0-9]/, label: 'One number' },
  { regex: /[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]/, label: 'One special character' },
];

interface PasswordStrengthMeterProps {
  password: string;
}

export function PasswordStrengthMeter({ password }: PasswordStrengthMeterProps) {
  const metCount = REQUIREMENTS.filter((r) => r.regex.test(password)).length;
  const percentage = (metCount / REQUIREMENTS.length) * 100;

  const getStrengthLabel = () => {
    if (percentage <= 20) return 'Very weak';
    if (percentage <= 40) return 'Weak';
    if (percentage <= 60) return 'Fair';
    if (percentage <= 80) return 'Good';
    return 'Strong';
  };

  const getBarColor = () => {
    if (percentage <= 20) return 'bg-red-500';
    if (percentage <= 40) return 'bg-orange-500';
    if (percentage <= 60) return 'bg-yellow-500';
    if (percentage <= 80) return 'bg-blue-500';
    return 'bg-green-500';
  };

  if (!password) return null;

  return (
    <div className="space-y-2 mt-2">
      {/* Strength bar */}
      <div className="space-y-1">
        <div className="h-1.5 bg-muted rounded-full overflow-hidden">
          <div
            className={cn('h-full rounded-full transition-all duration-300', getBarColor())}
            style={{ width: `${percentage}%` }}
          />
        </div>
        <p className="text-xs text-muted-foreground">
          Strength: <span className="font-medium">{getStrengthLabel()}</span>
        </p>
      </div>

      {/* Requirements checklist */}
      <ul className="space-y-1">
        {REQUIREMENTS.map((req, i) => {
          const isMet = req.regex.test(password);
          return (
            <li
              key={i}
              className={cn(
                'flex items-center gap-2 text-xs',
                isMet ? 'text-green-600' : 'text-muted-foreground'
              )}
            >
              {isMet ? (
                <Check className="w-3.5 h-3.5" />
              ) : (
                <Circle className="w-3.5 h-3.5" />
              )}
              {req.label}
            </li>
          );
        })}
      </ul>
    </div>
  );
}
