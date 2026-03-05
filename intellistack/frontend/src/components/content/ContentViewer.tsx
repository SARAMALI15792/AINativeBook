'use client';

import { useEffect, useRef, useState } from 'react';

interface ContentViewerProps {
  contentId: string;
  docusaurusUrl: string;
  title: string;
  estimatedMinutes: number;
  isCompleted: boolean;
  onComplete: () => void;
  onNavigateNext?: () => void;
  onNavigatePrev?: () => void;
}

interface PostMessageEvent {
  type: string;
  contentId?: string;
  percentage?: number;
  timeSpent?: number;
}

export default function ContentViewer({
  contentId,
  docusaurusUrl,
  title,
  estimatedMinutes,
  isCompleted,
  onComplete,
  onNavigateNext,
  onNavigatePrev,
}: ContentViewerProps) {
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [scrollProgress, setScrollProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Listen for PostMessage events from Docusaurus iframe
    const handleMessage = (event: MessageEvent<PostMessageEvent>) => {
      // Validate origin
      const docusaurusOrigin = new URL(docusaurusUrl).origin;
      if (event.origin !== docusaurusOrigin) {
        return;
      }

      const { type, percentage } = event.data;

      switch (type) {
        case 'content_loaded':
          setIsLoading(false);
          break;
        case 'scroll_progress':
          if (percentage !== undefined) {
            setScrollProgress(percentage);
            // Auto-complete at 90% scroll
            if (percentage >= 90 && !isCompleted) {
              onComplete();
            }
          }
          break;
        case 'content_completed':
          onComplete();
          break;
      }
    };

    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, [docusaurusUrl, isCompleted, onComplete]);

  const handleIframeLoad = () => {
    setIsLoading(false);
    setError(null);
  };

  const handleIframeError = () => {
    setIsLoading(false);
    setError('Failed to load content. Please try again.');
  };

  const handleMarkComplete = () => {
    if (!isCompleted) {
      onComplete();
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
            <p className="text-sm text-gray-500 mt-1">
              Estimated time: {estimatedMinutes} minutes
            </p>
          </div>
          <div className="flex items-center gap-4">
            {!isCompleted && (
              <button
                onClick={handleMarkComplete}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                Mark Complete
              </button>
            )}
            {isCompleted && (
              <div className="flex items-center gap-2 text-green-600">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clipRule="evenodd"
                  />
                </svg>
                <span className="font-medium">Completed</span>
              </div>
            )}
          </div>
        </div>

        {/* Progress bar */}
        {!isCompleted && scrollProgress > 0 && (
          <div className="mt-3">
            <div className="flex items-center justify-between text-xs text-gray-600 mb-1">
              <span>Reading progress</span>
              <span>{Math.round(scrollProgress)}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${scrollProgress}%` }}
              />
            </div>
          </div>
        )}
      </div>

      {/* Navigation */}
      <div className="bg-gray-50 border-b border-gray-200 px-6 py-2 flex items-center justify-between">
        <button
          onClick={onNavigatePrev}
          disabled={!onNavigatePrev}
          className="flex items-center gap-2 px-3 py-1.5 text-sm text-gray-700 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Previous
        </button>
        <button
          onClick={onNavigateNext}
          disabled={!onNavigateNext}
          className="flex items-center gap-2 px-3 py-1.5 text-sm text-gray-700 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Next
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      {/* Content iframe */}
      <div className="flex-1 relative bg-white">
        {isLoading && (
          <div className="absolute inset-0 flex items-center justify-center bg-gray-50">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4" />
              <p className="text-gray-600">Loading content...</p>
            </div>
          </div>
        )}

        {error && (
          <div className="absolute inset-0 flex items-center justify-center bg-gray-50">
            <div className="text-center max-w-md">
              <div className="text-red-600 mb-4">
                <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Failed to Load Content</h3>
              <p className="text-gray-600 mb-4">{error}</p>
              <a
                href={docusaurusUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                Open in New Tab
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                  />
                </svg>
              </a>
            </div>
          </div>
        )}

        <iframe
          ref={iframeRef}
          src={`${docusaurusUrl}?embedded=true`}
          className="w-full h-full border-0"
          title={title}
          onLoad={handleIframeLoad}
          onError={handleIframeError}
          sandbox="allow-same-origin allow-scripts allow-popups allow-forms"
        />
      </div>
    </div>
  );
}
