import React, { useState, useEffect } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import Layout from '@theme/Layout';
import StepIndicator from '../../components/onboarding/StepIndicator';
import TriangleLoader from '../../components/ui/TriangleLoader';
import { authClient } from '../../lib/auth';

const SOURCES = [
  { value: 'search',        label: 'Search Engine' },
  { value: 'social_media',  label: 'Social Media' },
  { value: 'friend',        label: 'Friend / Colleague' },
  { value: 'university',    label: 'University' },
  { value: 'conference',    label: 'Conference / Event' },
  { value: 'blog',          label: 'Blog / Article' },
  { value: 'other',         label: 'Other' },
];

function ConfettiOnMount() {
  useEffect(() => {
    let cancelled = false;
    import('canvas-confetti')
      .then(({ default: confetti }) => {
        if (!cancelled) {
          confetti({
            particleCount: 120,
            spread: 80,
            origin: { y: 0.55 },
            colors: ['#4f46e5', '#6366f1', '#a78bfa', '#f1f5f9'],
          });
        }
      })
      .catch(() => {/* canvas-confetti not installed — silent */});

    return () => { cancelled = true; };
  }, []);

  return null;
}

function Step4Content() {
  const [source, setSource] = useState('');
  const [completed, setCompleted] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleComplete = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (!source) { setError('Please let us know how you heard about us'); setLoading(false); return; }

      const stepRes = await fetch(`${authClient.baseURL}/api/auth/onboarding/step`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ step: 'additional', data: { how_did_you_hear: source, additional_notes: '' } }),
      });
      const stepResult = await stepRes.json();
      if (!stepRes.ok) { setError(stepResult.message || 'Failed to save'); setLoading(false); return; }

      const completeRes = await fetch(`${authClient.baseURL}/api/auth/onboarding/complete`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
      });
      const completeResult = await completeRes.json();
      if (!completeRes.ok) { setError(completeResult.message || 'Failed to complete'); setLoading(false); return; }

      window.dispatchEvent(new Event('auth-state-changed'));
      setCompleted(true);
      setLoading(false);
    } catch {
      setError('An unexpected error occurred. Please try again.');
      setLoading(false);
    }
  };

  const handleBack = () => {
    const baseUrl = (window as any).docusaurus?.siteConfig?.baseUrl || '/AINativeBook/';
    window.location.href = `${baseUrl}onboarding/step-3`;
  };

  const goToDashboard = () => {
    const baseUrl = (window as any).docusaurus?.siteConfig?.baseUrl || '/AINativeBook/';
    window.location.href = `${baseUrl}stage-1/intro`;
  };

  if (completed) {
    return (
      <Layout title="Welcome to IntelliStack!" noFooter>
        <ConfettiOnMount />
        <div className="onboarding-wrapper">
          <div className="onboarding-card">
            <div style={{ height: 3, background: 'linear-gradient(90deg, #4f46e5, #6366f1)' }} />
            <div className="onboarding-card-body" style={{ textAlign: 'center', padding: '3rem 2rem' }}>
              <div className="onboarding-success-icon">🎉</div>
              <h1 className="onboarding-heading" style={{ textAlign: 'center' }}>You're all set!</h1>
              <p className="onboarding-subtext" style={{ textAlign: 'center', maxWidth: 320, margin: '0 auto 2rem' }}>
                Your IntelliStack account is ready. Let's start building the future of Physical AI.
              </p>
              <button onClick={goToDashboard} className="onboarding-btn-continue" style={{ margin: '0 auto' }}>
                Start Learning →
              </button>
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout title="Onboarding - Step 4" description="Almost there" noFooter>
      <div className="onboarding-wrapper">
        <div className="onboarding-card">
          <StepIndicator currentStep={4} />
          <div className="onboarding-card-body">
            <h1 className="onboarding-heading">Almost there!</h1>
            <p className="onboarding-subtext">One last thing before you start your journey.</p>

            {error && <div className="onboarding-error">{error}</div>}

            <form onSubmit={handleComplete}>
              <label className="onboarding-label">How did you hear about us?</label>
              <div className="onboarding-pills" style={{ marginBottom: '1.5rem' }}>
                {SOURCES.map(s => (
                  <button
                    key={s.value}
                    type="button"
                    onClick={() => setSource(s.value)}
                    className={`onboarding-pill${source === s.value ? ' active' : ''}`}
                  >
                    {s.label}
                  </button>
                ))}
              </div>

              <div className="onboarding-nav">
                <button type="button" onClick={handleBack} className="onboarding-btn-back" disabled={loading}>
                  ← Back
                </button>
                <button type="submit" disabled={loading} className="onboarding-btn-continue">
                  {loading && <TriangleLoader size="sm" />}
                  Complete setup
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default function Step4Page() {
  return (
    <BrowserOnly fallback={<div style={{ minHeight: '100vh' }} />}>
      {() => <Step4Content />}
    </BrowserOnly>
  );
}
