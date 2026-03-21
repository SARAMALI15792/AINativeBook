import React, { useState } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import Layout from '@theme/Layout';
import StepIndicator from '../../components/onboarding/StepIndicator';
import TriangleLoader from '../../components/ui/TriangleLoader';
import { authClient } from '../../lib/auth';

const LEARNING_PATHS = [
  { value: 'solo',     emoji: '🧑‍💻', label: 'Solo Learner',     desc: 'Self-paced, independent' },
  { value: 'team',     emoji: '👥',    label: 'Part of a Team',   desc: 'Collaborative projects' },
  { value: 'academic', emoji: '🎓',    label: 'Academic Cohort',  desc: 'University / institution' },
];

const GOALS = [
  { value: 'career_change',           label: 'Career Change' },
  { value: 'academic_research',        label: 'Academic Research' },
  { value: 'hobby',                    label: 'Hobby' },
  { value: 'professional_development', label: 'Professional Development' },
];

function Step3Content() {
  const [path, setPath] = useState('');
  const [goals, setGoals] = useState<string[]>([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const toggleGoal = (value: string) => {
    setGoals(prev => prev.includes(value) ? prev.filter(g => g !== value) : [...prev, value]);
  };

  const handleNext = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (!path) { setError('Please select your learning path'); setLoading(false); return; }
      if (goals.length === 0) { setError('Please select at least one goal'); setLoading(false); return; }

      const response = await fetch(`${authClient.baseURL}/api/auth/onboarding/step`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          step: 'interests',
          data: {
            learning_goals: goals,
            learning_style: path === 'solo' ? 'hands_on' : path === 'team' ? 'mixed' : 'reading',
            topics_of_interest: ['ros2', 'ai_integration'],
          },
        }),
      });
      const result = await response.json();
      if (!response.ok) { setError(result.message || 'Failed to save'); setLoading(false); return; }

      const baseUrl = (window as any).docusaurus?.siteConfig?.baseUrl || '/AINativeBook/';
      window.location.href = `${baseUrl}onboarding/step-4`;
    } catch {
      setError('An unexpected error occurred. Please try again.');
      setLoading(false);
    }
  };

  const handleBack = () => {
    const baseUrl = (window as any).docusaurus?.siteConfig?.baseUrl || '/AINativeBook/';
    window.location.href = `${baseUrl}onboarding/step-2`;
  };

  return (
    <Layout title="Onboarding - Step 3" description="Your Learning Path" noFooter>
      <div className="onboarding-wrapper">
        <div className="onboarding-card">
          <StepIndicator currentStep={3} />
          <div className="onboarding-card-body">
            <h1 className="onboarding-heading">How do you learn?</h1>
            <p className="onboarding-subtext">Help us match you with the right experience.</p>

            {error && <div className="onboarding-error">{error}</div>}

            <form onSubmit={handleNext}>
              <label className="onboarding-label" style={{ marginBottom: '0.75rem', display: 'block' }}>Learning context</label>
              <div className="onboarding-icon-cards" style={{ marginBottom: '1.75rem' }}>
                {LEARNING_PATHS.map(lp => (
                  <button
                    key={lp.value}
                    type="button"
                    onClick={() => setPath(lp.value)}
                    className={`onboarding-icon-card${path === lp.value ? ' active' : ''}`}
                  >
                    <span className="onboarding-icon-card-emoji">{lp.emoji}</span>
                    <span className="onboarding-icon-card-label" style={{ fontWeight: 600, color: path === lp.value ? undefined : '#f1f5f9', marginBottom: '0.25rem', display: 'block', fontSize: '0.875rem' }}>{lp.label}</span>
                    <span className="onboarding-icon-card-label" style={{ fontSize: '0.75rem' }}>{lp.desc}</span>
                  </button>
                ))}
              </div>

              <label className="onboarding-label">Learning goals</label>
              <div className="onboarding-pills">
                {GOALS.map(g => (
                  <button
                    key={g.value}
                    type="button"
                    onClick={() => toggleGoal(g.value)}
                    className={`onboarding-pill${goals.includes(g.value) ? ' active' : ''}`}
                  >
                    {g.label}
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

export default function Step3Page() {
  return (
    <BrowserOnly fallback={<div style={{ minHeight: '100vh' }} />}>
      {() => <Step3Content />}
    </BrowserOnly>
  );
}
