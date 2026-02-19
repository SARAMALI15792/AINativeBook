'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui';
import { UserMenu } from './UserMenu';
import { useAuth } from '@/contexts/AuthContext';

interface HeaderProps {
  transparent?: boolean;
  showAuth?: boolean;
  className?: string;
}

export function Header({ transparent = false, showAuth = true, className = '' }: HeaderProps) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const { session } = useAuth();

  const navLinks: { label: string; href: string; badge?: string; external?: boolean }[] = [
    { label: 'Home', href: '/' },
    { label: 'Books', href: `${process.env.NEXT_PUBLIC_DOCUSAURUS_URL || 'http://localhost:3002'}/docs/stage-1/intro`, external: true },
    { label: 'Personalize', href: '/personalization' },
    { label: 'Community', href: '#', badge: 'Coming Soon' },
    { label: 'AI Tutor', href: '#', badge: 'Coming Soon' },
  ];

  const baseStyles = 'fixed top-0 left-0 right-0 z-sticky transition-all duration-normal';
  const backgroundStyles = transparent
    ? 'bg-transparent'
    : 'glass backdrop-blur-md border-b border-glass-border shadow-md';

  return (
    <>
      {/* Skip to main content link for accessibility */}
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-[9999] focus:px-4 focus:py-2 focus:bg-accent-cyan focus:text-bg-primary focus:font-semibold focus:rounded-lg focus:shadow-lg"
      >
        Skip to main content
      </a>

      <header className={`${baseStyles} ${backgroundStyles} ${className}`}>
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2 group">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-accent-cyan to-accent-violet flex items-center justify-center group-hover:shadow-glow-cyan transition-all">
              <span className="text-white font-bold text-xl">IS</span>
            </div>
            <span className="text-xl font-bold text-text-primary hidden sm:block">
              IntelliStack
            </span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            {navLinks.map((link) => {
              const linkContent = (
                <>
                  {link.label}
                  {link.badge && (
                    <span className="ml-1.5 inline-flex items-center px-1.5 py-0.5 rounded-full text-[10px] font-semibold bg-gradient-to-r from-accent-cyan/20 to-accent-violet/20 text-accent-cyan border border-accent-cyan/30">
                      {link.badge}
                    </span>
                  )}
                  <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-accent-cyan to-accent-violet group-hover:w-full transition-all duration-normal" />
                </>
              );
              const className = "relative text-text-secondary hover:text-accent-cyan transition-all duration-normal focus:outline-none focus:ring-2 focus:ring-accent-cyan rounded px-2 py-1 group inline-flex items-center";

              if (link.external) {
                return (
                  <a key={link.label} href={link.href} className={className}>
                    {linkContent}
                  </a>
                );
              }
              return (
                <Link key={link.label} href={link.href} className={className}>
                  {linkContent}
                </Link>
              );
            })}
          </nav>

          {/* Auth Buttons / User Menu */}
          {showAuth && (
            <div className="hidden md:flex items-center space-x-4">
              {session.isAuthenticated ? (
                <UserMenu />
              ) : (
                <>
                  <Link href="/auth/login">
                    <Button
                      variant="ghost"
                      size="sm"
                      className="hover:shadow-glow-cyan transition-all duration-normal"
                    >
                      Login
                    </Button>
                  </Link>
                  <Link href="/auth/register">
                    <Button
                      variant="primary"
                      size="sm"
                      className="hover:shadow-glow-cyan hover:scale-105 transition-all duration-normal"
                    >
                      Sign Up
                    </Button>
                  </Link>
                </>
              )}
            </div>
          )}

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="md:hidden text-text-primary focus:outline-none focus:ring-2 focus:ring-accent-cyan rounded p-2"
            aria-label="Toggle mobile menu"
            aria-expanded={isMobileMenuOpen}
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              {isMobileMenuOpen ? (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              ) : (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Menu */}
        {isMobileMenuOpen && (
          <div className="md:hidden py-4 glass backdrop-blur-md rounded-lg mt-2 animate-slide-in-left">
            <nav className="flex flex-col space-y-2 px-4">
              {navLinks.map((link) => {
                const content = (
                  <>
                    {link.label}
                    {link.badge && (
                      <span className="ml-2 inline-flex items-center px-1.5 py-0.5 rounded-full text-[10px] font-semibold bg-gradient-to-r from-accent-cyan/20 to-accent-violet/20 text-accent-cyan border border-accent-cyan/30">
                        {link.badge}
                      </span>
                    )}
                  </>
                );
                const cls = "text-text-secondary hover:text-accent-cyan transition-colors py-2 px-3 rounded hover:bg-glass-highlight inline-flex items-center";

                if (link.external) {
                  return (
                    <a key={link.label} href={link.href} onClick={() => setIsMobileMenuOpen(false)} className={cls}>
                      {content}
                    </a>
                  );
                }
                return (
                  <Link key={link.label} href={link.href} onClick={() => setIsMobileMenuOpen(false)} className={cls}>
                    {content}
                  </Link>
                );
              })}
              {showAuth && (
                <>
                  {session.isAuthenticated ? (
                    <div className="py-2 border-t border-glass-border mt-2">
                      <UserMenu />
                    </div>
                  ) : (
                    <>
                      <Link
                        href="/auth/login"
                        onClick={() => setIsMobileMenuOpen(false)}
                        className="py-2"
                      >
                        <Button variant="ghost" size="sm" fullWidth>
                          Login
                        </Button>
                      </Link>
                      <Link
                        href="/auth/register"
                        onClick={() => setIsMobileMenuOpen(false)}
                        className="py-2"
                      >
                        <Button variant="primary" size="sm" fullWidth>
                          Sign Up
                        </Button>
                      </Link>
                    </>
                  )}
                </>
              )}
            </nav>
          </div>
        )}
      </div>
    </header>
    </>
  );
}
