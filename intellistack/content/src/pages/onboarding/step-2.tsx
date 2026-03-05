import React, { useState } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import Layout from '@theme/Layout';
import StepIndicator from '../../components/onboarding/StepIndicator';
import { authClient } from '../../lib/auth';

function Step2Content() {
  const [level, setLevel] = useState('');
  const [fieldOfStudy, setFieldOfStudy] = useState('');
  const [priorExperience, setPriorExperience] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleNext = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Validate inputs
      if (!level || !['high_school', 'undergraduate', 'graduate', 'professional'].includes(level)) {
        setError('Please select your education level');
        setLoading(false);
        return;
      }

      if (!fieldOfStudy || fieldOfStudy.trim().length === 0) {
        setError('Field of study is required');
        setLoading(false);
        return;
      }

      if (!priorExperience || !['none', 'beginner', 'intermediate', 'advanced'].includes(priorExperience)) {
        setError('Please select your prior experience level');
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
          step: 'education',
          data: {
            level: level,
            field_of_study: fieldOfStudy.trim(),
            prior_experience: priorExperience,
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
      window.location.href = `${baseUrl}onboarding/step-3`;
    } catch (err) {
      console.error('Error saving step 2:', err);
      setError('An unexpected error occurred. Please try again.');
      setLoading(false);
    }
  };

  const handleBack = () => {
    const baseUrl = (window as any).docusaurus?.siteConfig?.baseUrl || '/AINativeBook/';
    window.location.href = `${baseUrl}onboarding/step-1`;
  };

  return (
    <Layout title="Onboarding - Step 2" description="Educational Background">
      <div style={{
        maxWidth: '600px',
        margin: '4rem auto',
        padding: '2rem',
      }}>
        <StepIndicator currentStep={2} />

        <div style={{
          backgroundColor: 'var(--ifm-background-surface-color)',
          padding: '2rem',
          borderRadius: '8px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        }}>
          <h1 style={{ marginBottom: '0.5rem' }}>Educational Background</h1>
          <p style={{ color: 'var(--ifm-color-emphasis-600)', marginBottom: '2rem' }}>
            Tell us about your educational background and experience.
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
              <label htmlFor="level" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
                Education Level *
              </label>
              <select
                id="level"
                value={level}
                onChange={(e) => setLevel(e.target.value)}
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
                <option value="">Select your education level</option>
                <option value="high_school">High School</option>
                <option value="undergraduate">Undergraduate</option>
                <option value="graduate">Graduate</option>
                <option value="professional">Professional</option>
              </select>
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <label htmlFor="fieldOfStudy" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
                Field of Study *
              </label>
              <input
                id="fieldOfStudy"
                type="text"
                value={fieldOfStudy}
                onChange={(e) => setFieldOfStudy(e.target.value)}
                placeholder="e.g., Computer Science, Mechanical Engineering"
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

            <div style={{ marginBottom: '2rem' }}>
              <label htmlFor="priorExperience" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
                Prior Experience with Robotics *
              </label>
              <select
                id="priorExperience"
                value={priorExperience}
                onChange={(e) => setPriorExperience(e.target.value)}
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
                <option value="">Select your experience level</option>
                <option value="none">None - I'm just starting</option>
                <option value="beginner">Beginner - Some basic knowledge</option>
                <option value="intermediate">Intermediate - Completed projects</option>
                <option value="advanced">Advanced - Professional experience</option>
              </select>
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

export default function Step2Page() {
  return (
    <BrowserOnly fallback={<div>Loading...</div>}>
      {() => <Step2Content />}
    </BrowserOnly>
  );
}
