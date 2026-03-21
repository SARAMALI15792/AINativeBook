'use client';

import React, { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui';
import { useAuth } from '@/contexts/AuthContext';
import { UserMenu } from './UserMenu';

interface HeaderProps {
  transparent?: boolean;
  className?: string;
}

export function Header({ transparent = false, className = '' }: HeaderProps) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const [isStagesOpen, setIsStagesOpen] = useState(false);
  const stagesRef = useRef<HTMLDivElement>(null);
  const { session } = useAuth();

  const docusaurusUrl = (process.env.NEXT_PUBLIC_DOCUSAURUS_URL || 'http://localhost:3005/AINativeBook').replace(/\/$/, '');

  const stages = [
    { label: 'Stage 1: Foundations',          href: `${docusaurusUrl}/stage-1/intro` },
    { label: 'Stage 2: ROS 2 & Simulation',   href: `${docusaurusUrl}/stage-2/intro` },
    { label: 'Stage 3: Perception & Planning', href: `${docusaurusUrl}/stage-3/intro` },
    { label: 'Stage 4: AI Integration',        href: `${docusaurusUrl}/stage-4/intro` },
    { label: 'Stage 5: Capstone Project',      href: `${docusaurusUrl}/stage-5/intro` },
  ];

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (stagesRef.current && !stagesRef.current.contains(e.target as Node)) {
        setIsStagesOpen(false);
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  const navLinks: { label: string; href: string; badge?: string; external?: boolean }[] = [
    { label: 'Home', href: '/' },
    { label: 'Dashboard', href: '/dashboard' },
    { label: 'Curriculum', href: '/curriculum' },
  ];

  const baseStyles = 'fixed top-0 left-0 right-0 z-[1100] transition-all duration-normal';
  const backgroundStyles =
    transparent && !isScrolled
      ? 'bg-transparent'
      : 'bg-bg-primary/80 backdrop-blur-md border-b border-border-subtle shadow-md';

  return (
    <>
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-[9999] focus:px-4 focus:py-2 focus:bg-accent-blue focus:text-white focus:font-semibold focus:rounded-lg focus:shadow-lg"
      >
        Skip to main content
      </a>

      <header className={`${baseStyles} ${backgroundStyles} ${className}`}>
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <Link href="/" className="flex items-center space-x-2 group">
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-accent-blue to-accent-violet flex items-center justify-center group-hover:shadow-glow-blue transition-all">
                <span className="text-white font-bold text-xl font-heading">IS</span>
              </div>
              <span className="text-xl font-bold text-text-primary font-heading hidden sm:block">
                IntelliStack
              </span>
            </Link>

            {/* Desktop Navigation — pill container */}
            <nav className="hidden md:flex items-center bg-bg-secondary border border-border-subtle rounded-full px-1 py-1">
              {navLinks.map((link) => {
                const pillClass =
                  'relative text-text-secondary hover:text-text-primary hover:bg-bg-elevated rounded-full px-4 py-1.5 text-sm font-medium transition-all duration-normal inline-flex items-center gap-1.5';

                const linkContent = (
                  <>
                    {link.label}
                    {link.badge && (
                      <span className="inline-flex items-center px-1.5 py-0.5 rounded-full text-[10px] font-semibold bg-accent-blue/20 text-accent-blue border border-accent-blue/30">
                        {link.badge}
                      </span>
                    )}
                  </>
                );

                if (link.external) {
                  return (
                    <a key={link.label} href={link.href} className={pillClass} target="_blank" rel="noopener noreferrer">
                      {linkContent}
                    </a>
                  );
                }
                return (
                  <Link key={link.label} href={link.href} className={pillClass}>
                    {linkContent}
                  </Link>
                );
              })}

              {/* Community — inline "Soon" badge, no overflow */}
              <span className="text-text-muted rounded-full px-4 py-1.5 text-sm font-medium opacity-50 cursor-not-allowed inline-flex items-center gap-1.5 select-none">
                Community
                <span className="text-[9px] font-bold px-1.5 py-0.5 rounded-full bg-accent-amber/20 text-accent-amber border border-accent-amber/30">
                  Soon
                </span>
              </span>

              {/* Stages Dropdown */}
              <div ref={stagesRef} className="relative">
                <button
                  onClick={() => setIsStagesOpen(!isStagesOpen)}
                  className="relative text-text-secondary hover:text-text-primary hover:bg-bg-elevated rounded-full px-4 py-1.5 text-sm font-medium transition-all duration-normal inline-flex items-center gap-1.5"
                >
                  Stages
                  <svg
                    className={`w-3 h-3 transition-transform ${isStagesOpen ? 'rotate-180' : ''}`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                {isStagesOpen && (
                  <div className="absolute top-full left-0 mt-2 w-56 bg-bg-secondary border border-border-subtle rounded-lg shadow-lg z-[1200] py-1">
                    {stages.map((stage) => (
                      <a
                        key={stage.href}
                        href={stage.href}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="block px-4 py-2 text-sm text-text-secondary hover:text-text-primary hover:bg-bg-elevated transition-colors"
                        onClick={() => setIsStagesOpen(false)}
                      >
                        {stage.label}
                      </a>
                    ))}
                  </div>
                )}
              </div>
            </nav>

            {/* Auth — Desktop */}
            <div className="hidden md:flex items-center">
              {session.isAuthenticated ? (
                <UserMenu />
              ) : (
                <a href={`${docusaurusUrl}/auth/login`}>
                  <Button variant="primary" size="sm">
                    Login
                  </Button>
                </a>
              )}
            </div>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="md:hidden text-text-primary focus:outline-none focus:ring-2 focus:ring-accent-blue rounded p-2"
              aria-label="Toggle mobile menu"
              aria-expanded={isMobileMenuOpen}
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                {isMobileMenuOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>

          {/* Mobile Menu */}
          {isMobileMenuOpen && (
            <div className="md:hidden py-4 surface rounded-lg mt-2 animate-slide-in-left">
              <nav className="flex flex-col space-y-1 px-4">
                {navLinks.map((link) => {
                  const content = (
                    <>
                      {link.label}
                      {link.badge && (
                        <span className="ml-2 inline-flex items-center px-1.5 py-0.5 rounded-full text-[10px] font-semibold bg-accent-blue/20 text-accent-blue border border-accent-blue/30">
                          {link.badge}
                        </span>
                      )}
                    </>
                  );
                  const cls =
                    'text-text-secondary hover:text-text-primary hover:bg-bg-elevated transition-colors py-2 px-3 rounded-lg inline-flex items-center';

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

                {/* Mobile Community */}
                <div className="flex items-center gap-2 py-2 px-3 opacity-50 cursor-not-allowed select-none">
                  <span className="text-text-secondary text-sm font-medium">Community</span>
                  <span className="text-[9px] font-bold px-1.5 py-0.5 rounded-full bg-accent-amber/20 text-accent-amber border border-accent-amber/30">
                    Soon
                  </span>
                </div>

                {/* Mobile Stages */}
                <div className="pt-1 pb-1">
                  <p className="px-3 py-1 text-xs font-semibold text-text-tertiary uppercase tracking-wider">Stages</p>
                  {stages.map((stage) => (
                    <a
                      key={stage.href}
                      href={stage.href}
                      target="_blank"
                      rel="noopener noreferrer"
                      onClick={() => setIsMobileMenuOpen(false)}
                      className="text-text-secondary hover:text-text-primary hover:bg-bg-elevated transition-colors py-2 px-3 rounded-lg inline-flex items-center w-full text-sm"
                    >
                      {stage.label}
                    </a>
                  ))}
                </div>
                {session.isAuthenticated ? (
                  <div className="py-2">
                    <UserMenu />
                  </div>
                ) : (
                  <a href={`${docusaurusUrl}/auth/login`} className="py-2 block">
                    <Button variant="primary" size="sm" fullWidth>
                      Login
                    </Button>
                  </a>
                )}
              </nav>
            </div>
          )}
        </div>
      </header>
    </>
  );
}
