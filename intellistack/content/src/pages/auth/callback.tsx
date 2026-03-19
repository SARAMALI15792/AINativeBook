import React, { useEffect, useState } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import Layout from '@theme/Layout';
import { authClient } from '../../lib/auth';

function CallbackPageContent() {
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('Processing authentication...');

  useEffect(() => {
    const handleCallback = async () => {
      // Get base URL from Docusaurus config
      const baseUrl = (window as any).docusaurus?.siteConfig?.baseUrl || '/AINativeBook/';

      try {
        // Get the current URL parameters
        const params = new URLSearchParams(window.location.search);
        const error = params.get('error');

        if (error) {
          setStatus('error');
          setMessage(`Authentication failed: ${error}`);
          setTimeout(() => {
            window.location.href = `${baseUrl}auth/login?error=oauth_failed`;
          }, 3000);
          return;
        }

        // Wait a moment for the session cookie to be set by the auth server
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Check session
        const session = await authClient.getSession();

        if (!session.data) {
          setStatus('error');
          setMessage('Failed to establish session. Redirecting to login...');
          setTimeout(() => {
            window.location.href = `${baseUrl}auth/login`;
          }, 2000);
          return;
        }

        setStatus('success');
        setMessage('Authentication successful! Redirecting...');

        // Dispatch auth state change event
        window.dispatchEvent(new Event('auth-state-changed'));

        // Check if user needs onboarding
        if (!session.data.onboarding_completed) {
          setTimeout(() => {
            window.location.href = `${baseUrl}onboarding/step-1`;
          }, 1000);
        } else {
          setTimeout(() => {
            window.location.href = `${baseUrl}stage-1/intro`;
          }, 1000);
        }
      } catch (err) {
        console.error('OAuth callback error:', err);
        setStatus('error');
        setMessage('An unexpected error occurred. Redirecting to login...');
        setTimeout(() => {
          window.location.href = `${baseUrl}auth/login`;
        }, 3000);
      }
    };

    handleCallback();
  }, []);

  return (
    <Layout title="Authentication" description="Processing authentication">
      <div style={{
        maxWidth: '500px',
        margin: '6rem auto',
        padding: '3rem',
        textAlign: 'center',
        backgroundColor: 'var(--ifm-background-surface-color)',
        borderRadius: '8px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
      }}>
        {status === 'loading' && (
          <>
            <div style={{
              width: '60px',
              height: '60px',
              margin: '0 auto 2rem',
              border: '4px solid var(--ifm-color-emphasis-300)',
              borderTop: '4px solid var(--ifm-color-primary)',
              borderRadius: '50%',
              animation: 'spin 1s linear infinite'
            }} />
            <style>{`
              @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
              }
            `}</style>
          </>
        )}

        {status === 'success' && (
          <div style={{
            width: '60px',
            height: '60px',
            margin: '0 auto 2rem',
            borderRadius: '50%',
            backgroundColor: '#4caf50',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="3">
              <polyline points="20 6 9 17 4 12" />
            </svg>
          </div>
        )}

        {status === 'error' && (
          <div style={{
            width: '60px',
            height: '60px',
            margin: '0 auto 2rem',
            borderRadius: '50%',
            backgroundColor: '#f44336',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="3">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </div>
        )}

        <h2 style={{ marginBottom: '1rem' }}>
          {status === 'loading' && 'Authenticating...'}
          {status === 'success' && 'Success!'}
          {status === 'error' && 'Error'}
        </h2>

        <p style={{ color: 'var(--ifm-color-emphasis-600)' }}>
          {message}
        </p>
      </div>
    </Layout>
  );
}

export default function CallbackPage() {
  return (
    <BrowserOnly fallback={<div>Loading...</div>}>
      {() => <CallbackPageContent />}
    </BrowserOnly>
  );
}
