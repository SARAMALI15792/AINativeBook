'use client';

import React from 'react';
import Link from 'next/link';

interface FooterProps {
  className?: string;
}

const GitHubIcon = () => (
  <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
  </svg>
);

const TwitterIcon = () => (
  <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
    <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
  </svg>
);

const DiscordIcon = () => (
  <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
    <path d="M20.317 4.492c-1.53-.69-3.17-1.2-4.885-1.49a.075.075 0 0 0-.079.036c-.21.369-.444.85-.608 1.23a18.566 18.566 0 0 0-5.487 0 12.36 12.36 0 0 0-.617-1.23A.077.077 0 0 0 8.562 3c-1.714.29-3.354.8-4.885 1.491a.07.07 0 0 0-.032.027C.533 9.093-.32 13.555.099 17.961a.08.08 0 0 0 .031.055 20.03 20.03 0 0 0 5.993 2.98.078.078 0 0 0 .084-.026c.462-.62.874-1.275 1.226-1.963.021-.04.001-.088-.041-.104a13.201 13.201 0 0 1-1.872-.878.075.075 0 0 1-.008-.125c.126-.093.252-.19.372-.287a.075.075 0 0 1 .078-.01c3.927 1.764 8.18 1.764 12.061 0a.075.075 0 0 1 .079.009c.12.098.245.195.372.288a.075.075 0 0 1-.006.125c-.598.344-1.22.635-1.873.877a.075.075 0 0 0-.041.105c.36.687.772 1.341 1.225 1.962a.077.077 0 0 0 .084.028 19.963 19.963 0 0 0 6.002-2.981.076.076 0 0 0 .032-.054c.5-5.094-.838-9.52-3.549-13.442a.06.06 0 0 0-.031-.028zM8.02 15.278c-1.182 0-2.157-1.069-2.157-2.38 0-1.312.956-2.38 2.157-2.38 1.21 0 2.176 1.077 2.157 2.38 0 1.312-.956 2.38-2.157 2.38zm7.975 0c-1.183 0-2.157-1.069-2.157-2.38 0-1.312.955-2.38 2.157-2.38 1.21 0 2.176 1.077 2.157 2.38 0 1.312-.946 2.38-2.157 2.38z" />
  </svg>
);

const docusaurusUrl =
  typeof process !== 'undefined'
    ? process.env.NEXT_PUBLIC_DOCUSAURUS_URL || 'http://localhost:3002/AINativeBook'
    : 'http://localhost:3002/AINativeBook';

export function Footer({ className = '' }: FooterProps) {
  return (
    <footer className={`relative mt-auto ${className}`}>
      {/* Gradient top border */}
      <div
        aria-hidden="true"
        style={{
          height: '1px',
          background: 'linear-gradient(90deg, transparent 0%, #6366f1 40%, #a78bfa 60%, transparent 100%)',
        }}
      />

      {/* Main footer body */}
      <div
        style={{
          background: 'rgba(10, 10, 16, 0.95)',
          backdropFilter: 'blur(16px)',
          WebkitBackdropFilter: 'blur(16px)',
        }}
      >
        {/* Top section — 3 columns */}
        <div
          className="container mx-auto px-6"
          style={{ paddingTop: '3rem', paddingBottom: '2.5rem' }}
        >
          <div className="grid grid-cols-1 md:grid-cols-4 gap-10">

            {/* Brand column */}
            <div className="md:col-span-1 space-y-4">
              <div className="flex items-center gap-3">
                <div
                  style={{
                    width: 36,
                    height: 36,
                    borderRadius: '8px',
                    background: 'linear-gradient(135deg, #4f46e5, #6366f1)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0,
                  }}
                >
                  <span style={{ color: 'white', fontWeight: 800, fontSize: '13px', fontFamily: 'var(--font-heading)' }}>IS</span>
                </div>
                <span style={{ color: '#f1f5f9', fontWeight: 700, fontSize: '16px', fontFamily: 'var(--font-heading)' }}>
                  IntelliStack
                </span>
              </div>
              <p style={{ color: '#64748b', fontSize: '14px', lineHeight: 1.6 }}>
                AI-Native learning platform for Physical AI & Humanoid Robotics education.
              </p>
              {/* Social icons */}
              <div style={{ display: 'flex', gap: '0.5rem', paddingTop: '0.25rem' }}>
                {[
                  { label: 'GitHub',  href: 'https://github.com',  Icon: GitHubIcon },
                  { label: 'Twitter', href: 'https://twitter.com', Icon: TwitterIcon },
                  { label: 'Discord', href: 'https://discord.com', Icon: DiscordIcon },
                ].map(({ label, href, Icon }) => (
                  <a
                    key={label}
                    href={href}
                    target="_blank"
                    rel="noopener noreferrer"
                    aria-label={label}
                    style={{
                      color: '#64748b',
                      padding: '8px',
                      borderRadius: '8px',
                      display: 'flex',
                      alignItems: 'center',
                      border: '1px solid rgba(255,255,255,0.06)',
                      transition: 'color 0.2s, background 0.2s, border-color 0.2s',
                    }}
                    onMouseEnter={(e) => {
                      const el = e.currentTarget as HTMLElement;
                      el.style.color = '#f1f5f9';
                      el.style.background = 'rgba(99,102,241,0.12)';
                      el.style.borderColor = 'rgba(99,102,241,0.3)';
                    }}
                    onMouseLeave={(e) => {
                      const el = e.currentTarget as HTMLElement;
                      el.style.color = '#64748b';
                      el.style.background = 'transparent';
                      el.style.borderColor = 'rgba(255,255,255,0.06)';
                    }}
                  >
                    <Icon />
                  </a>
                ))}
              </div>
            </div>

            {/* Platform links */}
            <div className="space-y-3">
              <p style={{ color: '#f1f5f9', fontWeight: 600, fontSize: '13px', letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: '1rem' }}>
                Platform
              </p>
              {[
                { label: 'Curriculum',  href: '/curriculum' },
                { label: 'Dashboard',   href: '/dashboard' },
                { label: 'AI Tutor',    href: '/tutor' },
                { label: 'Simulations', href: '/simulations' },
              ].map((link) => (
                <div key={link.label}>
                  <Link
                    href={link.href}
                    style={{ color: '#94a3b8', fontSize: '14px', textDecoration: 'none', transition: 'color 0.2s' }}
                    onMouseEnter={(e) => ((e.currentTarget as HTMLElement).style.color = '#f1f5f9')}
                    onMouseLeave={(e) => ((e.currentTarget as HTMLElement).style.color = '#94a3b8')}
                  >
                    {link.label}
                  </Link>
                </div>
              ))}
            </div>

            {/* Learn links */}
            <div className="space-y-3">
              <p style={{ color: '#f1f5f9', fontWeight: 600, fontSize: '13px', letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: '1rem' }}>
                Learn
              </p>
              {[
                { label: 'Stage 1 — Foundations',     href: `${docusaurusUrl}/stage-1/intro`, external: true },
                { label: 'Stage 2 — ROS 2',           href: `${docusaurusUrl}/stage-2/intro`, external: true },
                { label: 'Stage 3 — Perception',      href: `${docusaurusUrl}/stage-3/intro`, external: true },
                { label: 'Stage 4 — AI Integration',  href: `${docusaurusUrl}/stage-4/intro`, external: true },
              ].map((link) => (
                <div key={link.label}>
                  <a
                    href={link.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{ color: '#94a3b8', fontSize: '14px', textDecoration: 'none', transition: 'color 0.2s' }}
                    onMouseEnter={(e) => ((e.currentTarget as HTMLElement).style.color = '#f1f5f9')}
                    onMouseLeave={(e) => ((e.currentTarget as HTMLElement).style.color = '#94a3b8')}
                  >
                    {link.label}
                  </a>
                </div>
              ))}
            </div>

            {/* Company links */}
            <div className="space-y-3">
              <p style={{ color: '#f1f5f9', fontWeight: 600, fontSize: '13px', letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: '1rem' }}>
                Company
              </p>
              {[
                { label: 'About',       href: '/about' },
                { label: 'Blog',        href: '/blog' },
                { label: 'Privacy',     href: '/privacy' },
                { label: 'Terms',       href: '/terms' },
              ].map((link) => (
                <div key={link.label}>
                  <Link
                    href={link.href}
                    style={{ color: '#94a3b8', fontSize: '14px', textDecoration: 'none', transition: 'color 0.2s' }}
                    onMouseEnter={(e) => ((e.currentTarget as HTMLElement).style.color = '#f1f5f9')}
                    onMouseLeave={(e) => ((e.currentTarget as HTMLElement).style.color = '#94a3b8')}
                  >
                    {link.label}
                  </Link>
                </div>
              ))}
            </div>

          </div>
        </div>

        {/* Bottom bar */}
        <div
          style={{
            borderTop: '1px solid rgba(255,255,255,0.06)',
          }}
        >
          <div
            className="container mx-auto px-6"
            style={{
              paddingTop: '1.25rem',
              paddingBottom: '1.25rem',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              flexWrap: 'wrap',
              gap: '0.75rem',
            }}
          >
            <p style={{ color: '#475569', fontSize: '13px' }}>
              © {new Date().getFullYear()} IntelliStack. All rights reserved.
            </p>
            <p style={{ color: '#475569', fontSize: '13px' }}>
              Built for the future of Physical AI education.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}
