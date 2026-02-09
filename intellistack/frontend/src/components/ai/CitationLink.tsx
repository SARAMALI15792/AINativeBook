/**
 * CitationLink Component
 *
 * Clickable citation link to source content (FR-067, FR-075, FR-132).
 */

'use client';

import { ExternalLink } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';

interface CitationLinkProps {
  stageName: string;
  contentTitle: string;
  relevanceScore?: number;
  onClick?: () => void;
}

export function CitationLink({
  stageName,
  contentTitle,
  relevanceScore,
  onClick,
}: CitationLinkProps) {
  const citation = `${stageName}: ${contentTitle}`;

  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <Badge
            variant="outline"
            className="cursor-pointer hover:bg-accent transition-colors"
            onClick={onClick}
          >
            <ExternalLink className="h-3 w-3 mr-1" />
            {citation}
          </Badge>
        </TooltipTrigger>
        <TooltipContent>
          <div className="space-y-1">
            <p className="font-semibold">{contentTitle}</p>
            <p className="text-xs text-muted-foreground">{stageName}</p>
            {relevanceScore && (
              <p className="text-xs">
                Relevance: {(relevanceScore * 100).toFixed(0)}%
              </p>
            )}
            <p className="text-xs text-muted-foreground">Click to view source</p>
          </div>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}
