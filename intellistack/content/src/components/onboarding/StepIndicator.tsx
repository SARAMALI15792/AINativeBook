import React from 'react';

interface StepIndicatorProps {
  currentStep: number;
  totalSteps?: number;
}

export default function StepIndicator({ currentStep, totalSteps = 4 }: StepIndicatorProps) {
  const progress = (currentStep / totalSteps) * 100;

  return (
    <>
      {/* Thin progress bar at top of card */}
      <div className="onboarding-progress-bar-track">
        <div
          className="onboarding-progress-bar-fill"
          style={{ width: `${progress}%` }}
          role="progressbar"
          aria-valuenow={currentStep}
          aria-valuemin={1}
          aria-valuemax={totalSteps}
        />
      </div>

      {/* Step counter row: label left, dot indicators right */}
      <div className="onboarding-step-counter" aria-label={`Step ${currentStep} of ${totalSteps}`}>
        <span>Step {currentStep} of {totalSteps}</span>
        <div className="onboarding-step-dots">
          {Array.from({ length: totalSteps }).map((_, i) => (
            <div
              key={i}
              className={`onboarding-step-dot ${
                i + 1 === currentStep ? 'active' : i + 1 < currentStep ? 'done' : ''
              }`}
            />
          ))}
        </div>
      </div>
    </>
  );
}
