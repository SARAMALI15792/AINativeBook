/**
 * useAIChat Hook
 *
 * Hook for managing RAG chatbot conversations (FR-070, FR-074).
 */

import { useState, useCallback } from 'react';
import { useStreaming } from './useStreaming';

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: any[];
  confidence?: number;
  timestamp: Date;
}

export interface UseAIChatOptions {
  conversationId?: string;
  apiUrl?: string;
}

export function useAIChat(options: UseAIChatOptions = {}) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversationId, setConversationId] = useState<string | undefined>(
    options.conversationId
  );
  const apiUrl = options.apiUrl || 'http://localhost:8000/api/v1';

  const {
    isStreaming,
    streamedContent,
    sources,
    startStream,
    stopStream,
  } = useStreaming({
    onComplete: (content, sources) => {
      // Add assistant message when streaming completes
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now().toString(),
          role: 'assistant',
          content,
          sources,
          timestamp: new Date(),
        },
      ]);
    },
  });

  const sendMessage = useCallback(
    async (query: string, selectedText?: string) => {
      // Add user message immediately
      const userMessage: Message = {
        id: Date.now().toString(),
        role: 'user',
        content: query,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, userMessage]);

      // Start streaming response
      await startStream(`${apiUrl}/ai/rag/query/stream`, {
        query,
        conversation_id: conversationId,
        selected_text: selectedText,
        user_id: 'current-user-id', // TODO: Get from auth context
      });
    },
    [conversationId, apiUrl, startStream]
  );

  const clearConversation = useCallback(() => {
    setMessages([]);
    setConversationId(undefined);
  }, []);

  return {
    messages,
    isStreaming,
    streamedContent,
    sources,
    sendMessage,
    stopStream,
    clearConversation,
    conversationId,
  };
}
