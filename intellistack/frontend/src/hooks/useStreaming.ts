/**
 * useStreaming Hook
 *
 * Custom hook for SSE (Server-Sent Events) streaming from RAG API (FR-069, FR-135).
 */

import { useCallback, useRef, useState } from 'react';

export interface StreamChunk {
  content: string;
  is_final: boolean;
  sources?: Array<{
    stage_name: string;
    content_title: string;
    text_snippet: string;
    relevance_score: number;
  }>;
  message_id?: string;
}

export interface UseStreamingOptions {
  onChunk?: (chunk: StreamChunk) => void;
  onComplete?: (fullContent: string, sources: any[]) => void;
  onError?: (error: Error) => void;
}

export function useStreaming(options: UseStreamingOptions = {}) {
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamedContent, setStreamedContent] = useState('');
  const [sources, setSources] = useState<any[]>([]);
  const abortControllerRef = useRef<AbortController | null>(null);

  const startStream = useCallback(
    async (url: string, body: any) => {
      setIsStreaming(true);
      setStreamedContent('');
      setSources([]);

      // Create abort controller for cancellation
      abortControllerRef.current = new AbortController();

      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('token')}`, // TODO: Use proper auth
          },
          body: JSON.stringify(body),
          signal: abortControllerRef.current.signal,
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const reader = response.body?.getReader();
        const decoder = new TextDecoder();

        if (!reader) {
          throw new Error('Response body is not readable');
        }

        let buffer = '';
        let fullContent = '';

        while (true) {
          const { done, value } = await reader.read();

          if (done) {
            break;
          }

          // Decode chunk
          buffer += decoder.decode(value, { stream: true });

          // Process complete SSE messages
          const lines = buffer.split('\n');
          buffer = lines.pop() || ''; // Keep incomplete line in buffer

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const data = line.slice(6);
              try {
                const chunk: StreamChunk = JSON.parse(data);

                // Accumulate content
                if (chunk.content) {
                  fullContent += chunk.content;
                  setStreamedContent((prev) => prev + chunk.content);
                }

                // Handle final chunk with sources
                if (chunk.is_final && chunk.sources) {
                  setSources(chunk.sources);
                  if (options.onComplete) {
                    options.onComplete(fullContent, chunk.sources);
                  }
                }

                // Call chunk callback
                if (options.onChunk) {
                  options.onChunk(chunk);
                }
              } catch (e) {
                console.error('Failed to parse SSE data:', e);
              }
            }
          }
        }
      } catch (error) {
        if (error instanceof Error) {
          if (error.name !== 'AbortError') {
            console.error('Streaming error:', error);
            if (options.onError) {
              options.onError(error);
            }
          }
        }
      } finally {
        setIsStreaming(false);
        abortControllerRef.current = null;
      }
    },
    [options]
  );

  const stopStream = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
      setIsStreaming(false);
    }
  }, []);

  return {
    isStreaming,
    streamedContent,
    sources,
    startStream,
    stopStream,
  };
}
