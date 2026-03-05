import React from 'react';

interface StepIndicatorProps {
  currentStep: number;
}

export default function StepIndicator({ currentStep }: StepIndicatorProps) {
  const steps = [
    { number: 1, label: 'Basic Information' },
    { number: 2, label: 'Educational Background' },
    { number: 3, label: 'Academic Interests' },
    { number: 4, label: 'Additional Details' },
  ];

  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      marginBottom: '3rem',
      gap: '1rem',
    }}>
      {steps.map((step, index) => (
        <React.Fragment key={step.number}>
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: '0.5rem',
          }}>
            <div style={{
              width: '40px',
              height: '40px',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontWeight: 'bold',
              backgroundColor: step.number === currentStep
                ? 'var(--ifm-color-primary)'
                : step.number < currentStep
                  ? 'var(--ifm-color-success)'
                  : 'var(--ifm-color-emphasis-300)',
              color: step.number <= currentStep ? 'white' : 'var(--ifm-color-emphasis-600)',
              transition: 'all 0.3s ease',
            }}>
              {step.number < currentStep ? '✓' : step.number}
            </div>
            <span style={{
              fontSize: '0.875rem',
              color: step.number === currentStep
                ? 'var(--ifm-color-primary)'
                : 'var(--ifm-color-emphasis-600)',
              fontWeight: step.number === currentStep ? 'bold' : 'normal',
              textAlign: 'center',
              maxWidth: '120px',
            }}>
              {step.label}
            </span>
          </div>
          {index < steps.length - 1 && (
            <div style={{
              width: '60px',
              height: '2px',
              backgroundColor: step.number < currentStep
                ? 'var(--ifm-color-success)'
                : 'var(--ifm-color-emphasis-300)',
              marginBottom: '2rem',
              transition: 'all 0.3s ease',
            }} />
          )}
        </React.Fragment>
      ))}
    </div>
  );
}
