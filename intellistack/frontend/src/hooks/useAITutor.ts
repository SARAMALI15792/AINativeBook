/**
 * AI Tutor Hook
 * Manages tutor conversations and Socratic interactions
 * FR-026 to FR-035
 */

import { useState, useCallback } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../lib/api';

export interface TutorConversation {
  id: string;
  user_id: string;
  stage_id?: string;
  content_id?: string;
  title: string;
  intent_type?: string;
  created_at: string;
  updated_at: string;
  messages: TutorMessage[];
  recent_guardrails: GuardrailEvent[];
}

export interface TutorMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  response_type?: string;
  socratic_strategy?: string;
  provided_hints?: string[];
  code_issues?: CodeIssue[];
  debugging_steps?: string[];
  confidence_score?: number;
  created_at: string;
}

export interface CodeIssue {
  line: string;
  type: string;
  description: string;
  hint: string;
}

export interface GuardrailEvent {
  id: string;
  guardrail_type: string;
  trigger_reason: string;
  escalated: boolean;
  created_at: string;
}

export interface TutorResponse {
  message_id: string;
  conversation_id: string;
  content: string;
  response_type: string;
  guiding_questions?: string[];
  hints?: string[];
  code_issues?: CodeIssue[];
  debugging_steps?: string[];
  systematic_approach?: string;
  guardrail_triggered: boolean;
  guardrail_message?: string;
  adapted_for_level?: number;
  explanation_depth?: string;
  escalation_available: boolean;
  escalation_reason?: string;
}

export interface DebuggingGuidance {
  message_id: string;
  conversation_id: string;
  observation: string;
  hypothesis: string[];
  verification_steps: Array<{
    step: string;
    action: string;
    expected_result: string;
  }>;
  hints: string[];
  guiding_questions: string[];
  relevant_concepts: string[];
  documentation_links?: Array<{
    title: string;
    url: string;
  }>;
}

export interface CodeReview {
  message_id: string;
  conversation_id: string;
  issues: Array<{
    line: string;
    severity: string;
    category: string;
    description: string;
    hint: string;
  }>;
  strengths: string[];
  improvement_questions: string[];
  concepts_to_review: string[];
  best_practices: string[];
  solution_provided: boolean;
}

export function useAITutor() {
  const queryClient = useQueryClient();
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);

  // Create conversation
  const createConversation = useMutation({
    mutationFn: async (data: {
      stage_id?: string;
      content_id?: string;
      initial_message: string;
      code_snippet?: string;
    }) => {
      const response = await apiClient.post('/ai/tutor/conversations', data);
      return response.data as TutorConversation;
    },
    onSuccess: (conversation) => {
      setCurrentConversationId(conversation.id);
      queryClient.invalidateQueries({ queryKey: ['tutor-conversations'] });
    },
  });

  // Get conversation
  const { data: conversation, isLoading: conversationLoading } = useQuery({
    queryKey: ['tutor-conversation', currentConversationId],
    queryFn: async () => {
      if (!currentConversationId) return null;
      const response = await apiClient.get(`/ai/tutor/conversations/${currentConversationId}`);
      return response.data as TutorConversation;
    },
    enabled: !!currentConversationId,
  });

  // Send message
  const sendMessage = useMutation({
    mutationFn: async (data: {
      conversation_id: string;
      content: string;
      code_snippet?: string;
      understanding_level?: number;
    }) => {
      const response = await apiClient.post(
        `/ai/tutor/conversations/${data.conversation_id}/messages`,
        {
          content: data.content,
          code_snippet: data.code_snippet,
          understanding_level: data.understanding_level,
        }
      );
      return response.data as TutorResponse;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tutor-conversation', currentConversationId] });
    },
  });

  // Request debugging help
  const requestDebuggingHelp = useMutation({
    mutationFn: async (data: {
      conversation_id?: string;
      code: string;
      error_message?: string;
      expected_behavior: string;
      actual_behavior: string;
      stage_id?: string;
    }) => {
      const response = await apiClient.post('/ai/tutor/debugging-help', data);
      return response.data as DebuggingGuidance;
    },
    onSuccess: (_, variables) => {
      if (variables.conversation_id) {
        queryClient.invalidateQueries({ queryKey: ['tutor-conversation', variables.conversation_id] });
      }
    },
  });

  // Request code review
  const requestCodeReview = useMutation({
    mutationFn: async (data: {
      conversation_id?: string;
      code: string;
      language: string;
      context: string;
      stage_id?: string;
    }) => {
      const response = await apiClient.post('/ai/tutor/code-review', data);
      return response.data as CodeReview;
    },
    onSuccess: (_, variables) => {
      if (variables.conversation_id) {
        queryClient.invalidateQueries({ queryKey: ['tutor-conversation', variables.conversation_id] });
      }
    },
  });

  // Escalate to instructor
  const escalateToInstructor = useMutation({
    mutationFn: async (data: {
      conversation_id: string;
      reason: string;
    }) => {
      const response = await apiClient.post(
        `/ai/tutor/conversations/${data.conversation_id}/escalate`,
        { reason: data.reason }
      );
      return response.data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['tutor-conversation', variables.conversation_id] });
    },
  });

  return {
    // State
    currentConversationId,
    setCurrentConversationId,
    conversation,
    conversationLoading,

    // Mutations
    createConversation,
    sendMessage,
    requestDebuggingHelp,
    requestCodeReview,
    escalateToInstructor,

    // Loading states
    isCreating: createConversation.isPending,
    isSending: sendMessage.isPending,
    isRequestingDebug: requestDebuggingHelp.isPending,
    isRequestingReview: requestCodeReview.isPending,
    isEscalating: escalateToInstructor.isPending,
  };
}
