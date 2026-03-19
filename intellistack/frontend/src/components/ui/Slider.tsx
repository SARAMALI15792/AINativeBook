'use client';

import React from 'react';

interface SliderProps {
  value: number;
  onChange: (value: number) => void;
  min: number;
  max: number;
  step?: number;
  label?: string;
  showValue?: boolean;
  marks?: { value: number; label: string }[];
  disabled?: boolean;
  className?: string;
  'aria-label'?: string;
}

export function Slider({
  value,
  onChange,
  min,
  max,
  step = 1,
  label,
  showValue = false,
  marks = [],
  disabled = false,
  className = '',
  'aria-label': ariaLabel,
}: SliderProps) {
  const sliderId = React.useId();
  const percentage = ((value - min) / (max - min)) * 100;

  return (
    <div className={`w-full ${className}`}>
      {label && (
        <label htmlFor={sliderId} className="block text-sm font-medium text-text-secondary mb-2">
          {label}
          {showValue && <span className="ml-2 text-accent-cyan font-semibold">{value}</span>}
        </label>
      )}
      <div className="relative pt-1">
        <input
          id={sliderId}
          type="range"
          min={min}
          max={max}
          step={step}
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
          disabled={disabled}
          aria-label={ariaLabel || label}
          aria-valuemin={min}
          aria-valuemax={max}
          aria-valuenow={value}
          className="w-full h-2 bg-bg-tertiary rounded-lg appearance-none cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-accent-cyan"
          style={{
            background: `linear-gradient(to right, var(--color-accent-cyan) 0%, var(--color-accent-cyan) ${percentage}%, var(--color-bg-tertiary) ${percentage}%, var(--color-bg-tertiary) 100%)`,
          }}
        />
        {marks.length > 0 && (
          <div className="flex justify-between mt-2">
            {marks.map((mark) => (
              <span
                key={mark.value}
                className="text-xs text-text-tertiary"
                style={{
                  position: 'absolute',
                  left: `${((mark.value - min) / (max - min)) * 100}%`,
                  transform: 'translateX(-50%)',
                }}
              >
                {mark.label}
              </span>
            ))}
          </div>
        )}
      </div>
      <style jsx>{`
        input[type='range']::-webkit-slider-thumb {
          appearance: none;
          width: 20px;
          height: 20px;
          border-radius: 50%;
          background: var(--color-accent-cyan);
          cursor: pointer;
          box-shadow: 0 0 10px rgba(0, 239, 255, 0.5);
          transition: all 0.2s ease;
        }

        input[type='range']::-webkit-slider-thumb:hover {
          transform: scale(1.2);
          box-shadow: 0 0 20px rgba(0, 239, 255, 0.8);
        }

        input[type='range']::-moz-range-thumb {
          width: 20px;
          height: 20px;
          border-radius: 50%;
          background: var(--color-accent-cyan);
          cursor: pointer;
          border: none;
          box-shadow: 0 0 10px rgba(0, 239, 255, 0.5);
          transition: all 0.2s ease;
        }

        input[type='range']::-moz-range-thumb:hover {
          transform: scale(1.2);
          box-shadow: 0 0 20px rgba(0, 239, 255, 0.8);
        }
      `}</style>
    </div>
  );
}
