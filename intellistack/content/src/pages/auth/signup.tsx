import React, { useState } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import { useHistory } from '@docusaurus/router';
import { signUp, signInWithGoogle } from '../../lib/auth';

function SignupPageContent() {
  const history = useHistory();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (!name || !email || !password || !confirmPassword) {
        setError('All fields are required');
        setLoading(false);
        return;
      }

      if (password.length < 8) {
        setError('Password must be at least 8 characters');
        setLoading(false);
        return;
      }

      if (password !== confirmPassword) {
        setError('Passwords do not match');
        setLoading(false);
        return;
      }

      const result = await signUp(email, password, name);

      if (result.error) {
        setError(result.error.message || 'Signup failed. Please try again.');
        setLoading(false);
        return;
      }

      window.dispatchEvent(new Event('auth-state-changed'));

      const baseUrl = (window as any).docusaurus?.siteConfig?.baseUrl || '/AINativeBook/';
      window.location.href = `${baseUrl}onboarding/step-1`;
    } catch (err) {
      console.error('Signup error:', err);
      setError('An unexpected error occurred. Please try again.');
      setLoading(false);
    }
  };

  const handleGoogleSignup = async () => {
    setError('');
    setLoading(true);

    try {
      await signInWithGoogle(`${window.location.origin}/auth/callback`);
    } catch (err) {
      console.error('Google signup error:', err);
      setError('Google signup failed. Please try again.');
      setLoading(false);
    }
  };

  return (
    <Layout title="Sign Up" description="Create your IntelliStack account">
      <div className="auth-page-wrapper">
        <div className="auth-form-card">
          <h1>Sign Up</h1>

          {error && <div className="auth-error">{error}</div>}

          <form onSubmit={handleSubmit}>
            <div className="auth-field">
              <label htmlFor="name">Full Name</label>
              <input
                id="name"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="John Doe"
                disabled={loading}
                className="auth-input"
                required
              />
            </div>

            <div className="auth-field">
              <label htmlFor="email">Email</label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="your@email.com"
                disabled={loading}
                className="auth-input"
                required
              />
            </div>

            <div className="auth-field">
              <label htmlFor="password">Password</label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                disabled={loading}
                className="auth-input"
                required
              />
              <small style={{ color: 'var(--color-text-muted)', fontSize: 'var(--text-xs)' }}>
                Minimum 8 characters
              </small>
            </div>

            <div className="auth-field">
              <label htmlFor="confirmPassword">Confirm Password</label>
              <input
                id="confirmPassword"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="••••••••"
                disabled={loading}
                className="auth-input"
                required
              />
            </div>

            <button type="submit" disabled={loading} className="auth-btn-primary" style={{ marginTop: '0.5rem' }}>
              {loading ? 'Creating account...' : 'Sign Up'}
            </button>
          </form>

          <div className="auth-divider">or</div>

          <button onClick={handleGoogleSignup} disabled={loading} className="auth-btn-google">
            <svg width="18" height="18" viewBox="0 0 18 18">
              <path fill="#4285F4" d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.874 2.684-6.615z"/>
              <path fill="#34A853" d="M9 18c2.43 0 4.467-.806 5.956-2.184l-2.908-2.258c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332C2.438 15.983 5.482 18 9 18z"/>
              <path fill="#FBBC05" d="M3.964 10.707c-.18-.54-.282-1.117-.282-1.707 0-.593.102-1.17.282-1.709V4.958H.957C.347 6.173 0 7.548 0 9c0 1.452.348 2.827.957 4.042l3.007-2.335z"/>
              <path fill="#EA4335" d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0 5.482 0 2.438 2.017.957 4.958L3.964 7.29C4.672 5.163 6.656 3.58 9 3.58z"/>
            </svg>
            Continue with Google
          </button>

          <div className="auth-footer-link">
            Already have an account?{' '}
            <Link to="/auth/login">Login</Link>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default function SignupPage() {
  return (
    <BrowserOnly fallback={<div>Loading...</div>}>
      {() => <SignupPageContent />}
    </BrowserOnly>
  );
}
