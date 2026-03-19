import React, { useState } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import { useHistory } from '@docusaurus/router';
import { signIn, signInWithGoogle } from '../../lib/auth';

function LoginPageContent() {
  const history = useHistory();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (!email || !password) {
        setError('Email and password are required');
        setLoading(false);
        return;
      }

      if (password.length < 8) {
        setError('Password must be at least 8 characters');
        setLoading(false);
        return;
      }

      const result = await signIn(email, password, rememberMe);

      if (result.error) {
        setError(result.error.message || 'Login failed. Please check your credentials.');
        setLoading(false);
        return;
      }

      window.dispatchEvent(new Event('auth-state-changed'));

      const baseUrl = (window as any).docusaurus?.siteConfig?.baseUrl || '/AINativeBook/';
      window.location.href = `${baseUrl}stage-1/intro`;
    } catch (err) {
      console.error('Login error:', err);
      setError('An unexpected error occurred. Please try again.');
      setLoading(false);
    }
  };

  const handleGoogleLogin = async () => {
    setError('');
    setLoading(true);

    try {
      await signInWithGoogle(`${window.location.origin}/auth/callback`);
    } catch (err) {
      console.error('Google login error:', err);
      setError('Google login failed. Please try again.');
      setLoading(false);
    }
  };

  return (
    <Layout title="Login" description="Login to IntelliStack">
      <div className="auth-page-wrapper">
        <div className="auth-form-card">
          <h1>Login</h1>

          {error && <div className="auth-error">{error}</div>}

          <form onSubmit={handleSubmit}>
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
            </div>

            <div className="auth-field" style={{ marginBottom: '1.5rem' }}>
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  disabled={loading}
                />
                <span style={{ color: 'var(--color-text-secondary)', fontSize: 'var(--text-sm)' }}>
                  Remember me
                </span>
              </label>
            </div>

            <button type="submit" disabled={loading} className="auth-btn-primary">
              {loading ? 'Logging in...' : 'Login'}
            </button>
          </form>

          <div className="auth-divider">or</div>

          <button onClick={handleGoogleLogin} disabled={loading} className="auth-btn-google">
            <svg width="18" height="18" viewBox="0 0 18 18">
              <path fill="#4285F4" d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.874 2.684-6.615z"/>
              <path fill="#34A853" d="M9 18c2.43 0 4.467-.806 5.956-2.184l-2.908-2.258c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332C2.438 15.983 5.482 18 9 18z"/>
              <path fill="#FBBC05" d="M3.964 10.707c-.18-.54-.282-1.117-.282-1.707 0-.593.102-1.17.282-1.709V4.958H.957C.347 6.173 0 7.548 0 9c0 1.452.348 2.827.957 4.042l3.007-2.335z"/>
              <path fill="#EA4335" d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0 5.482 0 2.438 2.017.957 4.958L3.964 7.29C4.672 5.163 6.656 3.58 9 3.58z"/>
            </svg>
            Continue with Google
          </button>

          <div className="auth-footer-link">
            Don&apos;t have an account?{' '}
            <Link to="/auth/signup">Sign up</Link>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default function LoginPage() {
  return (
    <BrowserOnly fallback={<div>Loading...</div>}>
      {() => <LoginPageContent />}
    </BrowserOnly>
  );
}
