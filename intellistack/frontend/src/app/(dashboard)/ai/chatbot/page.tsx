/**
 * RAG Chatbot Page
 *
 * Main page for AI-powered RAG chatbot with streaming responses (FR-066 to FR-080).
 */

'use client';

import { MessageSquare, Sparkles, BookOpen, Info } from 'lucide-react';
import { ChatInterface } from '@/components/ai/ChatInterface';
import { TextSelectionQuery } from '@/components/ai/TextSelectionQuery';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';

export default function ChatbotPage() {
  const handleTextSelectionQuery = (query: string, selectedText: string) => {
    // TODO: Integrate with chat interface
    console.log('Text selection query:', { query, selectedText });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
          <Sparkles className="h-8 w-8 text-primary" />
          AI Chatbot
        </h1>
        <p className="text-muted-foreground mt-2">
          Ask questions about your course content and get instant answers with citations
        </p>
      </div>

      {/* Info Alert */}
      <Alert>
        <Info className="h-4 w-4" />
        <AlertTitle>How to use the AI Chatbot</AlertTitle>
        <AlertDescription className="space-y-2">
          <ul className="list-disc list-inside space-y-1 text-sm">
            <li>Ask questions about course materials you have access to</li>
            <li>Highlight text in lessons and ask specific questions about it</li>
            <li>View source citations to verify information</li>
            <li>Confidence scores help you assess answer reliability</li>
          </ul>
        </AlertDescription>
      </Alert>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Chat Interface */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <MessageSquare className="h-5 w-5" />
                Chat
              </CardTitle>
              <CardDescription>
                Ask questions and get AI-powered answers from your course content
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ChatInterface />
            </CardContent>
          </Card>
        </div>

        {/* Sidebar with tips and features */}
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Features</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex gap-3">
                <BookOpen className="h-5 w-5 text-primary flex-shrink-0 mt-0.5" />
                <div>
                  <h4 className="font-semibold text-sm">Source Citations</h4>
                  <p className="text-xs text-muted-foreground">
                    Every answer includes links to source materials
                  </p>
                </div>
              </div>

              <div className="flex gap-3">
                <Sparkles className="h-5 w-5 text-primary flex-shrink-0 mt-0.5" />
                <div>
                  <h4 className="font-semibold text-sm">Real-time Streaming</h4>
                  <p className="text-xs text-muted-foreground">
                    Watch answers appear as they're generated
                  </p>
                </div>
              </div>

              <div className="flex gap-3">
                <MessageSquare className="h-5 w-5 text-primary flex-shrink-0 mt-0.5" />
                <div>
                  <h4 className="font-semibold text-sm">Context Aware</h4>
                  <p className="text-xs text-muted-foreground">
                    Remembers conversation history for follow-up questions
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Tips</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="flex items-start gap-2">
                  <span className="text-primary font-bold">•</span>
                  <span>Be specific in your questions for better answers</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary font-bold">•</span>
                  <span>Check confidence scores to verify answer reliability</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary font-bold">•</span>
                  <span>Click citations to view original source material</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary font-bold">•</span>
                  <span>Use text selection to ask about specific passages</span>
                </li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Text Selection Query Feature */}
      <TextSelectionQuery onQuery={handleTextSelectionQuery} />
    </div>
  );
}
