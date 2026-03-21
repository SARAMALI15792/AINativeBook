import React, { useState, useEffect } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import { signUp, signInWithGoogle, signInWithGitHub } from '../../lib/auth';
import TriangleLoader from '../../components/ui/TriangleLoader';

const QUOTES = [
  { text: 'Every expert was once a beginner.', author: '— Helen Hayes' },
  { text: 'The best time to start was yesterday. The next best time is now.', author: '— Proverb' },
  { text: 'Physical AI is the frontier. You are the explorer.', author: '— IntelliStack' },
];

const GoogleIcon = () => (
  <svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true">
    <path fill="#4285F4" d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.874 2.684-6.615z"/>
    <path fill="#34A853" d="M9 18c2.43 0 4.467-.806 5.956-2.184l-2.908-2.258c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332C2.438 15.983 5.482 18 9 18z"/>
    <path fill="#FBBC05" d="M3.964 10.707c-.18-.54-.282-1.117-.282-1.707 0-.593.102-1.17.282-1.709V4.958H.957C.347 6.173 0 7.548 0 9c0 1.452.348 2.827.957 4.042l3.007-2.335z"/>
    <path fill="#EA4335" d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0 5.482 0 2.438 2.017.957 4.958L3.964 7.29C4.672 5.163 6.656 3.58 9 3.58z"/>
  </svg>
);

const GitHubIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
    <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0 1 12 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
  </svg>
);

function SignupPageContent() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [quoteIndex, setQuoteIndex] = useState(0);
  const [quoteVisible, setQuoteVisible] = useState(true);

  useEffect(() => {
    const interval = setInterval(() => {
      setQuoteVisible(false);
      setTimeout(() => {
        setQuoteIndex(i => (i + 1) % QUOTES.length);
        setQuoteVisible(true);
      }, 500);
    }, 4500);
    return () => clearInterval(interval);
  }, []);

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
    } catch {
      setError('An unexpected error occurred. Please try again.');
      setLoading(false);
    }
  };

  const handleGoogleSignup = async () => {
    setError('');
    setLoading(true);
    try {
      const baseUrl = ((window as any).docusaurus?.siteConfig?.baseUrl || '/AINativeBook/').replace(/\/$/, '');
      await signInWithGoogle(`${window.location.origin}${baseUrl}/auth/callback`);
    } catch {
      setError('Google signup failed. Please try again.');
      setLoading(false);
    }
  };

  const handleGitHubSignup = async () => {
    setError('');
    setLoading(true);
    try {
      const baseUrl = ((window as any).docusaurus?.siteConfig?.baseUrl || '/AINativeBook/').replace(/\/$/, '');
      await signInWithGitHub(`${window.location.origin}${baseUrl}/auth/callback`);
    } catch {
      setError('GitHub signup failed. Please try again.');
      setLoading(false);
    }
  };

  const quote = QUOTES[quoteIndex];

  return (
    <Layout title="Sign Up" description="Create your IntelliStack account" noFooter>
      <div className="auth-split-wrapper">
        {/* Left panel */}
        <div className="auth-split-left">
          <div className="auth-split-blob" />

          <div className="auth-split-logo">
            <div className="auth-split-logo-mark">IS</div>
            <span className="auth-split-logo-name">IntelliStack</span>
          </div>

          <div className="auth-split-quote" style={{ opacity: quoteVisible ? 1 : 0, transition: 'opacity 0.5s ease' }}>
            <p className="auth-split-quote-text">"{quote.text}"</p>
            <span className="auth-split-quote-author">{quote.author}</span>
          </div>
        </div>

        {/* Right panel */}
        <div className="auth-split-right">
          <div className="auth-split-form-container">
            <h1 className="auth-split-headline">Create account</h1>
            <p className="auth-split-subheadline">Join thousands of learners mastering Physical AI.</p>

            {error && <div className="auth-error">{error}</div>}

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.625rem', marginBottom: '1rem' }}>
              <button onClick={handleGoogleSignup} disabled={loading} className="auth-btn-oauth">
                <GoogleIcon /> Continue with Google
              </button>
              <button onClick={handleGitHubSignup} disabled={loading} className="auth-btn-oauth">
                <GitHubIcon /> Continue with GitHub
              </button>
            </div>

            <div className="auth-split-divider">or sign up with email</div>

            <form onSubmit={handleSubmit} noValidate>
              <div className="auth-float-field">
                <input
                  id="name"
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder=" "
                  disabled={loading}
                  className={`auth-float-input${name ? ' has-value' : ''}`}
                  required
                  autoComplete="name"
                />
                <label htmlFor="name" className="auth-float-label">Full name</label>
              </div>

              <div className="auth-float-field">
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder=" "
                  disabled={loading}
                  className={`auth-float-input${email ? ' has-value' : ''}`}
                  required
                  autoComplete="email"
                />
                <label htmlFor="email" className="auth-float-label">Email address</label>
              </div>

              <div className="auth-float-field">
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder=" "
                  disabled={loading}
                  className={`auth-float-input${password ? ' has-value' : ''}`}
                  required
                  autoComplete="new-password"
                />
                <label htmlFor="password" className="auth-float-label">Password (min 8 chars)</label>
              </div>

              <div className="auth-float-field" style={{ marginBottom: '1.25rem' }}>
                <input
                  id="confirmPassword"
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder=" "
                  disabled={loading}
                  className={`auth-float-input${confirmPassword ? ' has-value' : ''}`}
                  required
                  autoComplete="new-password"
                />
                <label htmlFor="confirmPassword" className="auth-float-label">Confirm password</label>
              </div>

              <button type="submit" disabled={loading} className="auth-btn-brand">
                {loading ? <TriangleLoader size="sm" /> : null}
                {loading ? 'Creating account…' : 'Create account'}
              </button>
            </form>

            <p style={{ textAlign: 'center', marginTop: '1.25rem', fontSize: '0.8125rem', color: '#64748b' }}>
              Already have an account?{' '}
              <Link to="/auth/login" style={{ color: '#6366f1', fontWeight: 600 }}>Sign in</Link>
            </p>

            <div className="auth-betterauth-footer">
              Powered by{' '}
              <a href="https://better-auth.com" target="_blank" rel="noopener noreferrer">BetterAuth</a>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default function SignupPage() {
  return (
    <BrowserOnly fallback={<div style={{ minHeight: '100vh' }} />}>
      {() => <SignupPageContent />}
    </BrowserOnly>
  );
}
