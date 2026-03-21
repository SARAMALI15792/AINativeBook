'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import { getAuthClient } from '@/lib/auth';

const DOCUSAURUS_URL =
  typeof process !== 'undefined'
    ? process.env.NEXT_PUBLIC_DOCUSAURUS_URL || 'http://localhost:3002/AINativeBook'
    : 'http://localhost:3002/AINativeBook';

/* ─── Data ───────────────────────────────────────────────── */

const stages = [
  {
    number: 1,
    slug: 'stage-1',
    title: 'Foundations',
    subtitle: 'Linux · ROS 2 basics · Workspace',
    completion: 100,
    unlocked: true,
    accent: '#10B981',
    icon: '⬡',
  },
  {
    number: 2,
    slug: 'stage-2',
    title: 'ROS 2 & Simulation',
    subtitle: 'Gazebo · URDF · Nav2',
    completion: 60,
    unlocked: true,
    accent: '#2563EB',
    icon: '⬡',
  },
  {
    number: 3,
    slug: 'stage-3',
    title: 'Perception & Planning',
    subtitle: 'Computer vision · Sensor fusion',
    completion: 0,
    unlocked: false,
    accent: '#6366F1',
    icon: '⬡',
  },
  {
    number: 4,
    slug: 'stage-4',
    title: 'AI Integration',
    subtitle: 'ML models · AI behaviours',
    completion: 0,
    unlocked: false,
    accent: '#8B5CF6',
    icon: '⬡',
  },
  {
    number: 5,
    slug: 'stage-5',
    title: 'Capstone Project',
    subtitle: 'Full autonomous system',
    completion: 0,
    unlocked: false,
    accent: '#F59E0B',
    icon: '⬡',
  },
];

const activity = [
  { time: '2h ago',  text: 'Completed "ROS 2 Publisher / Subscriber" exercise', tag: 'Exercise', color: '#2563EB' },
  { time: '5h ago',  text: 'Earned badge: Navigation Initiate',                 tag: 'Badge',    color: '#F59E0B' },
  { time: '1d ago',  text: 'Finished Stage 1 — Foundations (100%)',             tag: 'Milestone', color: '#10B981' },
  { time: '2d ago',  text: 'AI Tutor session: URDF joint types explained',      tag: 'Tutor',    color: '#6366F1' },
];

const quickActions = [
  { label: 'Continue Learning', href: `${DOCUSAURUS_URL}/stage-2/intro`, primary: true, icon: '→' },
  { label: 'Ask AI Tutor',      href: '/tutor',  primary: false, icon: '✦' },
  { label: 'Take a Quiz',       href: '/quiz',   primary: false, icon: '◈' },
];

/* ─── Keyframes (injected once) ───────────────────────────── */
const CSS = `
  @keyframes db-fade-up {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  @keyframes db-fade-in {
    from { opacity: 0; }
    to   { opacity: 1; }
  }
  @keyframes db-glow-pulse {
    0%, 100% { box-shadow: 0 0 20px rgba(37,99,235,0.15); }
    50%       { box-shadow: 0 0 40px rgba(37,99,235,0.35), 0 0 80px rgba(99,102,241,0.1); }
  }
  @keyframes db-bar-fill {
    from { width: 0%; }
  }
  @keyframes db-dot-blink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.3; }
  }
  @keyframes db-scan {
    0%   { background-position: 0% 0%; }
    100% { background-position: 0% 100%; }
  }

  .db-sidebar-link {
    display: flex; align-items: center; gap: 12px;
    padding: 10px 16px; border-radius: 10px;
    text-decoration: none;
    font-size: 14px; font-weight: 500;
    color: #64748b;
    transition: all 0.2s ease;
    position: relative; cursor: pointer; border: none; background: none; width: 100%; text-align: left;
  }
  .db-sidebar-link:hover, .db-sidebar-link.active {
    background: rgba(99,102,241,0.1);
    color: #f1f5f9;
  }
  .db-sidebar-link.active::before {
    content: '';
    position: absolute; left: 0; top: 20%; bottom: 20%;
    width: 3px; border-radius: 0 3px 3px 0;
    background: linear-gradient(180deg, #4f46e5, #6366f1);
  }

  .db-stage-card {
    flex: 0 0 220px;
    border-radius: 16px;
    padding: 20px;
    cursor: pointer;
    text-decoration: none;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    display: block;
  }
  .db-stage-card:hover {
    transform: translateY(-3px);
  }
  .db-stat-card {
    border-radius: 16px;
    padding: 20px 24px;
    transition: transform 0.2s ease;
  }
  .db-stat-card:hover {
    transform: translateY(-2px);
  }
  .db-action-btn {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 11px 20px; border-radius: 10px;
    font-size: 14px; font-weight: 600;
    text-decoration: none; cursor: pointer; border: none;
    transition: all 0.2s ease;
  }
  .db-action-btn:hover { transform: translateY(-1px); }

  .db-progress-bar {
    height: 100%; border-radius: 4px;
    animation: db-bar-fill 1.2s cubic-bezier(0.25,0.46,0.45,0.94) both;
  }
  .db-live-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: #10B981;
    animation: db-dot-blink 2s ease-in-out infinite;
    flex-shrink: 0;
  }
  .db-card-entry {
    animation: db-fade-up 0.5s ease both;
  }
`;

/* ─── Sub-components ─────────────────────────────────────── */

function SidebarIcon({ d }: { d: string }) {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.8} strokeLinecap="round" strokeLinejoin="round">
      <path d={d} />
    </svg>
  );
}

const NAV_ITEMS = [
  { label: 'Dashboard',   href: '/dashboard',  icon: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6', active: true },
  { label: 'Curriculum',  href: '/curriculum', icon: 'M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2z' },
  { label: 'AI Tutor',    href: '/tutor',      icon: 'M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z' },
  { label: 'Community',   href: '/community',  icon: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z' },
  { label: 'Settings',    href: '/settings',   icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z' },
];

/* Animated XP counter */
function AnimatedNumber({ target, duration = 1400 }: { target: number; duration?: number }) {
  const [val, setVal] = useState(0);
  useEffect(() => {
    const start = performance.now();
    const step = (now: number) => {
      const t = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - t, 3);
      setVal(Math.round(eased * target));
      if (t < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }, [target, duration]);
  return <>{val.toLocaleString()}</>;
}

/* Arc progress ring */
function ProgressRing({ pct, color, size = 80, stroke = 6 }: { pct: number; color: string; size?: number; stroke?: number }) {
  const r = (size - stroke) / 2;
  const circ = 2 * Math.PI * r;
  const dash = (pct / 100) * circ;
  return (
    <svg width={size} height={size} style={{ transform: 'rotate(-90deg)' }}>
      <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth={stroke} />
      <circle
        cx={size / 2} cy={size / 2} r={r} fill="none"
        stroke={color} strokeWidth={stroke}
        strokeDasharray={`${dash} ${circ - dash}`}
        strokeLinecap="round"
        style={{ transition: 'stroke-dasharray 1.2s cubic-bezier(0.25,0.46,0.45,0.94)' }}
      />
    </svg>
  );
}

/* ─── Main component ─────────────────────────────────────── */

export default function DashboardPage() {
  const { session } = useAuth();
  const [time, setTime] = useState('');
  const userName = (session as any)?.user?.name?.split(' ')[0] || 'Learner';

  useEffect(() => {
    const update = () =>
      setTime(new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
    update();
    const t = setInterval(update, 10000);
    return () => clearInterval(t);
  }, []);

  const handleSignOut = async () => {
    const client = getAuthClient();
    await client.signOut();
  };

  return (
    <>
      <style>{CSS}</style>

      <div style={{
        display: 'flex',
        minHeight: '100vh',
        background: '#080810',
        fontFamily: 'var(--font-body, DM Sans, sans-serif)',
        color: '#f1f5f9',
      }}>

        {/* ── Sidebar ───────────────────────────────────────── */}
        <aside style={{
          width: 260,
          flexShrink: 0,
          background: 'rgba(8,8,18,0.97)',
          borderRight: '1px solid rgba(255,255,255,0.06)',
          display: 'flex',
          flexDirection: 'column',
          position: 'sticky',
          top: 0,
          height: '100vh',
          overflowY: 'auto',
          zIndex: 40,
        }}>
          {/* Logo */}
          <div style={{ padding: '24px 20px 20px', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
            <Link href="/" style={{ display: 'flex', alignItems: 'center', gap: 10, textDecoration: 'none' }}>
              <div style={{
                width: 34, height: 34, borderRadius: 9,
                background: 'linear-gradient(135deg, #4f46e5, #6366f1)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                flexShrink: 0,
                boxShadow: '0 0 20px rgba(99,102,241,0.4)',
              }}>
                <span style={{ color: 'white', fontWeight: 800, fontSize: 13, fontFamily: 'var(--font-heading)' }}>IS</span>
              </div>
              <div>
                <div style={{ color: '#f1f5f9', fontWeight: 700, fontSize: 15, fontFamily: 'var(--font-heading)', lineHeight: 1.1 }}>IntelliStack</div>
                <div style={{ color: '#475569', fontSize: 10, letterSpacing: '0.1em', textTransform: 'uppercase' }}>Learning Platform</div>
              </div>
            </Link>
          </div>

          {/* Nav */}
          <nav style={{ flex: 1, padding: '16px 12px' }}>
            <div style={{ fontSize: 10, color: '#334155', letterSpacing: '0.12em', textTransform: 'uppercase', fontWeight: 600, padding: '4px 8px', marginBottom: 6 }}>
              Navigation
            </div>
            {NAV_ITEMS.map((item) => (
              <Link
                key={item.label}
                href={item.href}
                className={`db-sidebar-link${item.active ? ' active' : ''}`}
              >
                <SidebarIcon d={item.icon} />
                {item.label}
              </Link>
            ))}
          </nav>

          {/* User card */}
          <div style={{
            margin: '0 12px 16px',
            background: 'rgba(99,102,241,0.07)',
            border: '1px solid rgba(99,102,241,0.15)',
            borderRadius: 12,
            padding: '14px 16px',
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 10 }}>
              <div style={{
                width: 36, height: 36, borderRadius: '50%',
                background: 'linear-gradient(135deg, #4f46e5, #a78bfa)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: 14, fontWeight: 700, color: 'white', flexShrink: 0,
              }}>
                {userName.charAt(0).toUpperCase()}
              </div>
              <div>
                <div style={{ fontSize: 13, fontWeight: 600, color: '#f1f5f9' }}>{userName}</div>
                <div style={{ fontSize: 11, color: '#475569' }}>Stage 2 · Active</div>
              </div>
            </div>
            <button
              onClick={handleSignOut}
              style={{
                width: '100%', padding: '7px 0', borderRadius: 8,
                background: 'rgba(255,255,255,0.04)',
                border: '1px solid rgba(255,255,255,0.06)',
                color: '#64748b', fontSize: 12, fontWeight: 500, cursor: 'pointer',
                transition: 'all 0.2s',
              }}
              onMouseEnter={e => { (e.currentTarget as HTMLElement).style.background = 'rgba(239,68,68,0.1)'; (e.currentTarget as HTMLElement).style.color = '#ef4444'; (e.currentTarget as HTMLElement).style.borderColor = 'rgba(239,68,68,0.2)'; }}
              onMouseLeave={e => { (e.currentTarget as HTMLElement).style.background = 'rgba(255,255,255,0.04)'; (e.currentTarget as HTMLElement).style.color = '#64748b'; (e.currentTarget as HTMLElement).style.borderColor = 'rgba(255,255,255,0.06)'; }}
            >
              Sign out
            </button>
          </div>
        </aside>

        {/* ── Main content ──────────────────────────────────── */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', minWidth: 0 }}>

          {/* Top bar */}
          <header style={{
            height: 64,
            display: 'flex', alignItems: 'center', justifyContent: 'space-between',
            padding: '0 32px',
            background: 'rgba(8,8,18,0.8)',
            backdropFilter: 'blur(12px)',
            borderBottom: '1px solid rgba(255,255,255,0.05)',
            position: 'sticky', top: 0, zIndex: 30,
          }}>
            <div>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: '#4f46e5', letterSpacing: '0.15em', textTransform: 'uppercase' }}>
                ◈ Mission Control
              </span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 20 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <div className="db-live-dot" />
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: 12, color: '#475569' }}>
                  {time || '––:––'}
                </span>
              </div>
              {/* XP chip */}
              <div style={{
                display: 'flex', alignItems: 'center', gap: 6,
                padding: '5px 12px', borderRadius: 20,
                background: 'rgba(16,185,129,0.08)',
                border: '1px solid rgba(16,185,129,0.2)',
              }}>
                <span style={{ color: '#10B981', fontSize: 11, fontWeight: 700, fontFamily: 'var(--font-mono)' }}>
                  ✦ 1,250 XP
                </span>
              </div>
            </div>
          </header>

          {/* Scrollable page body */}
          <div style={{ flex: 1, overflowY: 'auto', padding: '32px 32px 48px' }}>

            {/* ── Greeting ─────────────────────────────── */}
            <div className="db-card-entry" style={{ marginBottom: 32, animationDelay: '0ms' }}>
              <p style={{ fontFamily: 'var(--font-mono)', fontSize: 12, color: '#4f46e5', letterSpacing: '0.12em', textTransform: 'uppercase', marginBottom: 4 }}>
                Welcome back
              </p>
              <h1 style={{
                fontFamily: 'var(--font-heading)',
                fontSize: 38, fontWeight: 700,
                background: 'linear-gradient(135deg, #f1f5f9 30%, #94a3b8)',
                WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
                lineHeight: 1.1, marginBottom: 6,
              }}>
                {userName}.
              </h1>
              <p style={{ color: '#64748b', fontSize: 15 }}>
                You're 60% through Stage 2. One more push and you unlock Perception &amp; Planning.
              </p>
            </div>

            {/* ── Top row: hero + stats ─────────────────── */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 300px', gap: 20, marginBottom: 20 }}>

              {/* Hero progress card */}
              <div
                className="db-card-entry"
                style={{
                  borderRadius: 20, padding: '28px 32px',
                  background: 'linear-gradient(135deg, rgba(15,15,28,0.95) 0%, rgba(20,14,40,0.9) 100%)',
                  border: '1px solid rgba(99,102,241,0.2)',
                  boxShadow: '0 0 40px rgba(79,70,229,0.08)',
                  animationDelay: '60ms',
                  position: 'relative', overflow: 'hidden',
                }}
              >
                {/* Background hex grid decoration */}
                <div aria-hidden style={{
                  position: 'absolute', inset: 0, opacity: 0.04,
                  backgroundImage: 'radial-gradient(circle, #6366f1 1px, transparent 1px)',
                  backgroundSize: '28px 28px',
                  pointerEvents: 'none',
                }} />

                <div style={{ position: 'relative', display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: 24 }}>
                  <div>
                    <p style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: '#475569', letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: 6 }}>
                      Overall Progress
                    </p>
                    <h2 style={{ fontFamily: 'var(--font-heading)', fontSize: 22, fontWeight: 600, color: '#f1f5f9', marginBottom: 4 }}>
                      Curriculum Journey
                    </h2>
                    <p style={{ color: '#475569', fontSize: 13 }}>2 of 5 stages completed</p>
                  </div>
                  {/* Arc ring */}
                  <div style={{ position: 'relative', flexShrink: 0 }}>
                    <ProgressRing pct={40} color="#6366f1" size={80} stroke={7} />
                    <div style={{
                      position: 'absolute', inset: 0,
                      display: 'flex', alignItems: 'center', justifyContent: 'center',
                      fontFamily: 'var(--font-mono)', fontSize: 15, fontWeight: 700, color: '#f1f5f9',
                    }}>
                      40%
                    </div>
                  </div>
                </div>

                {/* Stage progress bars */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: 10, marginBottom: 24 }}>
                  {stages.map((s) => (
                    <div key={s.number} style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                      <span style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: '#334155', width: 16, textAlign: 'right', flexShrink: 0 }}>
                        {s.number}
                      </span>
                      <div style={{ flex: 1, height: 5, background: 'rgba(255,255,255,0.05)', borderRadius: 4, overflow: 'hidden' }}>
                        <div
                          className="db-progress-bar"
                          style={{ width: `${s.completion}%`, background: `linear-gradient(90deg, ${s.accent}cc, ${s.accent})` }}
                        />
                      </div>
                      <span style={{ fontFamily: 'var(--font-mono)', fontSize: 10, color: s.unlocked ? s.accent : '#1e293b', width: 30, textAlign: 'right', flexShrink: 0 }}>
                        {s.completion}%
                      </span>
                    </div>
                  ))}
                </div>

                {/* CTA buttons */}
                <div style={{ display: 'flex', gap: 10 }}>
                  {quickActions.map((a) => (
                    <Link
                      key={a.label}
                      href={a.href}
                      className="db-action-btn"
                      style={a.primary ? {
                        background: 'linear-gradient(135deg, #4f46e5, #6366f1)',
                        color: 'white',
                        boxShadow: '0 0 20px rgba(99,102,241,0.3)',
                      } : {
                        background: 'rgba(255,255,255,0.04)',
                        border: '1px solid rgba(255,255,255,0.08)',
                        color: '#94a3b8',
                      }}
                    >
                      <span style={{ fontSize: 13 }}>{a.icon}</span>
                      {a.label}
                    </Link>
                  ))}
                </div>
              </div>

              {/* Stats column */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>

                {/* Streak */}
                <div
                  className="db-stat-card db-card-entry"
                  style={{
                    background: 'rgba(245,158,11,0.06)',
                    border: '1px solid rgba(245,158,11,0.18)',
                    animationDelay: '80ms',
                  }}
                >
                  <div style={{ fontSize: 11, color: '#92400e', letterSpacing: '0.1em', textTransform: 'uppercase', fontFamily: 'var(--font-mono)', marginBottom: 8 }}>
                    🔥 Daily Streak
                  </div>
                  <div style={{ display: 'flex', alignItems: 'baseline', gap: 4 }}>
                    <span style={{ fontFamily: 'var(--font-heading)', fontSize: 42, fontWeight: 700, color: '#F59E0B', lineHeight: 1 }}>7</span>
                    <span style={{ color: '#78350f', fontSize: 13 }}>days</span>
                  </div>
                  <p style={{ fontSize: 12, color: '#78350f', marginTop: 6 }}>Best: 14 days · Keep it up!</p>
                </div>

                {/* XP */}
                <div
                  className="db-stat-card db-card-entry"
                  style={{
                    background: 'rgba(16,185,129,0.06)',
                    border: '1px solid rgba(16,185,129,0.18)',
                    animationDelay: '120ms',
                  }}
                >
                  <div style={{ fontSize: 11, color: '#065f46', letterSpacing: '0.1em', textTransform: 'uppercase', fontFamily: 'var(--font-mono)', marginBottom: 8 }}>
                    ✦ XP Points
                  </div>
                  <div style={{ display: 'flex', alignItems: 'baseline', gap: 4 }}>
                    <span style={{ fontFamily: 'var(--font-heading)', fontSize: 36, fontWeight: 700, color: '#10B981', lineHeight: 1 }}>
                      <AnimatedNumber target={1250} />
                    </span>
                    <span style={{ color: '#064e3b', fontSize: 13 }}>xp</span>
                  </div>
                  <p style={{ fontSize: 12, color: '#064e3b', marginTop: 6 }}>+250 this week</p>
                </div>

                {/* Badges */}
                <div
                  className="db-stat-card db-card-entry"
                  style={{
                    background: 'rgba(99,102,241,0.06)',
                    border: '1px solid rgba(99,102,241,0.18)',
                    animationDelay: '160ms',
                  }}
                >
                  <div style={{ fontSize: 11, color: '#3730a3', letterSpacing: '0.1em', textTransform: 'uppercase', fontFamily: 'var(--font-mono)', marginBottom: 8 }}>
                    🏅 Badges
                  </div>
                  <div style={{ display: 'flex', alignItems: 'baseline', gap: 4 }}>
                    <span style={{ fontFamily: 'var(--font-heading)', fontSize: 42, fontWeight: 700, color: '#818cf8', lineHeight: 1 }}>3</span>
                    <span style={{ color: '#3730a3', fontSize: 13 }}>earned</span>
                  </div>
                  <p style={{ fontSize: 12, color: '#3730a3', marginTop: 6 }}>ROS2 Init · Nav Init · Stage 1</p>
                </div>

              </div>
            </div>

            {/* ── Stage cards row ───────────────────────── */}
            <div className="db-card-entry" style={{ marginBottom: 20, animationDelay: '180ms' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 16 }}>
                <div>
                  <h2 style={{ fontFamily: 'var(--font-heading)', fontSize: 18, fontWeight: 600, color: '#f1f5f9', marginBottom: 2 }}>
                    Learning Stages
                  </h2>
                  <p style={{ color: '#475569', fontSize: 13 }}>Your path through Physical AI</p>
                </div>
                <Link href="/curriculum" style={{ fontSize: 13, color: '#6366f1', textDecoration: 'none', fontWeight: 500, display: 'flex', alignItems: 'center', gap: 4 }}>
                  Full curriculum →
                </Link>
              </div>

              <div style={{ display: 'flex', gap: 14, overflowX: 'auto', paddingBottom: 8 }}>
                {stages.map((s, i) => {
                  const card = (
                    <div
                      className="db-stage-card"
                      style={{
                        background: s.unlocked
                          ? `linear-gradient(160deg, rgba(22,22,34,0.9), rgba(13,13,20,0.95))`
                          : 'rgba(10,10,16,0.7)',
                        border: `1px solid ${s.unlocked ? `${s.accent}30` : 'rgba(255,255,255,0.05)'}`,
                        opacity: s.unlocked ? 1 : 0.45,
                        boxShadow: s.completion === 100
                          ? `0 0 20px ${s.accent}20`
                          : s.completion > 0
                          ? `0 0 12px ${s.accent}10`
                          : 'none',
                      }}
                    >
                      {/* Stage number badge */}
                      <div style={{
                        display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
                        width: 36, height: 36, borderRadius: 10,
                        background: s.unlocked ? `${s.accent}18` : 'rgba(255,255,255,0.04)',
                        border: `1px solid ${s.unlocked ? `${s.accent}35` : 'rgba(255,255,255,0.06)'}`,
                        fontFamily: 'var(--font-mono)', fontSize: 14, fontWeight: 700,
                        color: s.unlocked ? s.accent : '#1e293b',
                        marginBottom: 14,
                      }}>
                        {s.unlocked ? s.number : '🔒'}
                      </div>

                      {/* Completion ring */}
                      {s.unlocked && (
                        <div style={{ float: 'right', marginTop: -8 }}>
                          <div style={{ position: 'relative', display: 'inline-block' }}>
                            <ProgressRing pct={s.completion} color={s.accent} size={40} stroke={4} />
                            <div style={{
                              position: 'absolute', inset: 0,
                              display: 'flex', alignItems: 'center', justifyContent: 'center',
                              fontFamily: 'var(--font-mono)', fontSize: 8, fontWeight: 700,
                              color: s.completion > 0 ? s.accent : '#334155',
                            }}>
                              {s.completion}%
                            </div>
                          </div>
                        </div>
                      )}

                      <div style={{ clear: 'both' }}>
                        <h3 style={{
                          fontFamily: 'var(--font-heading)', fontSize: 14, fontWeight: 600,
                          color: s.unlocked ? '#f1f5f9' : '#334155',
                          marginBottom: 4, lineHeight: 1.3,
                        }}>
                          {s.title}
                        </h3>
                        <p style={{ fontSize: 11, color: s.unlocked ? '#475569' : '#1e293b', lineHeight: 1.5 }}>
                          {s.subtitle}
                        </p>
                      </div>

                      {s.unlocked && (
                        <div style={{
                          marginTop: 14, paddingTop: 12,
                          borderTop: `1px solid rgba(255,255,255,0.05)`,
                          fontSize: 11, color: s.accent, fontWeight: 600,
                          display: 'flex', alignItems: 'center', gap: 4,
                          fontFamily: 'var(--font-mono)',
                        }}>
                          {s.completion === 100 ? '✓ Complete' : s.completion > 0 ? '→ Continue' : '→ Start'}
                        </div>
                      )}
                    </div>
                  );

                  return s.unlocked ? (
                    <Link
                      key={s.number}
                      href={`${DOCUSAURUS_URL}/${s.slug}/intro`}
                      style={{ textDecoration: 'none', display: 'block', flex: '0 0 210px' }}
                    >
                      {card}
                    </Link>
                  ) : (
                    <div key={s.number} style={{ flex: '0 0 210px' }}>{card}</div>
                  );
                })}
              </div>
            </div>

            {/* ── Bottom row: activity + next lesson ───── */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>

              {/* Activity feed */}
              <div
                className="db-card-entry"
                style={{
                  borderRadius: 18, padding: '24px',
                  background: 'rgba(12,12,20,0.9)',
                  border: '1px solid rgba(255,255,255,0.06)',
                  animationDelay: '240ms',
                }}
              >
                <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: 16, fontWeight: 600, color: '#f1f5f9', marginBottom: 18 }}>
                  Recent Activity
                </h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                  {activity.map((a, i) => (
                    <div
                      key={i}
                      style={{
                        display: 'flex', alignItems: 'flex-start', gap: 12,
                        padding: '12px 0',
                        borderBottom: i < activity.length - 1 ? '1px solid rgba(255,255,255,0.04)' : 'none',
                      }}
                    >
                      <div style={{
                        width: 6, height: 6, borderRadius: '50%',
                        background: a.color, flexShrink: 0, marginTop: 6,
                        boxShadow: `0 0 6px ${a.color}`,
                      }} />
                      <div style={{ flex: 1, minWidth: 0 }}>
                        <p style={{ fontSize: 13, color: '#cbd5e1', lineHeight: 1.5, marginBottom: 4 }}>{a.text}</p>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                          <span style={{
                            fontSize: 10, fontWeight: 600,
                            color: a.color,
                            padding: '2px 7px', borderRadius: 20,
                            background: `${a.color}15`,
                            fontFamily: 'var(--font-mono)',
                          }}>
                            {a.tag}
                          </span>
                          <span style={{ fontSize: 11, color: '#334155', fontFamily: 'var(--font-mono)' }}>{a.time}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Next lesson card */}
              <div
                className="db-card-entry"
                style={{
                  borderRadius: 18, padding: '24px',
                  background: 'linear-gradient(150deg, rgba(15,15,30,0.95), rgba(10,8,25,0.98))',
                  border: '1px solid rgba(99,102,241,0.2)',
                  animationDelay: '280ms',
                  position: 'relative', overflow: 'hidden',
                  animation: 'db-card-entry 0.5s ease both, db-glow-pulse 4s ease-in-out 1s infinite',
                }}
              >
                {/* Glow orb decoration */}
                <div aria-hidden style={{
                  position: 'absolute', right: -40, bottom: -40,
                  width: 160, height: 160, borderRadius: '50%',
                  background: 'radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%)',
                  pointerEvents: 'none',
                }} />

                <div style={{ position: 'relative' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 16 }}>
                    <div style={{
                      padding: '3px 10px', borderRadius: 20,
                      background: 'rgba(37,99,235,0.15)',
                      border: '1px solid rgba(37,99,235,0.3)',
                      fontSize: 10, color: '#2563EB', fontWeight: 700,
                      fontFamily: 'var(--font-mono)', letterSpacing: '0.08em',
                    }}>
                      UP NEXT
                    </div>
                    <span style={{ fontSize: 11, color: '#334155', fontFamily: 'var(--font-mono)' }}>Stage 2</span>
                  </div>

                  <h3 style={{
                    fontFamily: 'var(--font-heading)', fontSize: 20, fontWeight: 700,
                    color: '#f1f5f9', marginBottom: 8, lineHeight: 1.3,
                  }}>
                    Nav2 Stack & Path Planning
                  </h3>
                  <p style={{ fontSize: 13, color: '#475569', lineHeight: 1.6, marginBottom: 20 }}>
                    Configure the Navigation2 stack, define cost maps, and implement goal-based autonomous navigation with a differential-drive robot.
                  </p>

                  <div style={{ display: 'flex', gap: 12, marginBottom: 20 }}>
                    {[
                      { label: '45 min', icon: '◷' },
                      { label: 'Intermediate', icon: '◈' },
                      { label: 'ROS 2 · Nav2', icon: '⬡' },
                    ].map((m) => (
                      <div key={m.label} style={{
                        display: 'flex', alignItems: 'center', gap: 5,
                        fontSize: 11, color: '#475569', fontFamily: 'var(--font-mono)',
                      }}>
                        <span style={{ color: '#6366f1' }}>{m.icon}</span>
                        {m.label}
                      </div>
                    ))}
                  </div>

                  <Link
                    href={`${DOCUSAURUS_URL}/stage-2/nav2`}
                    className="db-action-btn"
                    style={{
                      background: 'linear-gradient(135deg, #4f46e5, #6366f1)',
                      color: 'white',
                      boxShadow: '0 0 24px rgba(99,102,241,0.35)',
                      fontSize: 14, fontWeight: 600,
                    }}
                  >
                    Start Lesson →
                  </Link>
                </div>
              </div>

            </div>
          </div>
        </div>
      </div>
    </>
  );
}
