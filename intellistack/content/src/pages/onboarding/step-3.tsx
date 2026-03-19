import React, { useState } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import Layout from '@theme/Layout';
import StepIndicator from '../../components/onboarding/StepIndicator';
import { authClient } from '../../lib/auth';

function Step3Content() {
  const [learningGoals, setLearningGoals] = useState<string[]>([]);
  const [learningStyle, setLearningStyle] = useState('');
  const [topicsOfInterest, setTopicsOfInterest] = useState<string[]>([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleGoalToggle = (goal: string) => {
    setLearningGoals(prev =>
      prev.includes(goal)
        ? prev.filter(g => g !== goal)
        : [...prev, goal]
    );
  };

  const handleTopicToggle = (topic: string) => {
    setTopicsOfInterest(prev =>
      prev.includes(topic)
        ? prev.filter(t => t !== topic)
        : [...prev, topic]
    );
  };

  const handleNext = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Validate inputs
      if (learningGoals.length === 0) {
        setError('Please select at least one learning goal');
        setLoading(false);
        return;
      }

      if (!learningStyle || !['visual', 'reading', 'hands_on', 'mixed'].includes(learningStyle)) {
        setError('Please select your learning style');
        setLoading(false);
        return;
      }

      if (topicsOfInterest.length === 0) {
        setError('Please select at least one topic of interest');
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
          step: 'interests',
          data: {
            learning_goals: learningGoals,
            learning_style: learningStyle,
            topics_of_interest: topicsOfInterest,
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
      window.location.href = `${baseUrl}onboarding/step-4`;
    } catch (err) {
      console.error('Error saving step 3:', err);
      setError('An unexpected error occurred. Please try again.');
      setLoading(false);
    }
  };

  const handleBack = () => {
    const baseUrl = (window as any).docusaurus?.siteConfig?.baseUrl || '/AINativeBook/';
    window.location.href = `${baseUrl}onboarding/step-2`;
  };

  const goalOptions = [
    { value: 'career_change', label: 'Career Change' },
    { value: 'academic_research', label: 'Academic Research' },
    { value: 'hobby', label: 'Hobby / Personal Interest' },
    { value: 'professional_development', label: 'Professional Development' },
  ];

  const topicOptions = [
    { value: 'ros2', label: 'ROS 2 Fundamentals' },
    { value: 'simulation', label: 'Simulation (Gazebo)' },
    { value: 'perception', label: 'Perception & Computer Vision' },
    { value: 'ai_integration', label: 'AI Integration' },
    { value: 'hardware', label: 'Hardware & Electronics' },
  ];

  return (
    <Layout title="Onboarding - Step 3" description="Academic Interests">
      <div style={{
        maxWidth: '600px',
        margin: '4rem auto',
        padding: '2rem',
      }}>
        <StepIndicator currentStep={3} />

        <div style={{
          backgroundColor: 'var(--ifm-background-surface-color)',
          padding: '2rem',
          borderRadius: '8px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        }}>
          <h1 style={{ marginBottom: '0.5rem' }}>Academic Interests</h1>
          <p style={{ color: 'var(--ifm-color-emphasis-600)', marginBottom: '2rem' }}>
            Help us personalize your learning experience.
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
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
                Learning Goals * (Select all that apply)
              </label>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {goalOptions.map(option => (
                  <label
                    key={option.value}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      padding: '0.75rem',
                      border: '1px solid var(--ifm-color-emphasis-300)',
                      borderRadius: '4px',
                      cursor: 'pointer',
                      backgroundColor: learningGoals.includes(option.value)
                        ? 'var(--ifm-color-primary-lightest)'
                        : 'transparent',
                    }}
                  >
                    <input
                      type="checkbox"
                      checked={learningGoals.includes(option.value)}
                      onChange={() => handleGoalToggle(option.value)}
                      disabled={loading}
                      style={{ marginRight: '0.75rem' }}
                    />
                    {option.label}
                  </label>
                ))}
              </div>
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <label htmlFor="learningStyle" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
                Preferred Learning Style *
              </label>
              <select
                id="learningStyle"
                value={learningStyle}
                onChange={(e) => setLearningStyle(e.target.value)}
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
                <option value="">Select your learning style</option>
                <option value="visual">Visual - Videos and diagrams</option>
                <option value="reading">Reading - Text and documentation</option>
                <option value="hands_on">Hands-on - Practice and experiments</option>
                <option value="mixed">Mixed - Combination of all</option>
              </select>
            </div>

            <div style={{ marginBottom: '2rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
                Topics of Interest * (Select all that apply)
              </label>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {topicOptions.map(option => (
                  <label
                    key={option.value}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      padding: '0.75rem',
                      border: '1px solid var(--ifm-color-emphasis-300)',
                      borderRadius: '4px',
                      cursor: 'pointer',
                      backgroundColor: topicsOfInterest.includes(option.value)
                        ? 'var(--ifm-color-primary-lightest)'
                        : 'transparent',
                    }}
                  >
                    <input
                      type="checkbox"
                      checked={topicsOfInterest.includes(option.value)}
                      onChange={() => handleTopicToggle(option.value)}
                      disabled={loading}
                      style={{ marginRight: '0.75rem' }}
                    />
                    {option.label}
                  </label>
                ))}
              </div>
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

export default function Step3Page() {
  return (
    <BrowserOnly fallback={<div>Loading...</div>}>
      {() => <Step3Content />}
    </BrowserOnly>
  );
}
