/**
 * Onboarding Wizard
 * Multi-step onboarding collecting user preferences
 */

import React, { useState, useEffect } from 'react';
import Layout from '@theme/Layout';
import { useHistory } from '@docusaurus/router';
import styles from './onboarding.module.css';

type OnboardingStep = 'system' | 'learning' | 'background' | 'complete';

interface SystemPreferences {
  theme: 'light' | 'dark' | 'system';
  os: 'windows' | 'macos' | 'linux' | 'other';
  deviceType: 'desktop' | 'laptop' | 'tablet';
  preferredIde: 'vscode' | 'pycharm' | 'clion' | 'nvim' | 'other';
  shellType: 'bash' | 'zsh' | 'powershell' | 'cmd' | 'fish';
}

interface LearningPreferences {
  learningStyle: 'visual' | 'reading' | 'hands-on' | 'mixed';
  pacePreference: 'self-paced' | 'structured' | 'intensive';
  goalTimeframe: '3-months' | '6-months' | '1-year' | 'flexible';
  focusAreas: string[];
}

interface BackgroundLevel {
  programmingExperience: 'none' | 'beginner' | 'intermediate' | 'advanced';
  roboticsExperience: 'none' | 'hobbyist' | 'academic' | 'professional';
  mathBackground: 'basic' | 'calculus' | 'linear-algebra' | 'advanced';
  linuxFamiliarity: 'none' | 'basic' | 'comfortable' | 'expert';
}

// Auto-detect OS
function detectOS(): SystemPreferences['os'] {
  if (typeof window === 'undefined') return 'other';
  const platform = navigator.platform.toLowerCase();
  if (platform.includes('win')) return 'windows';
  if (platform.includes('mac')) return 'macos';
  if (platform.includes('linux')) return 'linux';
  return 'other';
}

export default function OnboardingPage(): JSX.Element {
  const history = useHistory();
  const [currentStep, setCurrentStep] = useState<OnboardingStep>('system');
  const [isLoading, setIsLoading] = useState(false);
  const [authClient, setAuthClient] = useState<any>(null);
  const [backendUrl, setBackendUrl] = useState<string>('');

  const [systemPrefs, setSystemPrefs] = useState<SystemPreferences>({
    theme: 'system',
    os: detectOS(),
    deviceType: 'desktop',
    preferredIde: 'vscode',
    shellType: detectOS() === 'windows' ? 'powershell' : 'bash',
  });

  const [learningPrefs, setLearningPrefs] = useState<LearningPreferences>({
    learningStyle: 'hands-on',
    pacePreference: 'self-paced',
    goalTimeframe: '6-months',
    focusAreas: [],
  });

  const [backgroundLevel, setBackgroundLevel] = useState<BackgroundLevel>({
    programmingExperience: 'beginner',
    roboticsExperience: 'none',
    mathBackground: 'basic',
    linuxFamiliarity: 'none',
  });

  useEffect(() => {
    import('@site/src/lib/auth-client').then((mod) => {
      setAuthClient(mod.authClient);
      setBackendUrl(mod.getBackendUrl());

      // Check if logged in
      mod.authClient.getSession().then((result) => {
        if (!result.data?.user) {
          history.push('/login');
        }
      });
    });
  }, []);

  const steps: OnboardingStep[] = ['system', 'learning', 'background', 'complete'];
  const currentStepIndex = steps.indexOf(currentStep);

  const goNext = () => {
    const nextIndex = currentStepIndex + 1;
    if (nextIndex < steps.length) {
      setCurrentStep(steps[nextIndex]);
    }
  };

  const goBack = () => {
    const prevIndex = currentStepIndex - 1;
    if (prevIndex >= 0) {
      setCurrentStep(steps[prevIndex]);
    }
  };

  const handleComplete = async () => {
    setIsLoading(true);
    try {
      const session = await authClient.getSession();
      const token = session.data?.session?.token;

      // Save preferences to backend
      const response = await fetch(`${backendUrl}/api/v1/users/onboarding`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          system_preferences: systemPrefs,
          learning_preferences: learningPrefs,
          background_level: backgroundLevel,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to save preferences');
      }

      // Navigate to docs
      history.push('/docs/stage-1/intro');
    } catch (error) {
      console.error('Onboarding error:', error);
      // Continue anyway - preferences are optional
      history.push('/docs/stage-1/intro');
    } finally {
      setIsLoading(false);
    }
  };

  const focusAreaOptions = [
    { value: 'ros2', label: 'ROS 2 Development' },
    { value: 'simulation', label: 'Robot Simulation' },
    { value: 'computer-vision', label: 'Computer Vision' },
    { value: 'motion-planning', label: 'Motion Planning' },
    { value: 'machine-learning', label: 'Machine Learning' },
    { value: 'humanoid', label: 'Humanoid Robotics' },
  ];

  const toggleFocusArea = (area: string) => {
    setLearningPrefs(prev => ({
      ...prev,
      focusAreas: prev.focusAreas.includes(area)
        ? prev.focusAreas.filter(a => a !== area)
        : [...prev.focusAreas, area],
    }));
  };

  return (
    <Layout title="Welcome to IntelliStack" description="Complete your profile">
      <div className={styles.onboardingContainer}>
        <div className={styles.onboardingCard}>
          {/* Progress Bar */}
          <div className={styles.progressContainer}>
            <div className={styles.progressBar}>
              <div
                className={styles.progressFill}
                style={{ width: `${((currentStepIndex + 1) / steps.length) * 100}%` }}
              />
            </div>
            <div className={styles.progressSteps}>
              {steps.map((step, index) => (
                <div
                  key={step}
                  className={`${styles.progressStep} ${index <= currentStepIndex ? styles.active : ''}`}
                >
                  <span className={styles.stepNumber}>{index + 1}</span>
                  <span className={styles.stepLabel}>
                    {step === 'system' && 'Setup'}
                    {step === 'learning' && 'Goals'}
                    {step === 'background' && 'Experience'}
                    {step === 'complete' && 'Done'}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Step Content */}
          <div className={styles.stepContent}>
            {currentStep === 'system' && (
              <SystemStep
                preferences={systemPrefs}
                onChange={setSystemPrefs}
              />
            )}

            {currentStep === 'learning' && (
              <LearningStep
                preferences={learningPrefs}
                focusAreaOptions={focusAreaOptions}
                onToggleFocusArea={toggleFocusArea}
                onChange={setLearningPrefs}
              />
            )}

            {currentStep === 'background' && (
              <BackgroundStep
                level={backgroundLevel}
                onChange={setBackgroundLevel}
              />
            )}

            {currentStep === 'complete' && (
              <CompleteStep
                systemPrefs={systemPrefs}
                learningPrefs={learningPrefs}
                backgroundLevel={backgroundLevel}
              />
            )}
          </div>

          {/* Navigation */}
          <div className={styles.navigation}>
            {currentStepIndex > 0 && currentStep !== 'complete' && (
              <button onClick={goBack} className={styles.backButton}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polyline points="15 18 9 12 15 6"/>
                </svg>
                Back
              </button>
            )}
            <div style={{ flex: 1 }} />
            {currentStep !== 'complete' ? (
              <button onClick={goNext} className={styles.nextButton}>
                Continue
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polyline points="9 18 15 12 9 6"/>
                </svg>
              </button>
            ) : (
              <button onClick={handleComplete} className={styles.nextButton} disabled={isLoading}>
                {isLoading ? 'Starting...' : 'Start Learning'}
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polyline points="9 18 15 12 9 6"/>
                </svg>
              </button>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
}

// Step Components
function SystemStep({ preferences, onChange }: {
  preferences: SystemPreferences;
  onChange: (p: SystemPreferences) => void;
}) {
  return (
    <div className={styles.step}>
      <h2 className={styles.stepTitle}>Let's customize your experience</h2>
      <p className={styles.stepDescription}>
        Tell us about your setup so we can provide the best recommendations.
      </p>

      <div className={styles.formGrid}>
        <div className={styles.formGroup}>
          <label>Color Theme</label>
          <div className={styles.optionGroup}>
            {(['light', 'dark', 'system'] as const).map(opt => (
              <button
                key={opt}
                className={`${styles.optionButton} ${preferences.theme === opt ? styles.selected : ''}`}
                onClick={() => onChange({ ...preferences, theme: opt })}
              >
                {opt === 'light' && '☀️ Light'}
                {opt === 'dark' && '🌙 Dark'}
                {opt === 'system' && '💻 System'}
              </button>
            ))}
          </div>
        </div>

        <div className={styles.formGroup}>
          <label>Operating System</label>
          <div className={styles.optionGroup}>
            {(['windows', 'macos', 'linux'] as const).map(opt => (
              <button
                key={opt}
                className={`${styles.optionButton} ${preferences.os === opt ? styles.selected : ''}`}
                onClick={() => onChange({ ...preferences, os: opt })}
              >
                {opt === 'windows' && '🪟 Windows'}
                {opt === 'macos' && '🍎 macOS'}
                {opt === 'linux' && '🐧 Linux'}
              </button>
            ))}
          </div>
        </div>

        <div className={styles.formGroup}>
          <label>Preferred IDE</label>
          <div className={styles.optionGroup}>
            {(['vscode', 'pycharm', 'clion', 'nvim'] as const).map(opt => (
              <button
                key={opt}
                className={`${styles.optionButton} ${preferences.preferredIde === opt ? styles.selected : ''}`}
                onClick={() => onChange({ ...preferences, preferredIde: opt })}
              >
                {opt === 'vscode' && 'VS Code'}
                {opt === 'pycharm' && 'PyCharm'}
                {opt === 'clion' && 'CLion'}
                {opt === 'nvim' && 'Neovim'}
              </button>
            ))}
          </div>
        </div>

        <div className={styles.formGroup}>
          <label>Shell Environment</label>
          <div className={styles.optionGroup}>
            {(['bash', 'zsh', 'powershell', 'fish'] as const).map(opt => (
              <button
                key={opt}
                className={`${styles.optionButton} ${preferences.shellType === opt ? styles.selected : ''}`}
                onClick={() => onChange({ ...preferences, shellType: opt })}
              >
                {opt}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function LearningStep({ preferences, focusAreaOptions, onToggleFocusArea, onChange }: {
  preferences: LearningPreferences;
  focusAreaOptions: { value: string; label: string }[];
  onToggleFocusArea: (area: string) => void;
  onChange: (p: LearningPreferences) => void;
}) {
  return (
    <div className={styles.step}>
      <h2 className={styles.stepTitle}>What are your learning goals?</h2>
      <p className={styles.stepDescription}>
        Help us personalize your learning path.
      </p>

      <div className={styles.formGrid}>
        <div className={styles.formGroup}>
          <label>Learning Style</label>
          <div className={styles.optionGroup}>
            {(['visual', 'reading', 'hands-on', 'mixed'] as const).map(opt => (
              <button
                key={opt}
                className={`${styles.optionButton} ${preferences.learningStyle === opt ? styles.selected : ''}`}
                onClick={() => onChange({ ...preferences, learningStyle: opt })}
              >
                {opt === 'visual' && '👁️ Visual'}
                {opt === 'reading' && '📖 Reading'}
                {opt === 'hands-on' && '🛠️ Hands-on'}
                {opt === 'mixed' && '🎯 Mixed'}
              </button>
            ))}
          </div>
        </div>

        <div className={styles.formGroup}>
          <label>Pace Preference</label>
          <div className={styles.optionGroup}>
            {(['self-paced', 'structured', 'intensive'] as const).map(opt => (
              <button
                key={opt}
                className={`${styles.optionButton} ${preferences.pacePreference === opt ? styles.selected : ''}`}
                onClick={() => onChange({ ...preferences, pacePreference: opt })}
              >
                {opt === 'self-paced' && '🚶 Self-paced'}
                {opt === 'structured' && '📅 Structured'}
                {opt === 'intensive' && '🏃 Intensive'}
              </button>
            ))}
          </div>
        </div>

        <div className={styles.formGroup}>
          <label>Goal Timeframe</label>
          <div className={styles.optionGroup}>
            {(['3-months', '6-months', '1-year', 'flexible'] as const).map(opt => (
              <button
                key={opt}
                className={`${styles.optionButton} ${preferences.goalTimeframe === opt ? styles.selected : ''}`}
                onClick={() => onChange({ ...preferences, goalTimeframe: opt })}
              >
                {opt}
              </button>
            ))}
          </div>
        </div>

        <div className={styles.formGroup}>
          <label>Focus Areas (select all that interest you)</label>
          <div className={styles.chipGroup}>
            {focusAreaOptions.map(opt => (
              <button
                key={opt.value}
                className={`${styles.chip} ${preferences.focusAreas.includes(opt.value) ? styles.selected : ''}`}
                onClick={() => onToggleFocusArea(opt.value)}
              >
                {opt.label}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function BackgroundStep({ level, onChange }: {
  level: BackgroundLevel;
  onChange: (l: BackgroundLevel) => void;
}) {
  return (
    <div className={styles.step}>
      <h2 className={styles.stepTitle}>Tell us about your experience</h2>
      <p className={styles.stepDescription}>
        This helps us recommend the right starting point for you.
      </p>

      <div className={styles.formGrid}>
        <div className={styles.formGroup}>
          <label>Programming Experience</label>
          <div className={styles.optionGroupVertical}>
            {([
              { value: 'none', label: 'None', desc: 'New to programming' },
              { value: 'beginner', label: 'Beginner', desc: 'Basic Python/JS knowledge' },
              { value: 'intermediate', label: 'Intermediate', desc: 'Built projects before' },
              { value: 'advanced', label: 'Advanced', desc: 'Professional experience' },
            ] as const).map(opt => (
              <button
                key={opt.value}
                className={`${styles.optionCard} ${level.programmingExperience === opt.value ? styles.selected : ''}`}
                onClick={() => onChange({ ...level, programmingExperience: opt.value })}
              >
                <span className={styles.optionCardLabel}>{opt.label}</span>
                <span className={styles.optionCardDesc}>{opt.desc}</span>
              </button>
            ))}
          </div>
        </div>

        <div className={styles.formGroup}>
          <label>Robotics Experience</label>
          <div className={styles.optionGroupVertical}>
            {([
              { value: 'none', label: 'None', desc: 'First time with robotics' },
              { value: 'hobbyist', label: 'Hobbyist', desc: 'Arduino/Raspberry Pi projects' },
              { value: 'academic', label: 'Academic', desc: 'Coursework or research' },
              { value: 'professional', label: 'Professional', desc: 'Industry experience' },
            ] as const).map(opt => (
              <button
                key={opt.value}
                className={`${styles.optionCard} ${level.roboticsExperience === opt.value ? styles.selected : ''}`}
                onClick={() => onChange({ ...level, roboticsExperience: opt.value })}
              >
                <span className={styles.optionCardLabel}>{opt.label}</span>
                <span className={styles.optionCardDesc}>{opt.desc}</span>
              </button>
            ))}
          </div>
        </div>

        <div className={styles.formGroup}>
          <label>Math Background</label>
          <div className={styles.optionGroup}>
            {(['basic', 'calculus', 'linear-algebra', 'advanced'] as const).map(opt => (
              <button
                key={opt}
                className={`${styles.optionButton} ${level.mathBackground === opt ? styles.selected : ''}`}
                onClick={() => onChange({ ...level, mathBackground: opt })}
              >
                {opt === 'basic' && 'Basic'}
                {opt === 'calculus' && 'Calculus'}
                {opt === 'linear-algebra' && 'Linear Algebra'}
                {opt === 'advanced' && 'Advanced'}
              </button>
            ))}
          </div>
        </div>

        <div className={styles.formGroup}>
          <label>Linux Familiarity</label>
          <div className={styles.optionGroup}>
            {(['none', 'basic', 'comfortable', 'expert'] as const).map(opt => (
              <button
                key={opt}
                className={`${styles.optionButton} ${level.linuxFamiliarity === opt ? styles.selected : ''}`}
                onClick={() => onChange({ ...level, linuxFamiliarity: opt })}
              >
                {opt.charAt(0).toUpperCase() + opt.slice(1)}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function CompleteStep({ systemPrefs, learningPrefs, backgroundLevel }: {
  systemPrefs: SystemPreferences;
  learningPrefs: LearningPreferences;
  backgroundLevel: BackgroundLevel;
}) {
  // Determine recommended starting point
  const getRecommendation = () => {
    if (backgroundLevel.programmingExperience === 'none') {
      return {
        stage: 'Stage 1: Foundations',
        message: "We'll start with programming basics before diving into robotics.",
      };
    }
    if (backgroundLevel.roboticsExperience === 'none' || backgroundLevel.roboticsExperience === 'hobbyist') {
      return {
        stage: 'Stage 1: Foundations',
        message: "Let's build a strong foundation in robotics concepts first.",
      };
    }
    if (backgroundLevel.linuxFamiliarity === 'none' || backgroundLevel.linuxFamiliarity === 'basic') {
      return {
        stage: 'Stage 1: Foundations',
        message: 'We recommend starting with Linux basics for ROS 2 development.',
      };
    }
    return {
      stage: 'Stage 2: ROS & Simulation',
      message: "You have a solid background! Let's jump into ROS 2.",
    };
  };

  const recommendation = getRecommendation();

  return (
    <div className={styles.step}>
      <div className={styles.completeIcon}>
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
          <polyline points="22 4 12 14.01 9 11.01"/>
        </svg>
      </div>
      <h2 className={styles.stepTitle}>You're all set!</h2>
      <p className={styles.stepDescription}>
        Based on your profile, we recommend starting with:
      </p>

      <div className={styles.recommendationCard}>
        <h3>{recommendation.stage}</h3>
        <p>{recommendation.message}</p>
      </div>

      <div className={styles.summaryGrid}>
        <div className={styles.summaryItem}>
          <span className={styles.summaryLabel}>Environment</span>
          <span className={styles.summaryValue}>{systemPrefs.os} / {systemPrefs.preferredIde}</span>
        </div>
        <div className={styles.summaryItem}>
          <span className={styles.summaryLabel}>Learning Style</span>
          <span className={styles.summaryValue}>{learningPrefs.learningStyle}</span>
        </div>
        <div className={styles.summaryItem}>
          <span className={styles.summaryLabel}>Pace</span>
          <span className={styles.summaryValue}>{learningPrefs.pacePreference}</span>
        </div>
        <div className={styles.summaryItem}>
          <span className={styles.summaryLabel}>Experience</span>
          <span className={styles.summaryValue}>{backgroundLevel.programmingExperience} programming</span>
        </div>
      </div>
    </div>
  );
}
