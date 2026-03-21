import React, { useEffect } from 'react';

/**
 * Landing page redirect
 * Immediately redirects to the first stage of the learning path
 */
export default function Home(): JSX.Element {
  useEffect(() => {
    window.location.replace('/AINativeBook/stage-1/intro');
  }, []);

  // Show minimal loading state during redirect
  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '100vh',
      background: '#1a1a2e',
      color: '#ffffff',
    }}>
      <div style={{ textAlign: 'center' }}>
        <div style={{
          width: '48px',
          height: '48px',
          margin: '0 auto 16px',
          border: '4px solid rgba(37, 99, 235, 0.3)',
          borderTopColor: '#2563EB',
          borderRadius: '50%',
          animation: 'spin 1s linear infinite',
        }} />
        <p>Loading IntelliStack...</p>
      </div>
      <style>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}
