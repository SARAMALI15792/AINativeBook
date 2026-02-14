'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useAuth } from '@/hooks/useAuth';
import { cn } from '@/lib/utils';
import { Settings, ExternalLink } from 'lucide-react';

export default function ProfilePage() {
  const { user } = useAuth();
  const [isEditing, setIsEditing] = useState(false);

  // Mock progress data
  const progress = {
    overall_percentage: 45,
    current_stage_id: 2,
    total_time_spent_minutes: 360,
  };

  const earnedBadges = [
    {
      id: '1',
      name: 'Foundation Master',
      description: 'Completed Stage 1: Foundations',
      icon: '🎓',
      earned_at: '2026-01-15T10:00:00Z',
    },
    {
      id: '2',
      name: 'ROS 2 Explorer',
      description: 'Started Stage 2: ROS 2 & Simulation',
      icon: '🤖',
      earned_at: '2026-02-01T14:30:00Z',
    },
  ];

  const lockedBadges = [
    { id: '3', name: 'Perception Specialist', icon: '👁️' },
    { id: '4', name: 'AI Integrator', icon: '🧠' },
    { id: '5', name: 'Capstone Graduate', icon: '🏆' },
  ];

  return (
    <div className="space-y-8">
      {/* Profile Header */}
      <div className="bg-gradient-to-r from-primary via-primary-400 to-primary rounded-xl p-8 text-white relative overflow-hidden">
        <div className="absolute inset-0 opacity-10"
          style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
          }}
        />
        <div className="relative flex items-start justify-between">
          <div className="flex items-center gap-6">
            <div className="w-24 h-24 rounded-full bg-white/20 flex items-center justify-center text-4xl font-bold backdrop-blur border-4 border-white/30">
              {user?.name?.charAt(0).toUpperCase() || 'U'}
            </div>
            <div>
              <h1 className="text-3xl font-bold font-serif mb-2">{user?.name || 'User'}</h1>
              <p className="text-white/70 mb-1">{user?.email || ''}</p>
              <div className="flex items-center gap-4 text-sm text-white/80">
                <span>{earnedBadges.length} / 5 stages completed</span>
                <span>{Math.floor(progress.total_time_spent_minutes / 60)}h invested</span>
              </div>
            </div>
          </div>
          <button
            onClick={() => setIsEditing(!isEditing)}
            className="px-4 py-2 bg-white/20 hover:bg-white/30 rounded-lg font-medium transition-colors flex items-center gap-2"
          >
            <Settings className="w-4 h-4" />
            Edit Profile
          </button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-card border border-border rounded-xl p-5 text-center">
          <p className="text-3xl font-bold text-foreground">{progress.overall_percentage}%</p>
          <p className="text-sm text-muted-foreground mt-1">Overall Progress</p>
        </div>
        <div className="bg-card border border-border rounded-xl p-5 text-center">
          <p className="text-3xl font-bold text-foreground">{earnedBadges.length}</p>
          <p className="text-sm text-muted-foreground mt-1">Badges Earned</p>
        </div>
        <div className="bg-card border border-border rounded-xl p-5 text-center">
          <p className="text-3xl font-bold text-foreground">
            {Math.floor(progress.total_time_spent_minutes / 60)}
          </p>
          <p className="text-sm text-muted-foreground mt-1">Hours Learned</p>
        </div>
        <div className="bg-card border border-border rounded-xl p-5 text-center">
          <p className="text-3xl font-bold text-foreground">
            {progress.current_stage_id}
          </p>
          <p className="text-sm text-muted-foreground mt-1">Current Stage</p>
        </div>
      </div>

      {/* Learning Path Progress */}
      <div className="bg-card border border-border rounded-xl p-6">
        <h2 className="text-xl font-bold text-foreground font-serif mb-6">Learning Path</h2>
        <div className="space-y-3">
          {[
            { num: 1, name: 'Foundations' },
            { num: 2, name: 'ROS 2 & Simulation' },
            { num: 3, name: 'Perception & Planning' },
            { num: 4, name: 'AI Integration' },
            { num: 5, name: 'Capstone Project' },
          ].map((stage) => {
            const isCompleted = stage.num <= earnedBadges.length;
            const isCurrent = stage.num === earnedBadges.length + 1;
            return (
              <div key={stage.num} className="flex items-center gap-3">
                <div
                  className={cn(
                    'w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold',
                    isCompleted && 'bg-green-100 text-green-700 border-2 border-green-300',
                    isCurrent && 'bg-amber-100 text-amber-700 border-2 border-amber-300',
                    !isCompleted && !isCurrent && 'bg-muted text-muted-foreground border-2 border-border'
                  )}
                >
                  {isCompleted ? '✓' : stage.num}
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-foreground m-0">{stage.name}</p>
                  <div className="h-1.5 bg-muted rounded-full overflow-hidden mt-1">
                    <div
                      className={cn(
                        'h-full transition-all rounded-full',
                        isCompleted && 'bg-green-500 w-full',
                        isCurrent && 'bg-amber-500 w-1/2',
                        !isCompleted && !isCurrent && 'w-0'
                      )}
                    />
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Achievements */}
      <div className="bg-card border border-border rounded-xl p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-foreground font-serif">Achievements</h2>
          <span className="text-sm text-muted-foreground">
            {earnedBadges.length} of {earnedBadges.length + lockedBadges.length} earned
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
          {earnedBadges.map((badge) => (
            <div key={badge.id} className="text-center p-4 bg-amber-50 border border-amber-200 rounded-xl">
              <div className="text-3xl mb-2">{badge.icon}</div>
              <p className="text-sm font-semibold text-foreground m-0">{badge.name}</p>
              <p className="text-xs text-muted-foreground mt-1 m-0">
                {badge.earned_at && new Date(badge.earned_at).toLocaleDateString()}
              </p>
            </div>
          ))}
          {lockedBadges.map((badge) => (
            <div key={badge.id} className="text-center p-4 bg-muted/50 border border-border rounded-xl opacity-60">
              <div className="text-3xl mb-2 grayscale">{badge.icon}</div>
              <p className="text-sm font-semibold text-muted-foreground m-0">{badge.name}</p>
              <p className="text-xs text-muted-foreground mt-1 m-0">Locked</p>
            </div>
          ))}
        </div>
      </div>

      {/* Connected Accounts */}
      <div className="bg-card border border-border rounded-xl p-6">
        <h2 className="text-xl font-bold text-foreground font-serif mb-6">Connected Accounts</h2>
        <div className="space-y-3">
          <div className="flex items-center justify-between p-4 bg-background border border-border rounded-lg">
            <div className="flex items-center gap-3">
              <svg className="w-5 h-5" viewBox="0 0 24 24">
                <path
                  d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"
                  fill="#4285F4"
                />
                <path
                  d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                  fill="#34A853"
                />
                <path
                  d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                  fill="#FBBC05"
                />
                <path
                  d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                  fill="#EA4335"
                />
              </svg>
              <div>
                <p className="text-sm font-medium text-foreground m-0">Google</p>
                <p className="text-xs text-muted-foreground m-0">Not connected</p>
              </div>
            </div>
            <button className="px-3 py-1.5 text-sm font-medium text-primary border border-primary/30 rounded-lg hover:bg-primary/5 transition-colors flex items-center gap-1">
              <ExternalLink className="w-3.5 h-3.5" />
              Connect
            </button>
          </div>

          <div className="flex items-center justify-between p-4 bg-background border border-border rounded-lg">
            <div className="flex items-center gap-3">
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
              </svg>
              <div>
                <p className="text-sm font-medium text-foreground m-0">GitHub</p>
                <p className="text-xs text-muted-foreground m-0">Not connected</p>
              </div>
            </div>
            <button className="px-3 py-1.5 text-sm font-medium text-primary border border-primary/30 rounded-lg hover:bg-primary/5 transition-colors flex items-center gap-1">
              <ExternalLink className="w-3.5 h-3.5" />
              Connect
            </button>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-card border border-border rounded-xl p-6">
        <h2 className="text-xl font-bold text-foreground font-serif mb-6">Recent Activity</h2>
        <div className="space-y-4">
          {earnedBadges.map((badge) => (
            <div key={badge.id} className="flex items-center gap-4 p-4 bg-background border border-border rounded-lg">
              <div className="w-12 h-12 rounded-full bg-amber-100 flex items-center justify-center text-2xl border-2 border-amber-300">
                {badge.icon}
              </div>
              <div className="flex-1">
                <p className="font-medium text-foreground m-0">{badge.name}</p>
                <p className="text-sm text-muted-foreground m-0">
                  {badge.earned_at && new Date(badge.earned_at).toLocaleDateString()}
                </p>
              </div>
              <div className="text-green-600 text-sm font-medium">Completed</div>
            </div>
          ))}

          {earnedBadges.length === 0 && (
            <div className="text-center py-8">
              <p className="text-muted-foreground">No activity yet.</p>
              <Link
                href="/learn"
                className="inline-block mt-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:bg-primary-600 transition-colors"
              >
                Start Learning
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
