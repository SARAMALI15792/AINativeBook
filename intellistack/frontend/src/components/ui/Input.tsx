'use client';

import React, { forwardRef } from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  type?: 'text' | 'email' | 'password' | 'number';
  label?: string;
  error?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  'aria-label'?: string;
  'aria-describedby'?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      type = 'text',
      value,
      onChange,
      placeholder,
      label,
      error,
      disabled = false,
      required = false,
      leftIcon,
      rightIcon,
      className = '',
      'aria-label': ariaLabel,
      'aria-describedby': ariaDescribedBy,
      ...rest
    },
    ref
  ) => {
    const inputId = React.useId();
    const errorId = `${inputId}-error`;

    const baseStyles =
      'w-full rounded-md bg-bg-tertiary border border-glass-border text-text-primary px-4 py-2 transition-all duration-normal focus:outline-none focus:ring-2 focus:ring-accent-cyan focus:border-accent-cyan disabled:opacity-50 disabled:cursor-not-allowed';

    const errorStyles = error ? 'border-error focus:ring-error' : '';

    const paddingStyles = leftIcon ? 'pl-10' : rightIcon ? 'pr-10' : '';

    return (
      <div className={`w-full ${className}`}>
        {label && (
          <label
            htmlFor={inputId}
            className="block text-sm font-medium text-text-secondary mb-1"
          >
            {label}
            {required && <span className="text-error ml-1">*</span>}
          </label>
        )}
        <div className="relative">
          {leftIcon && (
            <div className="absolute left-3 top-1/2 -translate-y-1/2 text-text-tertiary">
              {leftIcon}
            </div>
          )}
          <input
            ref={ref}
            id={inputId}
            type={type}
            value={value}
            onChange={onChange}
            placeholder={placeholder}
            disabled={disabled}
            required={required}
            aria-label={ariaLabel || label}
            aria-describedby={error ? errorId : ariaDescribedBy}
            aria-invalid={!!error}
            className={`${baseStyles} ${errorStyles} ${paddingStyles}`}
            {...rest}
          />
          {rightIcon && (
            <div className="absolute right-3 top-1/2 -translate-y-1/2 text-text-tertiary">
              {rightIcon}
            </div>
          )}
        </div>
        {error && (
          <p id={errorId} className="mt-1 text-sm text-error" role="alert">
            {error}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';
