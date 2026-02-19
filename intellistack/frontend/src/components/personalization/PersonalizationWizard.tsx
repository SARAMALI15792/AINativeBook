'use client';

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui';
import { LearningGoalSelector } from './LearningGoalSelector';
import { ExperienceLevelSelector } from './ExperienceLevelSelector';
import { WeeklyCommitmentSlider } from './WeeklyCommitmentSlider';
import { InterestTagSelector } from './InterestTagSelector';
import type { PersonalizationPreferences, LearningGoal, ExperienceLevel } from '@/types/api';

interface PersonalizationWizardProps {
  onComplete: (preferences: PersonalizationPreferences) => void;
  onSkip?: () => void;
  className?: string;
}

interface WizardStep {
  id: number;
  title: string;
  component: React.ReactNode;
  isValid: boolean;
}

export function PersonalizationWizard({ onComplete, onSkip, className = '' }: PersonalizationWizardProps) {
  const [currentStep, setCurrentStep] = useState(1);
  const [learningGoal, setLearningGoal] = useState<LearningGoal | undefined>();
  const [experienceLevel, setExperienceLevel] = useState<ExperienceLevel | undefined>();
  const [weeklyCommitment, setWeeklyCommitment] = useState(5);
  const [interests, setInterests] = useState<string[]>([]);
  const [showSkipModal, setShowSkipModal] = useState(false);

  const totalSteps = 4;

  // Load from sessionStorage on mount
  useEffect(() => {
    const saved = sessionStorage.getItem('personalization_progress');
    if (saved) {
      try {
        const data = JSON.parse(saved);
        setCurrentStep(data.currentStep || 1);
        setLearningGoal(data.learningGoal);
        setExperienceLevel(data.experienceLevel);
        setWeeklyCommitment(data.weeklyCommitment || 5);
        setInterests(data.interests || []);
      } catch (error) {
        console.error('Failed to load saved progress:', error);
      }
    }
  }, []);

  // Save to sessionStorage on change
  useEffect(() => {
    const data = {
      currentStep,
      learningGoal,
      experienceLevel,
      weeklyCommitment,
      interests,
    };
    sessionStorage.setItem('personalization_progress', JSON.stringify(data));
  }, [currentStep, learningGoal, experienceLevel, weeklyCommitment, interests]);

  const steps: WizardStep[] = [
    {
      id: 1,
      title: 'Learning Goal',
      component: <LearningGoalSelector value={learningGoal} onChange={setLearningGoal} />,
      isValid: !!learningGoal,
    },
    {
      id: 2,
      title: 'Experience Level',
      component: <ExperienceLevelSelector value={experienceLevel} onChange={setExperienceLevel} />,
      isValid: !!experienceLevel,
    },
    {
      id: 3,
      title: 'Time Commitment',
      component: <WeeklyCommitmentSlider value={weeklyCommitment} onChange={setWeeklyCommitment} />,
      isValid: weeklyCommitment >= 1 && weeklyCommitment <= 20,
    },
    {
      id: 4,
      title: 'Interests',
      component: <InterestTagSelector value={interests} onChange={setInterests} />,
      isValid: interests.length > 0,
    },
  ];

  const currentStepData = steps[currentStep - 1];
  const canGoNext = currentStepData.isValid;
  const canGoPrevious = currentStep > 1;
  const isLastStep = currentStep === totalSteps;

  const handleNext = () => {
    if (canGoNext && !isLastStep) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handlePrevious = () => {
    if (canGoPrevious) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleComplete = () => {
    if (!learningGoal || !experienceLevel) return;

    const preferences: PersonalizationPreferences = {
      userId: '', // Will be set by the API
      learningGoal,
      experienceLevel,
      weeklyCommitment,
      interests,
      preferredLanguage: 'en',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    // Clear saved progress
    sessionStorage.removeItem('personalization_progress');

    onComplete(preferences);
  };

  const handleSkipConfirm = () => {
    sessionStorage.removeItem('personalization_progress');
    onSkip?.();
  };

  return (
    <div className={`max-w-4xl mx-auto ${className}`} role="region" aria-label="Personalization wizard">
      {/* Progress Bar */}
      <div className="mb-8 space-y-4" role="progressbar" aria-valuenow={currentStep} aria-valuemin={1} aria-valuemax={totalSteps} aria-label={`Step ${currentStep} of ${totalSteps}: ${currentStepData.title}`}>
        <div className="flex items-center justify-between text-sm">
          <span className="text-text-tertiary">Step {currentStep} of {totalSteps}</span>
          <span className="text-text-secondary font-medium">{currentStepData.title}</span>
        </div>
        <div className="h-2 bg-glass-highlight rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-accent-cyan to-accent-violet transition-all duration-normal"
            style={{ width: `${(currentStep / totalSteps) * 100}%` }}
            aria-hidden="true"
          />
        </div>
      </div>

      {/* Step Indicators */}
      <div className="flex items-center justify-center mb-8 space-x-2">
        {steps.map((step) => (
          <div
            key={step.id}
            className={`flex items-center ${step.id < totalSteps ? 'flex-1' : ''}`}
          >
            <div
              className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold transition-all ${
                step.id < currentStep
                  ? 'bg-gradient-to-br from-accent-cyan to-accent-violet text-white'
                  : step.id === currentStep
                  ? 'bg-gradient-to-br from-accent-cyan to-accent-violet text-white shadow-glow-cyan'
                  : 'bg-glass-highlight text-text-tertiary'
              }`}
            >
              {step.id < currentStep ? (
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fillRule="evenodd"
                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                    clipRule="evenodd"
                  />
                </svg>
              ) : (
                step.id
              )}
            </div>
            {step.id < totalSteps && (
              <div
                className={`flex-1 h-1 mx-2 rounded-full transition-all ${
                  step.id < currentStep ? 'bg-gradient-to-r from-accent-cyan to-accent-violet' : 'bg-glass-highlight'
                }`}
              />
            )}
          </div>
        ))}
      </div>

      {/* Wizard Card Container */}
      <div className="glass backdrop-blur-md rounded-2xl border-2 border-glass-border shadow-2xl overflow-hidden">
        {/* Step Content Card */}
        <div className="p-8 min-h-[400px] animate-fade-in">
          {currentStepData.component}
        </div>

        {/* Navigation Footer Box */}
        <div className="glass backdrop-blur-md border-t-2 border-glass-border p-6">
          <div className="flex items-center justify-between">
            <div>
              {canGoPrevious && (
                <Button variant="ghost" size="md" onClick={handlePrevious} className="px-6 py-3">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                  </svg>
                  Previous
                </Button>
              )}
            </div>

            <div className="flex items-center space-x-4">
              <Button variant="ghost" size="md" onClick={() => setShowSkipModal(true)} className="px-6 py-3">
                Skip for now
              </Button>

              {!isLastStep ? (
                <Button
                  variant="primary"
                  size="lg"
                  onClick={handleNext}
                  disabled={!canGoNext}
                  className="px-8 py-4 text-lg bg-gradient-to-r from-accent-cyan to-accent-violet hover:shadow-glow-cyan hover:scale-105 transition-all duration-normal"
                >
                  Next
                  <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </Button>
              ) : (
                <Button
                  variant="primary"
                  size="lg"
                  onClick={handleComplete}
                  disabled={!canGoNext}
                  className="px-8 py-4 text-lg bg-gradient-to-r from-accent-cyan to-accent-violet hover:shadow-glow-cyan hover:scale-105 transition-all duration-normal"
                >
                  Complete Setup
                  <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </Button>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Skip Confirmation Modal */}
      {showSkipModal && (
        <div className="fixed inset-0 z-modal flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={() => setShowSkipModal(false)} />
          <div className="relative glass backdrop-blur-md rounded-xl p-8 max-w-md w-full border border-glass-border shadow-xl animate-fade-in-up">
            <h3 className="text-2xl font-bold text-text-primary mb-4">Skip personalization?</h3>
            <p className="text-text-secondary mb-6">
              You can always personalize your learning experience later from your profile settings. However, we recommend completing this now for the best experience.
            </p>
            <div className="flex items-center space-x-4">
              <Button variant="ghost" size="lg" fullWidth onClick={() => setShowSkipModal(false)}>
                Continue Setup
              </Button>
              <Button variant="outline" size="lg" fullWidth onClick={handleSkipConfirm}>
                Skip
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
