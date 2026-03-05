import React, { useState } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import Layout from '@theme/Layout';
import StepIndicator from '../../components/onboarding/StepIndicator';
import { authClient } from '../../lib/auth';

function Step1Content() {
  const [fullName, setFullName] = useState('');
  const [preferredLanguage, setPreferredLanguage] = useState('en');
  const [timezone, setTimezone] = useState('America/New_York');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleNext = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Validate inputs
      if (!fullName || fullName.trim().length === 0) {
        setError('Full name is required');
        setLoading(false);
        return;
      }

      if (!preferredLanguage || !['en', 'ur'].includes(preferredLanguage)) {
        setError('Please select a valid language');
        setLoading(false);
        return;
      }

      if (!timezone || timezone.trim().length === 0) {
        setError('Timezone is required');
        setLoading(false);
        return;
      }

      // Save step data
      const response = await fetch(`${authClient.baseURL}/api/auth/onboarding/step`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          step: 'basic_info',
          data: {
            full_name: fullName.trim(),
            preferred_language: preferredLanguage,
            timezone: timezone,
          },
        }),
      });

      const result = await response.json();

      if (!response.ok) {
        setError(result.message || 'Failed to save step data');
        setLoading(false);
        return;
      }

      // Navigate to next step
      const baseUrl = (window as any).docusaurus?.siteConfig?.baseUrl || '/AINativeBook/';
      window.location.href = `${baseUrl}onboarding/step-2`;
    } catch (err) {
      console.error('Error saving step 1:', err);
      setError('An unexpected error occurred. Please try again.');
      setLoading(false);
    }
  };

  return (
    <Layout title="Onboarding - Step 1" description="Basic Information">
      <div style={{
        maxWidth: '600px',
        margin: '4rem auto',
        padding: '2rem',
      }}>
        <StepIndicator currentStep={1} />

        <div style={{
          backgroundColor: 'var(--ifm-background-surface-color)',
          padding: '2rem',
          borderRadius: '8px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        }}>
          <h1 style={{ marginBottom: '0.5rem' }}>Basic Information</h1>
          <p style={{ color: 'var(--ifm-color-emphasis-600)', marginBottom: '2rem' }}>
            Let's start with some basic information about you.
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

          <form onSubmit={handleNext}>
            <div style={{ marginBottom: '1.5rem' }}>
              <label htmlFor="fullName" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
                Full Name *
              </label>
              <input
                id="fullName"
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="John Doe"
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
              />
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <label htmlFor="preferredLanguage" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
                Preferred Language *
              </label>
              <select
                id="preferredLanguage"
                value={preferredLanguage}
                onChange={(e) => setPreferredLanguage(e.target.value)}
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
                <option value="en">English</option>
                <option value="ur">Urdu</option>
              </select>
            </div>

            <div style={{ marginBottom: '2rem' }}>
              <label htmlFor="timezone" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
                Timezone *
              </label>
              <select
                id="timezone"
                value={timezone}
                onChange={(e) => setTimezone(e.target.value)}
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
                <option value="America/New_York">Eastern Time (US & Canada)</option>
                <option value="America/Chicago">Central Time (US & Canada)</option>
                <option value="America/Denver">Mountain Time (US & Canada)</option>
                <option value="America/Los_Angeles">Pacific Time (US & Canada)</option>
                <option value="Europe/London">London</option>
                <option value="Europe/Paris">Paris</option>
                <option value="Asia/Dubai">Dubai</option>
                <option value="Asia/Karachi">Karachi</option>
                <option value="Asia/Kolkata">Mumbai, Kolkata</option>
                <option value="Asia/Shanghai">Beijing, Shanghai</option>
                <option value="Asia/Tokyo">Tokyo</option>
                <option value="Australia/Sydney">Sydney</option>
              </select>
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
              <button
                type="submit"
                disabled={loading}
                style={{
                  padding: '0.75rem 2rem',
                  fontSize: '1rem',
                  fontWeight: 'bold',
                  color: 'white',
                  backgroundColor: 'var(--ifm-color-primary)',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: loading ? 'not-allowed' : 'pointer',
                  opacity: loading ? 0.6 : 1,
                }}
              >
                {loading ? 'Saving...' : 'Next'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Layout>
  );
}

export default function Step1Page() {
  return (
    <BrowserOnly fallback={<div>Loading...</div>}>
      {() => <Step1Content />}
    </BrowserOnly>
  );
}
