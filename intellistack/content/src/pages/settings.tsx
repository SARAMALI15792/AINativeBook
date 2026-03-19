/**
 * User Settings Page
 * Manage account settings and preferences
 *
 * NOTE: useColorMode must be called inside Layout (ColorModeProvider).
 * We use an inner component pattern to satisfy this requirement.
 */

import React, { useState, useEffect } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import { useHistory } from '@docusaurus/router';
import { useColorMode } from '@docusaurus/theme-common';
import styles from './auth.module.css';

// Outer component renders Layout, inner component uses hooks that need ColorModeProvider
export default function SettingsPage(): JSX.Element {
  return (
    <Layout title="Settings" description="Account settings">
      <SettingsContent />
    </Layout>
  );
}

function SettingsContent(): JSX.Element {
  const history = useHistory();
  const { colorMode, setColorMode } = useColorMode();
  const [session, setSession] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [authClient, setAuthClient] = useState<any>(null);
  const [backendUrl, setBackendUrl] = useState<string>('');

  // Settings state
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  const [emailNotifications, setEmailNotifications] = useState(true);

  useEffect(() => {
    setTheme(colorMode as 'light' | 'dark');
  }, [colorMode]);

  useEffect(() => {
    import('../lib/auth-client').then((mod) => {
      setAuthClient(mod.authClient);
      setBackendUrl(mod.getBackendUrl());

      mod.authClient.getSession().then((result) => {
        if (result.data?.user) {
          setSession(result.data);
        } else {
          history.push('/login');
        }
        setIsLoading(false);
      }).catch(() => {
        history.push('/login');
      });
    });
  }, []);

  const handleThemeChange = (newTheme: 'light' | 'dark') => {
    setTheme(newTheme);
    setColorMode(newTheme);
  };

  const handleSaveSettings = async () => {
    if (!session) return;

    setIsSaving(true);
    setMessage(null);

    try {
      // Use JWT token for backend API calls (not opaque session token)
      const mod = await import('../lib/auth-client');
      const jwt = await mod.getJwtToken();
      if (!jwt) {
        setMessage('Session expired. Please sign in again.');
        setTimeout(() => {
          history.push('/login');
        }, 2000);
        return;
      }

      const response = await fetch(`${backendUrl}/api/v1/users/preferences/onboarding`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${jwt}`,
        },
        credentials: 'include', // Include cookies for session validation
        body: JSON.stringify({
          learning_style: 'visual', // Default value
          learning_pace: 'moderate',
          preferred_language: 'en',
          adaptive_complexity: true,
          personalized_exercises: true,
          personalized_time_estimates: true,
        }),
      });

      if (response.ok) {
        setMessage('Settings saved successfully!');
      } else if (response.status === 401) {
        setMessage('Session expired. Please sign in again.');
        setTimeout(() => {
          history.push('/login');
        }, 2000);
      } else {
        const errorData = await response.json().catch(() => ({}));
        setMessage(errorData.detail || 'Failed to save settings. Please try again.');
      }
    } catch (error) {
      console.error('Save settings error:', error);
      setMessage('An error occurred. Please try again.');
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return (
      <div className={styles.authContainer}>
        <div className={styles.authCard}>
          <div style={{ textAlign: 'center', padding: '2rem' }}>
            <span className={styles.spinner} style={{ display: 'inline-block' }} />
            <p style={{ marginTop: '1rem', color: 'var(--ifm-color-emphasis-600)' }}>Loading...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.authContainer}>
      <div className={styles.authCard} style={{ maxWidth: '550px' }}>
        <h1 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>Settings</h1>
        <p style={{ color: 'var(--ifm-color-emphasis-600)', marginBottom: '2rem' }}>
          Manage your account preferences
        </p>

        {message && (
          <div style={{
            padding: '0.75rem 1rem',
            marginBottom: '1.5rem',
            borderRadius: '8px',
            background: message.includes('success')
              ? 'rgba(34, 197, 94, 0.1)'
              : 'rgba(239, 68, 68, 0.1)',
            color: message.includes('success') ? '#22c55e' : '#dc2626',
            fontSize: '0.875rem',
          }}>
            {message}
          </div>
        )}

        {/* Appearance Section */}
        <section style={{ marginBottom: '2rem' }}>
          <h2 style={{ fontSize: '1rem', fontWeight: '600', marginBottom: '1rem' }}>
            Appearance
          </h2>

          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <button
              onClick={() => handleThemeChange('light')}
              style={{
                flex: 1,
                padding: '1rem',
                border: `2px solid ${theme === 'light' ? 'var(--ifm-color-primary)' : 'var(--ifm-color-emphasis-300)'}`,
                borderRadius: '8px',
                background: theme === 'light' ? 'rgba(var(--ifm-color-primary-rgb), 0.1)' : 'transparent',
                cursor: 'pointer',
                display: 'flex',
                flexDirection: 'column' as const,
                alignItems: 'center',
                gap: '0.5rem',
              }}
            >
              <span style={{ fontSize: '1.5rem' }}>☀️</span>
              <span style={{ fontSize: '0.875rem', fontWeight: '500' }}>Light</span>
            </button>

            <button
              onClick={() => handleThemeChange('dark')}
              style={{
                flex: 1,
                padding: '1rem',
                border: `2px solid ${theme === 'dark' ? 'var(--ifm-color-primary)' : 'var(--ifm-color-emphasis-300)'}`,
                borderRadius: '8px',
                background: theme === 'dark' ? 'rgba(var(--ifm-color-primary-rgb), 0.1)' : 'transparent',
                cursor: 'pointer',
                display: 'flex',
                flexDirection: 'column' as const,
                alignItems: 'center',
                gap: '0.5rem',
              }}
            >
              <span style={{ fontSize: '1.5rem' }}>🌙</span>
              <span style={{ fontSize: '0.875rem', fontWeight: '500' }}>Dark</span>
            </button>
          </div>
        </section>

        {/* Notifications Section */}
        <section style={{ marginBottom: '2rem' }}>
          <h2 style={{ fontSize: '1rem', fontWeight: '600', marginBottom: '1rem' }}>
            Notifications
          </h2>

          <label style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '1rem',
            background: 'var(--ifm-color-emphasis-100)',
            borderRadius: '8px',
            cursor: 'pointer',
          }}>
            <div>
              <span style={{ fontWeight: '500', display: 'block' }}>Email Notifications</span>
              <span style={{ fontSize: '0.8125rem', color: 'var(--ifm-color-emphasis-600)' }}>
                Receive updates about your learning progress
              </span>
            </div>
            <input
              type="checkbox"
              checked={emailNotifications}
              onChange={(e) => setEmailNotifications(e.target.checked)}
              style={{
                width: '20px',
                height: '20px',
                cursor: 'pointer',
              }}
            />
          </label>
        </section>

        {/* Account Section */}
        <section style={{ marginBottom: '2rem' }}>
          <h2 style={{ fontSize: '1rem', fontWeight: '600', marginBottom: '1rem' }}>
            Account
          </h2>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            <div style={{
              padding: '1rem',
              background: 'var(--ifm-color-emphasis-100)',
              borderRadius: '8px',
            }}>
              <p style={{ fontSize: '0.875rem', color: 'var(--ifm-color-emphasis-700)', margin: 0 }}>
                To update your learning preferences, visit your account dashboard at{' '}
                <a
                  href={process.env.FRONTEND_URL || 'http://localhost:3000'}
                  style={{ color: 'var(--ifm-color-primary)', textDecoration: 'underline' }}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  IntelliStack Dashboard
                </a>
              </p>
            </div>

            <Link
              to="/profile"
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '1rem',
                background: 'var(--ifm-color-emphasis-100)',
                borderRadius: '8px',
                textDecoration: 'none',
                color: 'var(--ifm-font-color-base)',
              }}
            >
              <span>View Profile</span>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polyline points="9 18 15 12 9 6"/>
              </svg>
            </Link>
          </div>
        </section>

        {/* Save Button */}
        <button
          onClick={handleSaveSettings}
          disabled={isSaving}
          className={styles.submitButton}
          style={{ width: '100%' }}
        >
          {isSaving ? (
            <span className={styles.spinner} />
          ) : (
            'Save Settings'
          )}
        </button>

        <p style={{ textAlign: 'center', marginTop: '1.5rem' }}>
          <Link to="/profile" style={{ color: 'var(--ifm-color-emphasis-600)', fontSize: '0.875rem' }}>
            ← Back to Profile
          </Link>
        </p>
      </div>
    </div>
  );
}
