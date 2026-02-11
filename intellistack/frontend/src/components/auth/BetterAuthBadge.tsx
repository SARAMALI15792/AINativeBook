'use client';

import { Lock } from 'lucide-react';

export function BetterAuthBadge() {
  return (
    <div className="flex items-center justify-center gap-1.5 text-xs text-muted-foreground mt-6 pt-4 border-t border-border">
      <Lock className="w-3 h-3" />
      <span>Secured by</span>
      <span className="font-semibold text-foreground">Better Auth</span>
    </div>
  );
}
