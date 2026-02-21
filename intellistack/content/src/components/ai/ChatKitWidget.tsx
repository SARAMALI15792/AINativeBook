/**
 * ChatKit Widget Component
 * Floating AI tutor chat for Docusaurus pages
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import { useLocation } from '@docusaurus/router';
import { ChatKitErrorBoundary } from './ChatKitErrorBoundary';
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

  // Only render on Docusaurus learning routes
  // The paths are like /AINativeBook/docs/stage-1/intro/, so check if they contain the stage paths
  const isStageRoute = location.pathname.includes('/stage-1/') ||
                       location.pathname.includes('/stage-2/') ||
                       location.pathname.includes('/stage-3/') ||
                       location.pathname.includes('/stage-4/') ||
                       location.pathname.includes('/stage-5/');

  if (!isStageRoute) {
    return null;
  }

  console.log('ChatKitWidget: Component rendering'); // Debug log

  // State
  const [isOpen, setIsOpen] = useState(false);
  const [session, setSession] = useState<any>(null);
  const [userStage, setUserStage] = useState<number>(1); // Store user's actual stage
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
  console.log('ChatKitWidget: Backend URL:', backendUrl); // Debug log

  // Cached JWT token for backend API calls
  const jwtTokenRef = useRef<string | null>(null);

  // Initialize auth and fetch user stage
  useEffect(() => {
    console.log('ChatKitWidget: Initializing auth...');

    const checkAuth = async () => {
      try {
        const mod = await import('../../lib/auth-client');
        console.log('ChatKitWidget: Auth client imported');

        const result = await mod.authClient.getSession();
        console.log('ChatKitWidget: Session result:', result);

        if (result.data?.user) {
          console.log('ChatKitWidget: User authenticated, setting session');
          setSession(result.data);

          // Get JWT token for backend API calls
          const jwt = await mod.getJwtToken();
          if (jwt) {
            jwtTokenRef.current = jwt;
            console.log('ChatKitWidget: JWT token obtained');

            // Fetch user's current stage using JWT
            try {
              const response = await fetch(`${backendUrl}/api/v1/users/stage`, {
                headers: {
                  'Authorization': `Bearer ${jwt}`,
                  'Content-Type': 'application/json',
                },
              });

              if (response.ok) {
                const data = await response.json();
                setUserStage(data.stage);
                console.log('ChatKitWidget: User stage fetched:', data.stage);
              } else {
                console.error('ChatKitWidget: Failed to fetch user stage:', response.status);
              }
            } catch (err) {
              console.error('ChatKitWidget: Failed to fetch user stage:', err);
              setUserStage(1);
            }
          } else {
            console.warn('ChatKitWidget: Could not obtain JWT token');
          }
        } else {
          console.log('ChatKitWidget: User not authenticated');
          setSession(null);
        }
      } catch (err) {
        console.error('ChatKitWidget: Error getting session:', err);
        setSession(null);
      }
    };

    checkAuth();

    // Listen for auth state changes (triggered by login/logout)
    const handleAuthChange = () => {
      console.log('ChatKitWidget: Auth state changed, refreshing session');
      checkAuth();
    };

    window.addEventListener('auth-state-changed', handleAuthChange);

    // Also poll every 3 seconds as fallback
    const interval = setInterval(checkAuth, 3000);

    return () => {
      window.removeEventListener('auth-state-changed', handleAuthChange);
      clearInterval(interval);
    };
  }, [backendUrl]);

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
    // Refresh JWT if needed (tokens expire)
    if (!jwtTokenRef.current) {
      try {
        const mod = await import('../../lib/auth-client');
        const jwt = await mod.getJwtToken();
        if (jwt) jwtTokenRef.current = jwt;
      } catch {
        // Ignore — will use whatever we have
      }
    }

    // Encode values that may contain non-ASCII characters.
    // HTTP headers only allow ISO-8859-1; use encodeURIComponent for safety.
    return {
      'Authorization': `Bearer ${jwtTokenRef.current || ''}`,
      'Content-Type': 'application/json',
      'X-Page-Url': encodeURIComponent(pageContext.url),
      'X-Page-Title': encodeURIComponent(pageContext.title),
      'X-Page-Headings': encodeURIComponent(JSON.stringify(pageContext.headings)),
      'X-Selected-Text': encodeURIComponent(selectedText || ''),
      'X-User-Stage': userStage.toString(),
    };
  }, [pageContext, selectedText, userStage]);

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

    let assistantContent = '';
    let completed = false;

    console.log('Sending message to:', `${backendUrl}/api/v1/chatkit/stream`);

    try {
      const headers = await getAuthHeaders();
      console.log('Request headers:', headers);

      const response = await fetch(`${backendUrl}/api/v1/chatkit/stream`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          thread_id: currentThreadId,
          content: userMessage,
        }),
      });

      console.log('Response status:', response.status, response.statusText);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Response error:', errorText);
        throw new Error(`HTTP ${response.status}: ${errorText}`);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });

          // SSE events separated by double newlines
          const parts = buffer.split('\n\n');
          buffer = parts.pop() || '';

          for (const part of parts) {
            if (!part.trim()) continue;

            // Extract data line from the SSE event block
            let eventData: string | null = null;
            let eventType: string | null = null;

            for (const line of part.split('\n')) {
              if (line.startsWith('event: ')) {
                eventType = line.slice(7);
              }
              if (line.startsWith('data: ')) {
                eventData = line.slice(6);
              }
            }

            if (!eventData) continue;

            let data: any;
            try {
              data = JSON.parse(eventData);
            } catch {
              console.warn('Failed to parse SSE data:', eventData);
              continue;
            }

            console.log('SSE event received:', eventType, data);

            if (data.code === 'RATE_LIMITED') {
              setError(data.message);
              return;
            }

            if (data.id && !currentThreadId) {
              setCurrentThreadId(data.id);
            }

            // Accumulate streaming text
            if (data.text) {
              console.log('Streaming chunk:', data.text);
              assistantContent += data.text;
              setStreamingContent(assistantContent);
            }

            if (data.rate_limit) {
              setRateLimit(data.rate_limit);
            }

            // Stream complete — add final message
            if (data.message_id) {
              console.log('Stream complete, message_id:', data.message_id);
              completed = true;
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
          }
        }
      }

      // If stream ended without a message_id but we have content, add it
      if (!completed && assistantContent) {
        setMessages(prev => [
          ...prev,
          {
            id: `assistant-${Date.now()}`,
            role: 'assistant',
            content: assistantContent,
            created_at: new Date().toISOString(),
          },
        ]);
        setStreamingContent('');
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

    // Always render the button to ensure it shows regardless of session status
    const renderButton = () => (
      <button
        className={session?.user ? styles.fab : `${styles.fab} ${styles.fabUnauthenticated}`}
        onClick={() => setIsOpen(!isOpen)}
        aria-label={isOpen ? 'Close AI Tutor' : 'Open AI Tutor'}
        style={{ display: 'flex' }} // Ensuring the button is visible
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
    );

    return (
      <ChatKitErrorBoundary>
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

          {/* Floating Button - Always rendered regardless of session status */}
          {renderButton()}

          {/* Panel - Conditionally rendered based on open state and session */}
          {isOpen && (
            session?.user ? (
              /* Authenticated User Panel */
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

                  {/* Streaming response bubble */}
                  {streamingContent && (
                    <div className={`${styles.message} ${styles.assistant}`}>
                      <div className={styles.messageContent}>
                        {streamingContent}
                        <span className={styles.cursor}>|</span>
                      </div>
                    </div>
                  )}

                  {/* Thinking indicator while waiting for first chunk */}
                  {isLoading && !streamingContent && (
                    <div className={`${styles.message} ${styles.assistant}`}>
                      <div className={styles.messageContent}>
                        <span className={styles.thinking}>
                          <span className={styles.dot} />
                          <span className={styles.dot} />
                          <span className={styles.dot} />
                        </span>
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
            ) : (
              /* Unauthenticated User Panel */
              <div className={styles.panel}>
                <div className={styles.header}>
                  <h3 className={styles.headerTitle}>AI Tutor</h3>
                  <button
                    className={styles.headerButton}
                    onClick={() => setIsOpen(false)}
                    title="Close"
                  >
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <line x1="18" y1="6" x2="6" y2="18"/>
                      <line x1="6" y1="6" x2="18" y2="18"/>
                    </svg>
                  </button>
                </div>
                <div className={styles.loginPrompt}>
                  <div className={styles.welcomeIcon}>
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                      <circle cx="12" cy="12" r="10"/>
                      <path d="M12 16v-4"/>
                      <path d="M12 8h.01"/>
                    </svg>
                  </div>
                  <h4>Unlock AI Learning Support</h4>
                  <p>Sign up or log in to access personalized AI tutoring, interactive exercises, and progress tracking.</p>
                  <button
                    className={styles.loginButton}
                    onClick={async () => {
                      try {
                        const authMod = await import('../../lib/auth-client');
                        // Use the exported signIn method which is a wrapper around authClient.signIn
                        await authMod.signIn('credentials'); // This will trigger the sign-in flow

                        // After sign-in, dispatch event to refresh widget state
                        window.dispatchEvent(new Event('auth-state-changed'));
                      } catch (err) {
                        console.error('Auth client import failed:', err);
                        // Fallback: redirect to login page
                        window.location.href = '/login';
                      }
                    }}
                  >
                    Sign In to Continue Learning
                  </button>
                </div>
              </div>
            )
          )}
        </>
      </ChatKitErrorBoundary>
    );
}
