/**
 * AI Tutor Page
 * Socratic guidance interface (FR-026 to FR-035)
 */

'use client';

import { useState, useEffect, useRef } from 'react';
import { useAITutor } from '@/hooks/useAITutor';
import { TutorChatInterface } from '@/components/ai/TutorChatInterface';
import { DebuggingHelper } from '@/components/ai/DebuggingHelper';
import { CodeReviewPanel } from '@/components/ai/CodeReviewPanel';
import { GuardrailMessage } from '@/components/ai/GuardrailMessage';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { MessageSquare, Bug, FileCode, AlertTriangle, Loader2 } from 'lucide-react';

export default function AITutorPage() {
  const {
    currentConversationId,
    conversation,
    conversationLoading,
    createConversation,
    sendMessage,
    requestDebuggingHelp,
    requestCodeReview,
    escalateToInstructor,
    isCreating,
    isSending,
  } = useAITutor();

  const [activeTab, setActiveTab] = useState<'chat' | 'debug' | 'review'>('chat');
  const [showEscalation, setShowEscalation] = useState(false);

  // Auto-create conversation on mount if none exists
  useEffect(() => {
    if (!currentConversationId && !isCreating) {
      createConversation.mutate({
        initial_message: 'Hello! I need help learning.',
      });
    }
  }, [currentConversationId, isCreating]);

  // Check if escalation is available
  useEffect(() => {
    if (conversation?.messages) {
      const lastAssistantMessage = [...conversation.messages]
        .reverse()
        .find((msg) => msg.role === 'assistant');

      // In production, check if escalation_available is true from response
      setShowEscalation(false);
    }
  }, [conversation]);

  if (conversationLoading || isCreating) {
    return (
      <div className="flex items-center justify-center h-screen">
        <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
        <span className="ml-3 text-lg">Initializing AI Tutor...</span>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6 max-w-7xl">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold mb-2">AI Tutor - Socratic Learning Guide</h1>
        <p className="text-muted-foreground">
          I'll guide you through questions, not give you answers! 🤔
        </p>
      </div>

      {/* Guardrail Notice */}
      {conversation?.recent_guardrails && conversation.recent_guardrails.length > 0 && (
        <Alert className="mb-6 border-blue-500 bg-blue-50">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>
            <strong>Note:</strong> The AI tutor uses guardrails to ensure you learn through
            guidance, not direct answers. If you see redirected responses, that's by design!
          </AlertDescription>
        </Alert>
      )}

      {/* Escalation Alert */}
      {showEscalation && (
        <Alert className="mb-6 border-orange-500 bg-orange-50">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>
            It seems you might benefit from instructor support. Would you like to escalate this
            conversation?
            <Button
              size="sm"
              variant="outline"
              className="ml-3"
              onClick={() => {
                const reason = prompt('Please describe why you need instructor help:');
                if (reason && currentConversationId) {
                  escalateToInstructor.mutate({
                    conversation_id: currentConversationId,
                    reason,
                  });
                }
              }}
            >
              Escalate to Instructor
            </Button>
          </AlertDescription>
        </Alert>
      )}

      {/* Main Content Tabs */}
      <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v as any)} className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="chat">
            <MessageSquare className="w-4 h-4 mr-2" />
            Chat
          </TabsTrigger>
          <TabsTrigger value="debug">
            <Bug className="w-4 h-4 mr-2" />
            Debug Help
          </TabsTrigger>
          <TabsTrigger value="review">
            <FileCode className="w-4 h-4 mr-2" />
            Code Review
          </TabsTrigger>
        </TabsList>

        {/* Chat Tab */}
        <TabsContent value="chat" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Socratic Conversation</CardTitle>
              <CardDescription>
                Ask questions and I'll guide you through guiding questions
              </CardDescription>
            </CardHeader>
            <CardContent>
              {currentConversationId && conversation ? (
                <TutorChatInterface
                  conversation={conversation}
                  onSendMessage={(content, code, level) => {
                    sendMessage.mutate({
                      conversation_id: currentConversationId,
                      content,
                      code_snippet: code,
                      understanding_level: level,
                    });
                  }}
                  isSending={isSending}
                />
              ) : (
                <div className="text-center text-muted-foreground py-8">
                  Starting conversation...
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Debugging Tab */}
        <TabsContent value="debug" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Systematic Debugging Guidance</CardTitle>
              <CardDescription>
                I'll guide you through debugging with a systematic approach (FR-030)
              </CardDescription>
            </CardHeader>
            <CardContent>
              {currentConversationId ? (
                <DebuggingHelper
                  conversationId={currentConversationId}
                  onRequestHelp={requestDebuggingHelp.mutate}
                  isLoading={requestDebuggingHelp.isPending}
                  guidance={requestDebuggingHelp.data}
                />
              ) : (
                <div className="text-center text-muted-foreground py-8">
                  Loading...
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Code Review Tab */}
        <TabsContent value="review" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Code Review Without Solutions</CardTitle>
              <CardDescription>
                I'll highlight issues and provide hints, but you'll fix it yourself! (FR-031)
              </CardDescription>
            </CardHeader>
            <CardContent>
              {currentConversationId ? (
                <CodeReviewPanel
                  conversationId={currentConversationId}
                  onRequestReview={requestCodeReview.mutate}
                  isLoading={requestCodeReview.isPending}
                  review={requestCodeReview.data}
                />
              ) : (
                <div className="text-center text-muted-foreground py-8">
                  Loading...
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Teaching Philosophy Info */}
      <Card className="mt-6 border-dashed">
        <CardHeader>
          <CardTitle className="text-sm font-medium">Teaching Philosophy</CardTitle>
        </CardHeader>
        <CardContent className="text-sm text-muted-foreground space-y-2">
          <p>
            <strong>Why questions instead of answers?</strong> Research shows that learning through
            guided discovery (Socratic method) leads to deeper understanding and better retention.
          </p>
          <p>
            <strong>What if I'm stuck?</strong> That's part of learning! Work through the guiding
            questions, and if you're still stuck after multiple attempts, I can escalate to an
            instructor.
          </p>
          <p>
            <strong>How does this help me?</strong> By figuring things out yourself (with guidance),
            you develop problem-solving skills that work beyond this specific problem.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
