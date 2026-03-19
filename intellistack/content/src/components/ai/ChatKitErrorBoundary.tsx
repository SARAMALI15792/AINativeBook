import React from 'react';

interface Props {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ChatKitErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('ChatKit Widget Error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      // Render fallback UI if available, otherwise render nothing
      if (this.props.fallback) {
        return this.props.fallback;
      }

      // Default fallback - a simple button that can open an error message
      return (
        <button
          style={{
            position: 'fixed',
            bottom: '24px',
            right: '24px',
            width: '56px',
            height: '56px',
            borderRadius: '50%',
            backgroundColor: '#dc2626', // Red background for error
            color: '#ffffff',
            border: 'none',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 4px 16px rgba(0, 0, 0, 0.2)',
            zIndex: 9999,
            pointerEvents: 'auto',
          }}
          onClick={() => {
            alert('AI Tutor widget experienced an error. Please refresh the page.');
          }}
          aria-label="AI Tutor Error"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
        </button>
      );
    }

    return this.props.children;
  }
}