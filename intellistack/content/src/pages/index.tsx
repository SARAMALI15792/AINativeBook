import React, { useEffect } from 'react';
import { useHistory } from '@docusaurus/router';

/**
 * Landing page redirect
 * Immediately redirects to the first stage of the learning path
 */
export default function Home(): JSX.Element {
  const history = useHistory();

  useEffect(() => {
    // Redirect to Stage 1 intro
    history.replace('/docs/stage-1/intro');
  }, [history]);

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
          border: '4px solid rgba(0, 239, 255, 0.3)',
          borderTopColor: '#00efff',
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
