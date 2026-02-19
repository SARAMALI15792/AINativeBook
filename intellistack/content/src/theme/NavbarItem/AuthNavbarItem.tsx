/**
 * Auth Navbar Item Component
 * Shows Sign In button or user dropdown based on auth state
 */

import React, { useState } from 'react';
import Link from '@docusaurus/Link';
import { useColorMode } from '@docusaurus/theme-common';
import { useAuth } from '@site/src/contexts/AuthContext';
import styles from './AuthNavbarItem.module.css';

export default function AuthNavbarItem(): JSX.Element {
  const { user, loading, logout } = useAuth();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const { colorMode } = useColorMode();

  const handleSignOut = async () => {
    setIsDropdownOpen(false);
    await logout();
  };

  // Loading state
  if (loading) {
    return (
      <div className={styles.authNavbarItem}>
        <span className={styles.loadingDot}>...</span>
      </div>
    );
  }

  // Authenticated state
  if (user) {
    const initials = user.name
      ? user.name.split(' ').map((n: string) => n[0]).join('').toUpperCase().slice(0, 2)
      : user.email[0].toUpperCase();

    return (
      <div className={styles.authNavbarItem}>
        <div
          className={styles.userDropdown}
          onMouseEnter={() => setIsDropdownOpen(true)}
          onMouseLeave={() => setIsDropdownOpen(false)}
        >
          <button className={styles.userButton} aria-label="User menu">
            {user.image ? (
              <img
                src={user.image}
                alt={user.name || 'User'}
                className={styles.userAvatar}
              />
            ) : (
              <span className={styles.userInitials}>{initials}</span>
            )}
            <span className={styles.userName}>{user.name || user.email}</span>
            <svg
              className={styles.chevron}
              width="12"
              height="12"
              viewBox="0 0 12 12"
              style={{ transform: isDropdownOpen ? 'rotate(180deg)' : 'rotate(0deg)' }}
            >
              <path d="M2 4L6 8L10 4" fill="none" stroke="currentColor" strokeWidth="2"/>
            </svg>
          </button>

          {isDropdownOpen && (
            <div className={styles.dropdownMenu}>
              <div className={styles.dropdownHeader}>
                <span className={styles.dropdownEmail}>{user.email}</span>
                <span className={styles.dropdownRole}>{user.role || 'Student'}</span>
              </div>
              <div className={styles.dropdownDivider} />
              <Link to="/profile" className={styles.dropdownItem}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
                Profile
              </Link>
              <Link to="/settings" className={styles.dropdownItem}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="3"/>
                  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
                </svg>
                Settings
              </Link>
              <div className={styles.dropdownDivider} />
              <button onClick={handleSignOut} className={styles.dropdownItemDanger}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                  <polyline points="16 17 21 12 16 7"/>
                  <line x1="21" y1="12" x2="9" y2="12"/>
                </svg>
                Sign Out
              </button>
            </div>
          )}
        </div>
      </div>
    );
  }

  // Unauthenticated state
  return (
    <div className={styles.authNavbarItem}>
      <Link to="/login" className={styles.signInButton}>
        Sign In
      </Link>
    </div>
  );
}
