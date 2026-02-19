import React from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import { useAuth } from '../contexts/AuthContext';

export default function UserMenu() {
  const { user, loading, logout } = useAuth();
  const { siteConfig } = useDocusaurusContext();
  const frontendUrl = (siteConfig.customFields?.frontendUrl as string) || 'http://localhost:3004';

  if (loading) {
    return (
      <div className="navbar__item">
        <div className="w-8 h-8 rounded-full bg-gray-700 animate-pulse" />
      </div>
    );
  }

  if (!user) {
    return (
      <div className="navbar__item navbar__item--auth">
        <a
          href="/login"
          className="button button--secondary button--sm"
        >
          Login
        </a>
        <a
          href="/register"
          className="button button--primary button--sm"
          style={{ marginLeft: '0.5rem' }}
        >
          Sign Up
        </a>
      </div>
    );
  }

  return (
    <div className="navbar__item dropdown dropdown--hoverable">
      <button
        className="navbar__link"
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          cursor: 'pointer',
          background: 'none',
          border: 'none',
          padding: '0.5rem',
        }}
      >
        <div
          style={{
            width: '32px',
            height: '32px',
            borderRadius: '50%',
            background: 'linear-gradient(135deg, #00efff, #a855f7)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white',
            fontWeight: 'bold',
            fontSize: '14px',
          }}
        >
          {user.name?.charAt(0).toUpperCase() || 'U'}
        </div>
        <span>{user.name}</span>
        <svg
          width="12"
          height="12"
          viewBox="0 0 12 12"
          fill="currentColor"
          style={{ marginLeft: '4px' }}
        >
          <path d="M6 9L1 4h10z" />
        </svg>
      </button>
      <ul className="dropdown__menu">
        <li>
          <a
            href="/profile"
            className="dropdown__link"
          >
            Profile
          </a>
        </li>
        <li>
          <a
            href={frontendUrl + '/personalization'}
            className="dropdown__link"
          >
            Preferences
          </a>
        </li>
        <li>
          <hr className="dropdown__divider" />
        </li>
        <li>
          <button
            onClick={logout}
            className="dropdown__link"
            style={{
              width: '100%',
              textAlign: 'left',
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              padding: '0.5rem 1rem',
            }}
          >
            Logout
          </button>
        </li>
      </ul>
    </div>
  );
}
