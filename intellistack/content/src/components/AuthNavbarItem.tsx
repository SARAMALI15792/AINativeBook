import React, { useState, useRef, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { authClient } from '../../lib/auth';

export default function AuthNavbarItem() {
  const { user, loading } = useAuth();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setDropdownOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleLogout = async () => {
    try {
      await authClient.signOut();
      window.dispatchEvent(new Event('auth-state-changed'));
      window.location.href = '/';
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  if (loading) {
    return null;
  }

  // Show Login button when unauthenticated
  if (!user) {
    return (
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <a
          href="/auth/login"
          style={{
            padding: '0.5rem 1rem',
            borderRadius: '4px',
            textDecoration: 'none',
            color: 'white',
            backgroundColor: 'var(--ifm-color-primary)',
            fontWeight: 500,
          }}
        >
          Login
        </a>
      </div>
    );
  }

  // Show User Menu when authenticated
  return (
    <div ref={dropdownRef} style={{ position: 'relative' }}>
      <button
        onClick={() => setDropdownOpen(!dropdownOpen)}
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          padding: '0.5rem 1rem',
          border: '1px solid var(--ifm-color-emphasis-300)',
          borderRadius: '4px',
          backgroundColor: 'transparent',
          color: 'var(--ifm-navbar-link-color)',
          cursor: 'pointer',
          fontWeight: 500,
        }}
      >
        <div
          style={{
            width: '32px',
            height: '32px',
            borderRadius: '50%',
            backgroundColor: 'var(--ifm-color-primary)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white',
            fontWeight: 'bold',
            fontSize: '0.875rem',
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
          style={{
            transform: dropdownOpen ? 'rotate(180deg)' : 'rotate(0deg)',
            transition: 'transform 0.2s',
          }}
        >
          <path d="M6 9L1 4h10z" />
        </svg>
      </button>

      {dropdownOpen && (
        <div
          style={{
            position: 'absolute',
            top: 'calc(100% + 0.5rem)',
            right: 0,
            minWidth: '200px',
            backgroundColor: 'var(--ifm-background-surface-color)',
            border: '1px solid var(--ifm-color-emphasis-300)',
            borderRadius: '4px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            zIndex: 1000,
          }}
        >
          <div
            style={{
              padding: '1rem',
              borderBottom: '1px solid var(--ifm-color-emphasis-300)',
            }}
          >
            <div style={{ fontWeight: 'bold', marginBottom: '0.25rem' }}>
              {user.name}
            </div>
            <div style={{ fontSize: '0.875rem', color: 'var(--ifm-color-emphasis-600)' }}>
              {user.email}
            </div>
          </div>

          <div style={{ padding: '0.5rem 0' }}>
            <a
              href="/profile"
              style={{
                display: 'block',
                padding: '0.75rem 1rem',
                textDecoration: 'none',
                color: 'var(--ifm-font-color-base)',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = 'var(--ifm-color-emphasis-100)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = 'transparent';
              }}
            >
              Profile
            </a>
            <a
              href="/settings"
              style={{
                display: 'block',
                padding: '0.75rem 1rem',
                textDecoration: 'none',
                color: 'var(--ifm-font-color-base)',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = 'var(--ifm-color-emphasis-100)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = 'transparent';
              }}
            >
              Settings
            </a>
          </div>

          <div
            style={{
              padding: '0.5rem 0',
              borderTop: '1px solid var(--ifm-color-emphasis-300)',
            }}
          >
            <button
              onClick={handleLogout}
              style={{
                display: 'block',
                width: '100%',
                padding: '0.75rem 1rem',
                textAlign: 'left',
                border: 'none',
                backgroundColor: 'transparent',
                color: 'var(--ifm-color-danger)',
                cursor: 'pointer',
                fontWeight: 500,
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = 'var(--ifm-color-emphasis-100)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = 'transparent';
              }}
            >
              Logout
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
