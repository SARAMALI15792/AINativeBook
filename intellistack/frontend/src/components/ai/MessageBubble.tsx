/**
 * MessageBubble Component
 *
 * Individual message display with streaming support and citations (FR-067, FR-132).
 */

'use client';

import { Bot, User, Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';
import { CitationLink } from './CitationLink';
import { ConfidenceIndicator } from './ConfidenceIndicator';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: any[];
  confidence?: number;
  timestamp: Date;
}

interface MessageBubbleProps {
  message: Message;
  isStreaming?: boolean;
}

export function MessageBubble({ message, isStreaming }: MessageBubbleProps) {
  const isUser = message.role === 'user';

  return (
    <div
      className={cn(
        'flex gap-3 p-4 rounded-lg',
        isUser ? 'bg-muted ml-auto max-w-[80%]' : 'bg-card'
      )}
    >
      {/* Avatar */}
      <div
        className={cn(
          'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center',
          isUser ? 'bg-primary text-primary-foreground' : 'bg-secondary'
        )}
      >
        {isUser ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
      </div>

      {/* Content */}
      <div className="flex-1 space-y-2">
        <div className="flex items-center gap-2">
          <span className="text-sm font-semibold">
            {isUser ? 'You' : 'AI Assistant'}
          </span>
          {isStreaming && (
            <Loader2 className="h-3 w-3 animate-spin text-muted-foreground" />
          )}
          {message.confidence && (
            <ConfidenceIndicator confidence={message.confidence} />
          )}
        </div>

        {/* Message content */}
        <div className="text-sm whitespace-pre-wrap">{message.content}</div>

        {/* Sources/Citations */}
        {message.sources && message.sources.length > 0 && (
          <div className="mt-3 space-y-1">
            <p className="text-xs font-semibold text-muted-foreground">
              Sources:
            </p>
            <div className="flex flex-wrap gap-2">
              {message.sources.map((source, idx) => (
                <CitationLink
                  key={idx}
                  stageName={source.stage_name}
                  contentTitle={source.content_title}
                  relevanceScore={source.relevance_score}
                />
              ))}
            </div>
          </div>
        )}

        {/* Timestamp */}
        <p className="text-xs text-muted-foreground">
          {message.timestamp.toLocaleTimeString()}
        </p>
      </div>
    </div>
  );
}
