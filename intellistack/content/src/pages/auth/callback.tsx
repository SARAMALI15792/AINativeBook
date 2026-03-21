import React, { useEffect, useState } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import Layout from '@theme/Layout';
import { authClient } from '../../lib/auth';
import TriangleLoader from '../../components/ui/TriangleLoader';

function CallbackPageContent() {
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('Processing authentication...');

  useEffect(() => {
    const handleCallback = async () => {
      const baseUrl = (window as any).docusaurus?.siteConfig?.baseUrl || '/AINativeBook/';

      try {
        const params = new URLSearchParams(window.location.search);
        const error = params.get('error');

        if (error) {
          setStatus('error');
          setMessage(`Authentication failed: ${error}`);
          setTimeout(() => { window.location.href = `${baseUrl}auth/login?error=oauth_failed`; }, 3000);
          return;
        }

        await new Promise(resolve => setTimeout(resolve, 1000));
        const session = await authClient.getSession();

        if (!session.data) {
          setStatus('error');
          setMessage('Failed to establish session. Redirecting to login...');
          setTimeout(() => { window.location.href = `${baseUrl}auth/login`; }, 2000);
          return;
        }

        setStatus('success');
        setMessage('Authentication successful! Redirecting...');
        window.dispatchEvent(new Event('auth-state-changed'));

        let onboardingCompleted = false;
        try {
          const authServerUrl = (window as any).docusaurus?.siteConfig?.customFields?.betterAuthUrl || 'http://localhost:3001';
          const statusRes = await fetch(`${authServerUrl}/api/auth/onboarding/status`, { credentials: 'include' });
          if (statusRes.ok) {
            const statusData = await statusRes.json();
            onboardingCompleted = statusData.onboarding_completed === true;
          }
        } catch {
          onboardingCompleted = session.data.onboarding_completed === true;
        }

        setTimeout(() => {
          window.location.href = onboardingCompleted
            ? `${baseUrl}stage-1/intro`
            : `${baseUrl}onboarding/step-1`;
        }, 1000);
      } catch {
        setStatus('error');
        setMessage('An unexpected error occurred. Redirecting to login...');
        setTimeout(() => { window.location.href = `${baseUrl}auth/login`; }, 3000);
      }
    };

    handleCallback();
  }, []);

  return (
    <Layout title="Authentication" description="Processing authentication" noFooter>
      <div style={{
        minHeight: 'calc(100vh - 60px)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: '#0d0d12',
      }}>
        <div style={{
          maxWidth: 420,
          width: '100%',
          margin: '0 1rem',
          padding: '3rem 2rem',
          textAlign: 'center',
          background: '#16161f',
          border: '1px solid rgba(255,255,255,0.08)',
          borderRadius: '1.25rem',
          boxShadow: '0 25px 50px rgba(0,0,0,0.5)',
        }}>
          {status === 'loading' && (
            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '1.5rem' }}>
              <TriangleLoader size="lg" />
            </div>
          )}

          {status === 'success' && (
            <div style={{
              width: 64, height: 64,
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #4f46e5, #6366f1)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              margin: '0 auto 1.5rem',
              boxShadow: '0 0 30px rgba(99,102,241,0.4)',
            }}>
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="20 6 9 17 4 12" />
              </svg>
            </div>
          )}

          {status === 'error' && (
            <div style={{
              width: 64, height: 64,
              borderRadius: '50%',
              background: 'rgba(239,68,68,0.15)',
              border: '2px solid rgba(239,68,68,0.4)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              margin: '0 auto 1.5rem',
            }}>
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fca5a5" strokeWidth="2.5" strokeLinecap="round">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </div>
          )}

          <h2 style={{
            fontFamily: 'var(--font-heading)',
            fontSize: '1.375rem',
            fontWeight: 600,
            color: '#f1f5f9',
            marginBottom: '0.625rem',
          }}>
            {status === 'loading' && 'Authenticating…'}
            {status === 'success' && 'Success!'}
            {status === 'error' && 'Authentication Error'}
          </h2>

          <p style={{ color: '#64748b', fontSize: '0.9rem', lineHeight: 1.6 }}>
            {message}
          </p>
        </div>
      </div>
    </Layout>
  );
}

export default function CallbackPage() {
  return (
    <BrowserOnly fallback={<div style={{ minHeight: '100vh' }} />}>
      {() => <CallbackPageContent />}
    </BrowserOnly>
  );
}
