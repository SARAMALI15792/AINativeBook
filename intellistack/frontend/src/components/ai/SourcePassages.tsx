/**
 * SourcePassages Component
 *
 * Display source passages used for answer generation (FR-075).
 */

'use client';

import { Book, ChevronDown, ChevronUp } from 'lucide-react';
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface Source {
  stage_name: string;
  content_title: string;
  text_snippet: string;
  relevance_score: number;
}

interface SourcePassagesProps {
  sources: Source[];
}

export function SourcePassages({ sources }: SourcePassagesProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!sources || sources.length === 0) {
    return null;
  }

  return (
    <Card className="mt-4">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Book className="h-4 w-4 text-muted-foreground" />
            <CardTitle className="text-sm">
              Source Passages ({sources.length})
            </CardTitle>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsExpanded(!isExpanded)}
          >
            {isExpanded ? (
              <ChevronUp className="h-4 w-4" />
            ) : (
              <ChevronDown className="h-4 w-4" />
            )}
          </Button>
        </div>
      </CardHeader>

      {isExpanded && (
        <CardContent className="space-y-3">
          {sources.map((source, idx) => (
            <div
              key={idx}
              className="p-3 border rounded-lg bg-muted/50 space-y-2"
            >
              <div className="flex items-center justify-between">
                <p className="text-sm font-semibold">
                  {source.stage_name}: {source.content_title}
                </p>
                <span className="text-xs text-muted-foreground">
                  {(source.relevance_score * 100).toFixed(0)}% relevant
                </span>
              </div>
              <p className="text-sm text-muted-foreground">
                {source.text_snippet}
              </p>
            </div>
          ))}
        </CardContent>
      )}
    </Card>
  );
}
