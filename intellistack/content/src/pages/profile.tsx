/**
 * User Profile Page
 * View and edit user profile settings
 */

import React, { useState, useEffect } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import { useHistory } from '@docusaurus/router';
import styles from './auth.module.css';

interface UserProfile {
  id: string;
  name: string;
  email: string;
  role: string;
  emailVerified: boolean;
  image?: string;
}

interface BackendProfile {
  id: string;
  email: string;
  name: string;
  role: string;
  email_verified: boolean;
  preferences?: {
    theme?: string;
    notifications?: boolean;
  };
  current_stage: number;
}

export default function ProfilePage(): JSX.Element {
  const history = useHistory();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [backendProfile, setBackendProfile] = useState<BackendProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [authClient, setAuthClient] = useState<any>(null);

  const [backendUrl, setBackendUrl] = useState<string>('');

  useEffect(() => {
    import('@site/src/lib/auth-client.tsx').then(async (mod) => {
      setAuthClient(mod.authClient);
      setBackendUrl(mod.getBackendUrl());
      try {
        const result = await mod.authClient.getSession();
        if (result.data?.user) {
          // Create a proper UserProfile from the auth result
          setProfile({
            id: result.data.user.id,
            name: result.data.user.name || '',
            email: result.data.user.email || '',
            role: result.data.user.role || 'student',
            emailVerified: result.data.user.emailVerified || false,
            image: result.data.user.image,
          });

          // Get JWT for backend API calls
          const jwt = await mod.getJwtToken();
          if (jwt) {
            fetch(`${mod.getBackendUrl()}/api/v1/users/me`, {
              headers: {
                'Authorization': `Bearer ${jwt}`,
                'Content-Type': 'application/json',
              },
            })
              .then(res => res.json())
              .then(data => setBackendProfile(data))
              .catch(err => console.error('Failed to fetch backend profile:', err))
              .finally(() => setIsLoading(false));
          } else {
            setIsLoading(false);
          }
        } else {
          history.push('/login');
          setIsLoading(false);
        }
      } catch {
        history.push('/login');
        setIsLoading(false);
      }
    });
  }, []);

  // Get stage name from stage number
  const getStageName = (stage: number): string => {
    const stageNames: Record<number, string> = {
      1: 'Foundations',
      2: 'ROS 2 & Simulation',
      3: 'Perception & Planning',
      4: 'AI Integration',
      5: 'Capstone',
    };
    return stageNames[stage] || 'Unknown';
  };

  const handleSignOut = async () => {
    if (!authClient) return;
    try {
      await authClient.signOut();
      history.push('/');
    } catch (error) {
      console.error('Sign out failed:', error);
    }
  };

  if (isLoading) {
    return (
      <Layout title="Profile" description="Your profile">
        <div className={styles.authContainer}>
          <div className={styles.authCard}>
            <div style={{ textAlign: 'center', padding: '2rem' }}>
              <span className={styles.spinner} style={{ display: 'inline-block' }} />
              <p style={{ marginTop: '1rem', color: 'var(--ifm-color-emphasis-600)' }}>Loading...</p>
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  if (!profile) {
    return (
      <Layout title="Profile" description="Your profile">
        <div className={styles.authContainer}>
          <div className={styles.authCard}>
            <p style={{ textAlign: 'center' }}>Please sign in to view your profile.</p>
            <Link to="/login" className={styles.submitButton} style={{ display: 'block', textAlign: 'center', textDecoration: 'none', marginTop: '1rem' }}>
              Sign In
            </Link>
          </div>
        </div>
      </Layout>
    );
  }

  const initials = profile.name
    ? profile.name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
    : profile.email[0].toUpperCase();

  return (
    <Layout title="Profile" description="Your profile">
      <div className={styles.authContainer}>
        <div className={styles.authCard} style={{ maxWidth: '500px' }}>
          {/* Profile Header */}
          <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
            {profile.image ? (
              <img
                src={profile.image}
                alt={profile.name || 'Profile'}
                style={{
                  width: '80px',
                  height: '80px',
                  borderRadius: '50%',
                  objectFit: 'cover',
                  marginBottom: '1rem',
                }}
              />
            ) : (
              <div
                style={{
                  width: '80px',
                  height: '80px',
                  borderRadius: '50%',
                  background: 'linear-gradient(135deg, var(--ifm-color-primary) 0%, var(--ifm-color-primary-dark) 100%)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto 1rem',
                  fontSize: '1.5rem',
                  fontWeight: '600',
                  color: '#ffffff',
                }}
              >
                {initials}
              </div>
            )}
            <h1 style={{ fontSize: '1.5rem', margin: '0 0 0.5rem' }}>{profile.name || 'User'}</h1>
            <p style={{ color: 'var(--ifm-color-emphasis-600)', margin: 0 }}>{profile.email}</p>
          </div>

          {/* Profile Info */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginBottom: '2rem' }}>
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              padding: '1rem',
              background: 'var(--ifm-color-emphasis-100)',
              borderRadius: '8px',
            }}>
              <span style={{ fontWeight: '500' }}>Role</span>
              <span style={{
                padding: '0.25rem 0.75rem',
                background: 'var(--ifm-color-primary)',
                color: '#ffffff',
                borderRadius: '9999px',
                fontSize: '0.8125rem',
                fontWeight: '500',
                textTransform: 'capitalize',
              }}>
                {profile.role || 'Student'}
              </span>
            </div>

            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              padding: '1rem',
              background: 'var(--ifm-color-emphasis-100)',
              borderRadius: '8px',
            }}>
              <span style={{ fontWeight: '500' }}>Email Verified</span>
              {profile.emailVerified ? (
                <span style={{ color: '#22c55e', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polyline points="20 6 9 17 4 12"/>
                  </svg>
                  Verified
                </span>
              ) : (
                <span style={{ color: '#eab308', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="12" y1="8" x2="12" y2="12"/>
                    <line x1="12" y1="16" x2="12.01" y2="16"/>
                  </svg>
                  Pending
                </span>
              )}
            </div>

            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              padding: '1rem',
              background: 'var(--ifm-color-emphasis-100)',
              borderRadius: '8px',
            }}>
              <span style={{ fontWeight: '500' }}>Learning Stage</span>
              <span style={{
                padding: '0.25rem 0.75rem',
                background: 'var(--ifm-color-primary)',
                color: '#ffffff',
                borderRadius: '9999px',
                fontSize: '0.8125rem',
                fontWeight: '500',
              }}>
                {backendProfile?.current_stage || 1} - {getStageName(backendProfile?.current_stage || 1)}
              </span>
            </div>

            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              padding: '1rem',
              background: 'var(--ifm-color-emphasis-100)',
              borderRadius: '8px',
            }}>
              <span style={{ fontWeight: '500' }}>Onboarding</span>
              {backendProfile?.preferences ? (
                <span style={{ color: '#22c55e' }}>Complete</span>
              ) : (
                <Link to="/onboarding" style={{ color: 'var(--ifm-color-primary)', textDecoration: 'none' }}>
                  Complete Setup
                </Link>
              )}
            </div>
          </div>

          {/* Actions */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            <Link
              to="/onboarding"
              style={{
                display: 'block',
                padding: '0.75rem 1rem',
                textAlign: 'center',
                background: 'var(--ifm-color-emphasis-100)',
                border: '1px solid var(--ifm-color-emphasis-300)',
                borderRadius: '8px',
                color: 'var(--ifm-font-color-base)',
                textDecoration: 'none',
                fontWeight: '500',
              }}
            >
              Update Preferences
            </Link>

            <button
              onClick={handleSignOut}
              style={{
                padding: '0.75rem 1rem',
                background: 'transparent',
                border: '1px solid #dc2626',
                borderRadius: '8px',
                color: '#dc2626',
                cursor: 'pointer',
                fontWeight: '500',
                fontSize: '0.9375rem',
              }}
            >
              Sign Out
            </button>
          </div>
        </div>
      </div>
    </Layout>
  );
}
