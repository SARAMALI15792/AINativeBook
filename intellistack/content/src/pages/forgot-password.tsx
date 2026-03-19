/**
 * Forgot Password Page
 * Request password reset via email
 */

import React, { useState, useEffect } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import styles from './auth.module.css';

export default function ForgotPasswordPage(): JSX.Element {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [authClient, setAuthClient] = useState<any>(null);

  useEffect(() => {
    import('../lib/auth-client').then((mod) => {
      setAuthClient(mod.authClient);
    });
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!authClient) return;

    setError(null);
    setIsLoading(true);

    try {
      await authClient.forgetPassword({
        email,
        redirectTo: window.location.origin + '/reset-password',
      });
      setIsSubmitted(true);
    } catch (err: any) {
      // Always show success to prevent email enumeration
      setIsSubmitted(true);
    } finally {
      setIsLoading(false);
    }
  };

  if (isSubmitted) {
    return (
      <Layout title="Check Your Email" description="Password reset instructions sent">
        <div className={styles.authContainer}>
          <div className={styles.authCard}>
            <div className={styles.successIcon}>
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="2" y="4" width="20" height="16" rx="2"/>
                <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
              </svg>
            </div>
            <h1 className={styles.authTitle}>Check Your Email</h1>
            <p className={styles.successMessage}>
              If an account exists for <strong>{email}</strong>, we've sent password reset instructions.
            </p>
            <p className={styles.successHint}>
              Didn't receive it? Check your spam folder or wait a few minutes and try again.
            </p>
            <Link to="/login" className={styles.submitButton} style={{ marginTop: '1.5rem', display: 'block', textAlign: 'center', textDecoration: 'none' }}>
              Back to Sign In
            </Link>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout title="Forgot Password" description="Reset your password">
      <div className={styles.authContainer}>
        <div className={styles.authCard}>
          <div className={styles.authHeader}>
            <h1 className={styles.authTitle}>Forgot Password?</h1>
            <p className={styles.authSubtitle}>
              No worries, we'll send you reset instructions.
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

          <form onSubmit={handleSubmit} className={styles.authForm}>
            <div className={styles.formGroup}>
              <label htmlFor="email" className={styles.label}>Email</label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className={styles.input}
                placeholder="you@example.com"
                required
                autoComplete="email"
                disabled={isLoading}
              />
            </div>

            <button
              type="submit"
              className={styles.submitButton}
              disabled={isLoading}
            >
              {isLoading ? (
                <span className={styles.spinner} />
              ) : (
                'Send Reset Instructions'
              )}
            </button>
          </form>

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
