import React, { useState } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import Layout from '@theme/Layout';
import StepIndicator from '../../components/onboarding/StepIndicator';
import TriangleLoader from '../../components/ui/TriangleLoader';
import { authClient } from '../../lib/auth';

const ROLES = [
  { value: 'undergraduate', label: 'Student' },
  { value: 'professional',  label: 'Professional' },
  { value: 'graduate',      label: 'Researcher' },
  { value: 'high_school',   label: 'Hobbyist' },
];

const EXPERIENCE = [
  { value: 'none',         label: 'No experience' },
  { value: 'beginner',     label: 'Beginner' },
  { value: 'intermediate', label: 'Intermediate' },
  { value: 'advanced',     label: 'Advanced' },
];

function Step2Content() {
  const [role, setRole] = useState('');
  const [experience, setExperience] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleNext = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (!role) { setError('Please select your role'); setLoading(false); return; }
      if (!experience) { setError('Please select your experience level'); setLoading(false); return; }

      const response = await fetch(`${authClient.baseURL}/api/auth/onboarding/step`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          step: 'education',
          data: { level: role, field_of_study: ROLES.find(r => r.value === role)?.label || role, prior_experience: experience },
        }),
      });
      const result = await response.json();
      if (!response.ok) { setError(result.message || 'Failed to save'); setLoading(false); return; }

      const baseUrl = (window as any).docusaurus?.siteConfig?.baseUrl || '/AINativeBook/';
      window.location.href = `${baseUrl}onboarding/step-3`;
    } catch {
      setError('An unexpected error occurred. Please try again.');
      setLoading(false);
    }
  };

  const handleBack = () => {
    const baseUrl = (window as any).docusaurus?.siteConfig?.baseUrl || '/AINativeBook/';
    window.location.href = `${baseUrl}onboarding/step-1`;
  };

  return (
    <Layout title="Onboarding - Step 2" description="Your Role" noFooter>
      <div className="onboarding-wrapper">
        <div className="onboarding-card">
          <StepIndicator currentStep={2} />
          <div className="onboarding-card-body">
            <h1 className="onboarding-heading">What describes you?</h1>
            <p className="onboarding-subtext">We'll tailor the curriculum to your background.</p>

            {error && <div className="onboarding-error">{error}</div>}

            <form onSubmit={handleNext}>
              <label className="onboarding-label">I am a…</label>
              <div className="onboarding-pills" style={{ marginBottom: '1.75rem' }}>
                {ROLES.map(r => (
                  <button
                    key={r.value}
                    type="button"
                    onClick={() => setRole(r.value)}
                    className={`onboarding-pill${role === r.value ? ' active' : ''}`}
                  >
                    {r.label}
                  </button>
                ))}
              </div>

              <label className="onboarding-label">Robotics experience</label>
              <div className="onboarding-pills">
                {EXPERIENCE.map(exp => (
                  <button
                    key={exp.value}
                    type="button"
                    onClick={() => setExperience(exp.value)}
                    className={`onboarding-pill${experience === exp.value ? ' active' : ''}`}
                  >
                    {exp.label}
                  </button>
                ))}
              </div>

              <div className="onboarding-nav">
                <button type="button" onClick={handleBack} className="onboarding-btn-back" disabled={loading}>
                  ← Back
                </button>
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

export default function Step2Page() {
  return (
    <BrowserOnly fallback={<div style={{ minHeight: '100vh' }} />}>
      {() => <Step2Content />}
    </BrowserOnly>
  );
}
