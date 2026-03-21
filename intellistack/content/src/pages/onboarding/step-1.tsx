import React, { useState } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import Layout from '@theme/Layout';
import StepIndicator from '../../components/onboarding/StepIndicator';
import TriangleLoader from '../../components/ui/TriangleLoader';
import { authClient } from '../../lib/auth';

const LANGUAGES = [
  { value: 'en', label: 'English' },
  { value: 'ur', label: 'اردو' },
];

const TIMEZONES = [
  { value: 'America/New_York',    label: 'Eastern (US)' },
  { value: 'America/Chicago',     label: 'Central (US)' },
  { value: 'America/Denver',      label: 'Mountain (US)' },
  { value: 'America/Los_Angeles', label: 'Pacific (US)' },
  { value: 'Europe/London',       label: 'London' },
  { value: 'Europe/Paris',        label: 'Paris' },
  { value: 'Asia/Dubai',          label: 'Dubai' },
  { value: 'Asia/Karachi',        label: 'Karachi' },
  { value: 'Asia/Kolkata',        label: 'Mumbai / Kolkata' },
  { value: 'Asia/Shanghai',       label: 'Beijing / Shanghai' },
  { value: 'Asia/Tokyo',          label: 'Tokyo' },
  { value: 'Australia/Sydney',    label: 'Sydney' },
];

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
      if (!fullName.trim()) { setError('Full name is required'); setLoading(false); return; }

      const response = await fetch(`${authClient.baseURL}/api/auth/onboarding/step`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          step: 'basic_info',
          data: { full_name: fullName.trim(), preferred_language: preferredLanguage, timezone },
        }),
      });
      const result = await response.json();
      if (!response.ok) { setError(result.message || 'Failed to save'); setLoading(false); return; }

      const baseUrl = (window as any).docusaurus?.siteConfig?.baseUrl || '/AINativeBook/';
      window.location.href = `${baseUrl}onboarding/step-2`;
    } catch {
      setError('An unexpected error occurred. Please try again.');
      setLoading(false);
    }
  };

  return (
    <Layout title="Onboarding - Step 1" description="Basic Information" noFooter>
      <div className="onboarding-wrapper">
        <div className="onboarding-card">
          <StepIndicator currentStep={1} />
          <div className="onboarding-card-body">
            <h1 className="onboarding-heading">Let's get to know you</h1>
            <p className="onboarding-subtext">A few details to personalize your experience.</p>

            {error && <div className="onboarding-error">{error}</div>}

            <form onSubmit={handleNext}>
              <label htmlFor="fullName" className="onboarding-label">Full Name</label>
              <input
                id="fullName"
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Your full name"
                disabled={loading}
                className="onboarding-input"
                style={{ marginBottom: '1.25rem' }}
                required
              />

              <label className="onboarding-label">Preferred Language</label>
              <div className="onboarding-pills" style={{ marginBottom: '1.25rem' }}>
                {LANGUAGES.map(lang => (
                  <button
                    key={lang.value}
                    type="button"
                    onClick={() => setPreferredLanguage(lang.value)}
                    className={`onboarding-pill${preferredLanguage === lang.value ? ' active' : ''}`}
                  >
                    {lang.label}
                  </button>
                ))}
              </div>

              <label htmlFor="timezone" className="onboarding-label">Timezone</label>
              <select
                id="timezone"
                value={timezone}
                onChange={(e) => setTimezone(e.target.value)}
                disabled={loading}
                className="onboarding-input"
                style={{ marginBottom: 0, cursor: 'pointer' }}
                required
              >
                {TIMEZONES.map(tz => (
                  <option key={tz.value} value={tz.value}>{tz.label}</option>
                ))}
              </select>

              <div className="onboarding-nav">
                <span />
                <button type="submit" disabled={loading} className="onboarding-btn-continue">
                  {loading && <TriangleLoader size="sm" />}
                  Continue →
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default function Step1Page() {
  return (
    <BrowserOnly fallback={<div style={{ minHeight: '100vh' }} />}>
      {() => <Step1Content />}
    </BrowserOnly>
  );
}
