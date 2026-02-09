/**
 * Tutor Chat Interface Component
 * Socratic conversation UI (FR-027, FR-028)
 */

'use client';

import { useState, useRef, useEffect } from 'react';
import { TutorConversation } from '@/hooks/useAITutor';
import { Button } from '../ui/button';
import { Textarea } from '../ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Label } from '../ui/label';
import { MessageBubble } from './MessageBubble';
import { GuardrailMessage } from './GuardrailMessage';
import { Send, Loader2, Code } from 'lucide-react';

interface TutorChatInterfaceProps {
  conversation: TutorConversation;
  onSendMessage: (content: string, code?: string, understandingLevel?: number) => void;
  isSending: boolean;
}

export function TutorChatInterface({
  conversation,
  onSendMessage,
  isSending,
}: TutorChatInterfaceProps) {
  const [message, setMessage] = useState('');
  const [codeSnippet, setCodeSnippet] = useState('');
  const [showCodeInput, setShowCodeInput] = useState(false);
  const [understandingLevel, setUnderstandingLevel] = useState<number | undefined>(undefined);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [conversation.messages]);

  const handleSubmit = () => {
    if (!message.trim() && !codeSnippet.trim()) return;

    onSendMessage(
      message,
      codeSnippet || undefined,
      understandingLevel
    );

    // Clear inputs
    setMessage('');
    setCodeSnippet('');
    setShowCodeInput(false);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="flex flex-col h-[600px]">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50 rounded-t-lg">
        {conversation.messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center text-muted-foreground">
            <p className="text-lg mb-2">Ask me anything! 🤔</p>
            <p className="text-sm">
              Remember: I'll guide you with questions, not give direct answers.
            </p>
          </div>
        ) : (
          <>
            {conversation.messages.map((msg) => (
              <div key={msg.id}>
                <MessageBubble message={msg} />

                {/* Show guardrail message if this message triggered one */}
                {msg.role === 'assistant' && (
                  conversation.recent_guardrails.find(
                    (g) => Math.abs(new Date(g.created_at).getTime() - new Date(msg.created_at).getTime()) < 1000
                  ) && (
                    <GuardrailMessage
                      type={conversation.recent_guardrails[0].guardrail_type}
                      reason={conversation.recent_guardrails[0].trigger_reason}
                    />
                  )
                )}
              </div>
            ))}

            {isSending && (
              <div className="flex items-center space-x-2 text-muted-foreground">
                <Loader2 className="w-4 h-4 animate-spin" />
                <span className="text-sm">Tutor is thinking...</span>
              </div>
            )}
          </>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t bg-white p-4 rounded-b-lg space-y-3">
        {/* Understanding Level Selector */}
        <div className="flex items-center space-x-4">
          <Label htmlFor="understanding" className="text-sm whitespace-nowrap">
            How well do you understand this? (Optional)
          </Label>
          <Select
            value={understandingLevel?.toString()}
            onValueChange={(v) => setUnderstandingLevel(v ? parseInt(v) : undefined)}
          >
            <SelectTrigger id="understanding" className="w-[200px]">
              <SelectValue placeholder="Select level" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="1">1 - Very confused</SelectItem>
              <SelectItem value="2">2 - Somewhat confused</SelectItem>
              <SelectItem value="3">3 - Neutral</SelectItem>
              <SelectItem value="4">4 - Mostly understand</SelectItem>
              <SelectItem value="5">5 - Fully understand</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Code Input Toggle */}
        <div className="flex items-center space-x-2">
          <Button
            type="button"
            variant={showCodeInput ? 'default' : 'outline'}
            size="sm"
            onClick={() => setShowCodeInput(!showCodeInput)}
          >
            <Code className="w-4 h-4 mr-2" />
            {showCodeInput ? 'Hide Code' : 'Include Code'}
          </Button>
        </div>

        {/* Code Input */}
        {showCodeInput && (
          <div>
            <Label htmlFor="code" className="text-sm mb-2 block">
              Code Snippet (Optional)
            </Label>
            <Textarea
              id="code"
              value={codeSnippet}
              onChange={(e) => setCodeSnippet(e.target.value)}
              placeholder="Paste your code here..."
              className="font-mono text-sm min-h-[100px]"
            />
          </div>
        )}

        {/* Message Input */}
        <div className="flex space-x-2">
          <Textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask a question, describe your problem, or share your thinking..."
            className="flex-1 min-h-[80px] resize-none"
            disabled={isSending}
          />
          <Button
            onClick={handleSubmit}
            disabled={isSending || (!message.trim() && !codeSnippet.trim())}
            className="self-end"
          >
            {isSending ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <>
                <Send className="w-4 h-4 mr-2" />
                Send
              </>
            )}
          </Button>
        </div>

        {/* Hint */}
        <p className="text-xs text-muted-foreground">
          💡 Tip: The more you share about your thinking process, the better I can guide you!
          Press Enter to send, Shift+Enter for new line.
        </p>
      </div>
    </div>
  );
}
