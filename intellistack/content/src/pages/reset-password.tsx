/**
 * Reset Password Page
 * Set new password using reset token
 */

import React, { useState, useEffect } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import { useLocation, useHistory } from '@docusaurus/router';
import styles from './auth.module.css';

// Password strength calculation (same as register page)
function calculatePasswordStrength(password: string): {
  score: number;
  label: string;
  color: string;
  feedback: string[];
} {
  const feedback: string[] = [];
  let score = 0;

  if (password.length >= 12) score += 25;
  else feedback.push('At least 12 characters');

  if (/[a-z]/.test(password)) score += 20;
  else feedback.push('Include lowercase letter');

  if (/[A-Z]/.test(password)) score += 20;
  else feedback.push('Include uppercase letter');

  if (/[0-9]/.test(password)) score += 20;
  else feedback.push('Include a number');

  if (/[^a-zA-Z0-9]/.test(password)) score += 15;
  else feedback.push('Include special character');

  let label = 'Weak';
  let color = '#ef4444';

  if (score >= 80) {
    label = 'Strong';
    color = '#22c55e';
  } else if (score >= 60) {
    label = 'Good';
    color = '#84cc16';
  } else if (score >= 40) {
    label = 'Fair';
    color = '#eab308';
  }

  return { score, label, color, feedback };
}

export default function ResetPasswordPage(): JSX.Element {
  const location = useLocation();
  const history = useHistory();
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showPassword, setShowPassword] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [authClient, setAuthClient] = useState<any>(null);

  const passwordStrength = calculatePasswordStrength(password);

  // Extract token from URL
  const params = new URLSearchParams(location.search);
  const token = params.get('token');

  useEffect(() => {
    import('@site/src/lib/auth-client.ts').then((mod) => {
      setAuthClient(mod.authClient);
    });

    if (!token) {
      setError('Invalid or missing reset token. Please request a new password reset.');
    }
  }, [token]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!authClient || !token) return;

    setError(null);

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (passwordStrength.score < 80) {
      setError('Please create a stronger password: ' + passwordStrength.feedback.join(', '));
      return;
    }

    setIsLoading(true);

    try {
      await authClient.resetPassword({
        token,
        newPassword: password,
      });
      setIsSuccess(true);
    } catch (err: any) {
      if (err.message?.includes('expired')) {
        setError('This reset link has expired. Please request a new one.');
      } else {
        setError(err.message || 'Failed to reset password');
      }
    } finally {
      setIsLoading(false);
    }
  };

  if (isSuccess) {
    return (
      <Layout title="Password Reset" description="Password reset successful">
        <div className={styles.authContainer}>
          <div className={styles.authCard}>
            <div className={styles.successIcon}>
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                <polyline points="22 4 12 14.01 9 11.01"/>
              </svg>
            </div>
            <h1 className={styles.authTitle}>Password Reset!</h1>
            <p className={styles.successMessage}>
              Your password has been successfully reset. You can now sign in with your new password.
            </p>
            <Link to="/login" className={styles.submitButton} style={{ marginTop: '1.5rem', display: 'block', textAlign: 'center', textDecoration: 'none' }}>
              Sign In
            </Link>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout title="Reset Password" description="Set your new password">
      <div className={styles.authContainer}>
        <div className={styles.authCard}>
          <div className={styles.authHeader}>
            <h1 className={styles.authTitle}>Set New Password</h1>
            <p className={styles.authSubtitle}>
              Create a strong password for your account.
            </p>
          </div>

          {error && (
            <div className={styles.errorAlert}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="8" x2="12" y2="12"/>
                <line x1="12" y1="16" x2="12.01" y2="16"/>
              </svg>
              <span>{error}</span>
            </div>
          )}

          {!token ? (
            <div>
              <p style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
                The reset link is invalid or has expired.
              </p>
              <Link to="/forgot-password" className={styles.submitButton} style={{ display: 'block', textAlign: 'center', textDecoration: 'none' }}>
                Request New Reset Link
              </Link>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className={styles.authForm}>
              <div className={styles.formGroup}>
                <label htmlFor="password" className={styles.label}>New Password</label>
                <div className={styles.passwordWrapper}>
                  <input
                    id="password"
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className={styles.input}
                    placeholder="Create a strong password"
                    required
                    autoComplete="new-password"
                    disabled={isLoading}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className={styles.passwordToggle}
                    tabIndex={-1}
                  >
                    {showPassword ? (
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24"/>
                        <line x1="1" y1="1" x2="23" y2="23"/>
                      </svg>
                    ) : (
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                        <circle cx="12" cy="12" r="3"/>
                      </svg>
                    )}
                  </button>
                </div>

                {password && (
                  <div className={styles.passwordStrength}>
                    <div className={styles.strengthBar}>
                      <div
                        className={styles.strengthFill}
                        style={{
                          width: `${passwordStrength.score}%`,
                          backgroundColor: passwordStrength.color,
                        }}
                      />
                    </div>
                    <span className={styles.strengthLabel} style={{ color: passwordStrength.color }}>
                      {passwordStrength.label}
                    </span>
                  </div>
                )}

                {password && passwordStrength.feedback.length > 0 && (
                  <ul className={styles.passwordFeedback}>
                    {passwordStrength.feedback.map((item, i) => (
                      <li key={i}>{item}</li>
                    ))}
                  </ul>
                )}
              </div>

              <div className={styles.formGroup}>
                <label htmlFor="confirmPassword" className={styles.label}>Confirm Password</label>
                <input
                  id="confirmPassword"
                  type={showPassword ? 'text' : 'password'}
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className={styles.input}
                  placeholder="Confirm your password"
                  required
                  autoComplete="new-password"
                  disabled={isLoading}
                />
                {confirmPassword && password !== confirmPassword && (
                  <span className={styles.fieldError}>Passwords do not match</span>
                )}
              </div>

              <button
                type="submit"
                className={styles.submitButton}
                disabled={isLoading || passwordStrength.score < 80}
              >
                {isLoading ? (
                  <span className={styles.spinner} />
                ) : (
                  'Reset Password'
                )}
              </button>
            </form>
          )}

          <p className={styles.authFooter}>
            Remember your password?{' '}
            <Link to="/login" className={styles.authLink}>
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </Layout>
  );
}
