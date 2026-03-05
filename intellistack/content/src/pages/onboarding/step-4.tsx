import React, { useState } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import Layout from '@theme/Layout';
import StepIndicator from '../../components/onboarding/StepIndicator';
import { authClient } from '../../lib/auth';

function Step4Content() {
  const [howDidYouHear, setHowDidYouHear] = useState('');
  const [additionalNotes, setAdditionalNotes] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleComplete = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Validate inputs
      if (!howDidYouHear || howDidYouHear.trim().length === 0) {
        setError('Please let us know how you heard about us');
        setLoading(false);
        return;
      }

      // Save step data
      const stepResponse = await fetch(`${authClient.baseURL}/api/auth/onboarding/step`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          step: 'additional',
          data: {
            how_did_you_hear: howDidYouHear,
            additional_notes: additionalNotes.trim(),
          },
        }),
      });

      const stepResult = await stepResponse.json();

      if (!stepResponse.ok) {
        setError(stepResult.message || 'Failed to save step data');
        setLoading(false);
        return;
      }

      // Complete onboarding
      const completeResponse = await fetch(`${authClient.baseURL}/api/auth/onboarding/complete`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
      });

      const completeResult = await completeResponse.json();

      if (!completeResponse.ok) {
        setError(completeResult.message || 'Failed to complete onboarding');
        setLoading(false);
        return;
      }

      // Dispatch auth state change event
      window.dispatchEvent(new Event('auth-state-changed'));

      // Redirect to book content
      const baseUrl = (window as any).docusaurus?.siteConfig?.baseUrl || '/AINativeBook/';
      window.location.href = `${baseUrl}stage-1/intro`;
    } catch (err) {
      console.error('Error completing onboarding:', err);
      setError('An unexpected error occurred. Please try again.');
      setLoading(false);
    }
  };

  const handleBack = () => {
    const baseUrl = (window as any).docusaurus?.siteConfig?.baseUrl || '/AINativeBook/';
    window.location.href = `${baseUrl}onboarding/step-3`;
  };

  return (
    <Layout title="Onboarding - Step 4" description="Additional Details">
      <div style={{
        maxWidth: '600px',
        margin: '4rem auto',
        padding: '2rem',
      }}>
        <StepIndicator currentStep={4} />

        <div style={{
          backgroundColor: 'var(--ifm-background-surface-color)',
          padding: '2rem',
          borderRadius: '8px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        }}>
          <h1 style={{ marginBottom: '0.5rem' }}>Additional Details</h1>
          <p style={{ color: 'var(--ifm-color-emphasis-600)', marginBottom: '2rem' }}>
            Just a few more details to complete your profile.
          </p>

          {error && (
            <div style={{
              padding: '1rem',
              marginBottom: '1rem',
              backgroundColor: '#fee',
              border: '1px solid #fcc',
              borderRadius: '4px',
              color: '#c33',
            }}>
              {error}
            </div>
          )}

          <form onSubmit={handleComplete}>
            <div style={{ marginBottom: '1.5rem' }}>
              <label htmlFor="howDidYouHear" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
                How did you hear about us? *
              </label>
              <select
                id="howDidYouHear"
                value={howDidYouHear}
                onChange={(e) => setHowDidYouHear(e.target.value)}
                disabled={loading}
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  fontSize: '1rem',
                  border: '1px solid var(--ifm-color-emphasis-300)',
                  borderRadius: '4px',
                  backgroundColor: 'var(--ifm-background-color)',
                }}
                required
              >
                <option value="">Select an option</option>
                <option value="search">Search Engine (Google, Bing, etc.)</option>
                <option value="social_media">Social Media</option>
                <option value="friend">Friend or Colleague</option>
                <option value="university">University or Institution</option>
                <option value="conference">Conference or Event</option>
                <option value="blog">Blog or Article</option>
                <option value="other">Other</option>
              </select>
            </div>

            <div style={{ marginBottom: '2rem' }}>
              <label htmlFor="additionalNotes" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
                Additional Notes (Optional)
              </label>
              <textarea
                id="additionalNotes"
                value={additionalNotes}
                onChange={(e) => setAdditionalNotes(e.target.value)}
                placeholder="Tell us anything else you'd like us to know..."
                disabled={loading}
                rows={4}
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  fontSize: '1rem',
                  border: '1px solid var(--ifm-color-emphasis-300)',
                  borderRadius: '4px',
                  backgroundColor: 'var(--ifm-background-color)',
                  resize: 'vertical',
                }}
              />
              <small style={{ color: 'var(--ifm-color-emphasis-600)', fontSize: '0.875rem' }}>
                Share your goals, expectations, or any questions you have
              </small>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <button
                type="button"
                onClick={handleBack}
                disabled={loading}
                style={{
                  padding: '0.75rem 2rem',
                  fontSize: '1rem',
                  fontWeight: 'bold',
                  color: 'var(--ifm-color-emphasis-700)',
                  backgroundColor: 'transparent',
                  border: '1px solid var(--ifm-color-emphasis-300)',
                  borderRadius: '4px',
                  cursor: loading ? 'not-allowed' : 'pointer',
                  opacity: loading ? 0.6 : 1,
                }}
              >
                Back
              </button>
              <button
                type="submit"
                disabled={loading}
                style={{
                  padding: '0.75rem 2rem',
                  fontSize: '1rem',
                  fontWeight: 'bold',
                  color: 'white',
                  backgroundColor: 'var(--ifm-color-success)',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: loading ? 'not-allowed' : 'pointer',
                  opacity: loading ? 0.6 : 1,
                }}
              >
                {loading ? 'Completing...' : 'Complete Onboarding'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Layout>
  );
}

export default function Step4Page() {
  return (
    <BrowserOnly fallback={<div>Loading...</div>}>
      {() => <Step4Content />}
    </BrowserOnly>
  );
}
