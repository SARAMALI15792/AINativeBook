/**
 * ChatKit Widget Component
 * Floating AI tutor chat for Docusaurus pages
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import { useLocation } from '@docusaurus/router';
import styles from './ChatKitWidget.module.css';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
}

interface Thread {
  id: string;
  title: string;
  updated_at: string;
}

interface RateLimitInfo {
  remaining: number;
  limit: number;
  reset_at: string | null;
}

// Extract page context from current Docusaurus page
function usePageContext() {
  const location = useLocation();

  return {
    url: location.pathname,
    title: typeof document !== 'undefined' ? document.title : '',
    headings: typeof document !== 'undefined'
      ? Array.from(document.querySelectorAll('article h1, article h2, article h3')).map(h => h.textContent || '')
      : [],
  };
}

export default function ChatKitWidget(): JSX.Element | null {
  const { siteConfig } = useDocusaurusContext();
  const pageContext = usePageContext();
  const location = useLocation();

  // State
  const [isOpen, setIsOpen] = useState(false);
  const [session, setSession] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [currentThreadId, setCurrentThreadId] = useState<string | null>(null);
  const [threads, setThreads] = useState<Thread[]>([]);
  const [showThreads, setShowThreads] = useState(false);
  const [rateLimit, setRateLimit] = useState<RateLimitInfo | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [streamingContent, setStreamingContent] = useState('');
  const [selectedText, setSelectedText] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const backendUrl = (siteConfig.customFields?.backendUrl as string) || 'http://localhost:8000';

  // Initialize auth
  useEffect(() => {
    import('@site/src/lib/auth-client').then((mod) => {
      mod.authClient.getSession().then((result) => {
        if (result.data?.user) {
          setSession(result.data);
        }
      });
    });
  }, []);

  // Listen for text selection
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      if (selection && selection.toString().trim().length > 10) {
        setSelectedText(selection.toString().trim());
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => document.removeEventListener('mouseup', handleSelection);
  }, []);

  // Scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, streamingContent]);

  // Load threads when panel opens
  useEffect(() => {
    if (isOpen && session?.user) {
      loadThreads();
      loadUsageStats();
    }
  }, [isOpen, session]);

  // Reset thread on page change
  useEffect(() => {
    setCurrentThreadId(null);
    setMessages([]);
  }, [location.pathname]);

  const getAuthHeaders = useCallback(async () => {
    const token = session?.session?.token;
    return {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
      'X-Page-Url': pageContext.url,
      'X-Page-Title': pageContext.title,
      'X-Page-Headings': JSON.stringify(pageContext.headings),
      'X-Selected-Text': selectedText || '',
      'X-User-Stage': '1', // TODO: Get from user profile
    };
  }, [session, pageContext, selectedText]);

  const loadThreads = async () => {
    try {
      const headers = await getAuthHeaders();
      const response = await fetch(`${backendUrl}/api/v1/chatkit/threads?limit=10`, {
        headers,
      });
      if (response.ok) {
        const data = await response.json();
        setThreads(data.threads || []);
      }
    } catch (err) {
      console.error('Failed to load threads:', err);
    }
  };

  const loadUsageStats = async () => {
    try {
      const headers = await getAuthHeaders();
      const response = await fetch(`${backendUrl}/api/v1/chatkit/usage`, {
        headers,
      });
      if (response.ok) {
        const data = await response.json();
        setRateLimit(data.usage);
      }
    } catch (err) {
      console.error('Failed to load usage stats:', err);
    }
  };

  const loadThread = async (threadId: string) => {
    try {
      const headers = await getAuthHeaders();
      const response = await fetch(`${backendUrl}/api/v1/chatkit/threads/${threadId}`, {
        headers,
      });
      if (response.ok) {
        const data = await response.json();
        setMessages(data.messages || []);
        setCurrentThreadId(threadId);
        setShowThreads(false);
      }
    } catch (err) {
      console.error('Failed to load thread:', err);
    }
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = inputValue.trim();
    setInputValue('');
    setError(null);
    setIsLoading(true);
    setStreamingContent('');

    // Add user message immediately
    const tempUserMsg: Message = {
      id: `temp-${Date.now()}`,
      role: 'user',
      content: userMessage,
      created_at: new Date().toISOString(),
    };
    setMessages(prev => [...prev, tempUserMsg]);

    try {
      const headers = await getAuthHeaders();
      const response = await fetch(`${backendUrl}/api/v1/chatkit/stream`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          thread_id: currentThreadId,
          content: userMessage,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let assistantContent = '';

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value);
          const lines = chunk.split('\n');

          for (const line of lines) {
            if (line.startsWith('event: ')) {
              const eventType = line.slice(7);
              continue;
            }
            if (line.startsWith('data: ')) {
              try {
                const data = JSON.parse(line.slice(6));

                if (data.code === 'RATE_LIMITED') {
                  setError(data.message);
                  setIsLoading(false);
                  return;
                }

                if (data.id && !currentThreadId) {
                  setCurrentThreadId(data.id);
                }

                if (data.text) {
                  assistantContent += data.text;
                  setStreamingContent(assistantContent);
                }

                if (data.rate_limit) {
                  setRateLimit(data.rate_limit);
                }

                if (data.message_id) {
                  // Response complete
                  setMessages(prev => [
                    ...prev,
                    {
                      id: data.message_id,
                      role: 'assistant',
                      content: assistantContent,
                      created_at: new Date().toISOString(),
                    },
                  ]);
                  setStreamingContent('');
                }
              } catch {
                // Ignore parse errors
              }
            }
          }
        }
      }
    } catch (err: any) {
      setError(err.message || 'Failed to send message');
    } finally {
      setIsLoading(false);
      setSelectedText(null);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const startNewThread = () => {
    setCurrentThreadId(null);
    setMessages([]);
    setShowThreads(false);
    inputRef.current?.focus();
  };

  const askAboutSelection = () => {
    if (selectedText) {
      setInputValue(`Can you explain this: "${selectedText.slice(0, 200)}${selectedText.length > 200 ? '...' : ''}"`);
      setIsOpen(true);
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  };

  // Don't render if not authenticated
  if (!session?.user) {
    return null;
  }

  return (
    <>
      {/* Text Selection Popup */}
      {selectedText && !isOpen && (
        <button
          className={styles.selectionPopup}
          onClick={askAboutSelection}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
          </svg>
          Ask AI
        </button>
      )}

      {/* Floating Button */}
      <button
        className={styles.fab}
        onClick={() => setIsOpen(!isOpen)}
        aria-label={isOpen ? 'Close AI Tutor' : 'Open AI Tutor'}
      >
        {isOpen ? (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="18" y1="6" x2="6" y2="18"/>
            <line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        ) : (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
          </svg>
        )}
      </button>

      {/* Chat Panel */}
      {isOpen && (
        <div className={styles.panel}>
          {/* Header */}
          <div className={styles.header}>
            <div className={styles.headerLeft}>
              <button
                className={styles.headerButton}
                onClick={() => setShowThreads(!showThreads)}
                title="Conversation history"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="3" y1="6" x2="21" y2="6"/>
                  <line x1="3" y1="12" x2="21" y2="12"/>
                  <line x1="3" y1="18" x2="21" y2="18"/>
                </svg>
              </button>
              <h3 className={styles.headerTitle}>AI Tutor</h3>
            </div>
            <div className={styles.headerRight}>
              <button
                className={styles.headerButton}
                onClick={startNewThread}
                title="New conversation"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="12" y1="5" x2="12" y2="19"/>
                  <line x1="5" y1="12" x2="19" y2="12"/>
                </svg>
              </button>
            </div>
          </div>

          {/* Rate Limit Banner */}
          {rateLimit && rateLimit.remaining <= 5 && (
            <div className={styles.rateLimitBanner}>
              {rateLimit.remaining === 0 ? (
                `Daily limit reached. Resets ${rateLimit.reset_at ? new Date(rateLimit.reset_at).toLocaleTimeString() : 'tomorrow'}`
              ) : (
                `${rateLimit.remaining}/${rateLimit.limit} messages remaining today`
              )}
            </div>
          )}

          {/* Thread List */}
          {showThreads && (
            <div className={styles.threadList}>
              <div className={styles.threadListHeader}>
                <span>Recent Conversations</span>
              </div>
              {threads.length === 0 ? (
                <div className={styles.emptyThreads}>No conversations yet</div>
              ) : (
                threads.map(thread => (
                  <button
                    key={thread.id}
                    className={`${styles.threadItem} ${thread.id === currentThreadId ? styles.active : ''}`}
                    onClick={() => loadThread(thread.id)}
                  >
                    <span className={styles.threadTitle}>{thread.title || 'Untitled'}</span>
                    <span className={styles.threadDate}>
                      {new Date(thread.updated_at).toLocaleDateString()}
                    </span>
                  </button>
                ))
              )}
            </div>
          )}

          {/* Messages */}
          <div className={styles.messages}>
            {messages.length === 0 && !streamingContent && (
              <div className={styles.welcome}>
                <div className={styles.welcomeIcon}>
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M12 16v-4"/>
                    <path d="M12 8h.01"/>
                  </svg>
                </div>
                <h4>How can I help you learn?</h4>
                <p>Ask questions about the current lesson, get help debugging code, or explore concepts.</p>
                <div className={styles.suggestions}>
                  <button onClick={() => setInputValue("Explain this concept in simpler terms")}>
                    Explain this concept
                  </button>
                  <button onClick={() => setInputValue("What should I learn next?")}>
                    What's next?
                  </button>
                </div>
              </div>
            )}

            {messages.map(msg => (
              <div
                key={msg.id}
                className={`${styles.message} ${styles[msg.role]}`}
              >
                <div className={styles.messageContent}>
                  {msg.content}
                </div>
              </div>
            ))}

            {streamingContent && (
              <div className={`${styles.message} ${styles.assistant}`}>
                <div className={styles.messageContent}>
                  {streamingContent}
                  <span className={styles.cursor}>|</span>
                </div>
              </div>
            )}

            {error && (
              <div className={styles.errorMessage}>
                {error}
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className={styles.inputArea}>
            <textarea
              ref={inputRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask a question..."
              className={styles.input}
              rows={1}
              disabled={isLoading || (rateLimit?.remaining === 0)}
            />
            <button
              onClick={sendMessage}
              className={styles.sendButton}
              disabled={!inputValue.trim() || isLoading || (rateLimit?.remaining === 0)}
            >
              {isLoading ? (
                <span className={styles.spinner} />
              ) : (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="22" y1="2" x2="11" y2="13"/>
                  <polygon points="22 2 15 22 11 13 2 9 22 2"/>
                </svg>
              )}
            </button>
          </div>
        </div>
      )}
    </>
  );
}
