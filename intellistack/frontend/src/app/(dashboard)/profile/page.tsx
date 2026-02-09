'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useUserStore } from '@/stores/userStore';
import { useLearningStore } from '@/stores/learningStore';
import { BadgeGrid, Badge } from '@/components/learning/BadgeDisplay';
import { CircularProgress } from '@/components/learning/ProgressBar';
import { CompactPathProgress } from '@/components/learning/LearningPathVisualization';

export default function ProfilePage() {
  const user = useUserStore((state) => state.user);
  const { progress, badges, certificate, fetchBadges, fetchCertificate } = useLearningStore();
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    fetchBadges();
    fetchCertificate();
  }, [fetchBadges, fetchCertificate]);

  // Mock data for demonstration
  const earnedBadges: Badge[] = [
    {
      id: '1',
      name: 'Foundation Master',
      description: 'Completed Stage 1: Foundations',
      icon: '🎓',
      earned_at: '2026-01-15T10:00:00Z',
      stage_id: '1',
    },
    {
      id: '2',
      name: 'ROS 2 Expert',
      description: 'Completed Stage 2: ROS 2 & Simulation',
      icon: '🤖',
      earned_at: '2026-02-01T14:30:00Z',
      stage_id: '2',
    },
  ];

  const lockedBadges: Badge[] = [
    {
      id: '3',
      name: 'Perception Specialist',
      description: 'Complete Stage 3: Perception & Planning',
      icon: '👁️',
      stage_id: '3',
    },
    {
      id: '4',
      name: 'AI Integrator',
      description: 'Complete Stage 4: AI Integration',
      icon: '🧠',
      stage_id: '4',
    },
    {
      id: '5',
      name: 'Capstone Graduate',
      description: 'Complete Stage 5: Capstone Project',
      icon: '🏆',
      stage_id: '5',
    },
  ];

  return (
    <div className="space-y-8">
      {/* Profile Header */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg p-8 text-white">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-6">
            {/* Avatar */}
            <div className="w-24 h-24 rounded-full bg-white/20 flex items-center justify-center text-4xl font-bold backdrop-blur">
              {user?.name?.charAt(0).toUpperCase()}
            </div>

            {/* Info */}
            <div>
              <h1 className="text-3xl font-bold mb-2">{user?.name}</h1>
              <p className="text-blue-100 mb-1">{user?.email}</p>
              <div className="flex items-center gap-4 text-sm">
                <span className="flex items-center gap-1">
                  <span>📚</span>
                  <span>{earnedBadges.length} / 5 stages completed</span>
                </span>
                <span className="flex items-center gap-1">
                  <span>⏱️</span>
                  <span>{Math.floor((progress?.total_time_spent_minutes || 0) / 60)}h invested</span>
                </span>
              </div>
            </div>
          </div>

          <button
            onClick={() => setIsEditing(!isEditing)}
            className="px-4 py-2 bg-white/20 hover:bg-white/30 rounded-lg font-medium transition-colors"
          >
            Edit Profile
          </button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-slate-800 border border-slate-700 rounded-lg p-6 text-center">
          <div className="mb-4">
            <CircularProgress percentage={progress?.overall_percentage || 0} size={80} />
          </div>
          <div className="text-slate-400 text-sm">Overall Progress</div>
        </div>

        <div className="bg-slate-800 border border-slate-700 rounded-lg p-6 text-center">
          <div className="text-4xl font-bold text-white mb-2">{earnedBadges.length}</div>
          <div className="text-slate-400 text-sm">Badges Earned</div>
        </div>

        <div className="bg-slate-800 border border-slate-700 rounded-lg p-6 text-center">
          <div className="text-4xl font-bold text-white mb-2">
            {Math.floor((progress?.total_time_spent_minutes || 0) / 60)}
          </div>
          <div className="text-slate-400 text-sm">Hours Learned</div>
        </div>

        <div className="bg-slate-800 border border-slate-700 rounded-lg p-6 text-center">
          <div className="text-4xl font-bold text-white mb-2">
            {progress?.current_stage_id || 1}
          </div>
          <div className="text-slate-400 text-sm">Current Stage</div>
        </div>
      </div>

      {/* Learning Path Progress */}
      <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
        <h2 className="text-2xl font-bold text-white mb-6">Learning Path</h2>
        <CompactPathProgress
          totalStages={5}
          completedStages={earnedBadges.length}
          currentStage={progress?.current_stage_id || 1}
        />
      </div>

      {/* Badges Section */}
      <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-white">Achievements</h2>
          <span className="text-slate-400 text-sm">
            {earnedBadges.length} of {earnedBadges.length + lockedBadges.length} earned
          </span>
        </div>

        <BadgeGrid badges={earnedBadges} lockedBadges={lockedBadges} columns={5} />

        {earnedBadges.length === 0 && (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🎯</div>
            <p className="text-slate-400 mb-4">No badges earned yet</p>
            <Link
              href="/learn"
              className="inline-block px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors"
            >
              Start Learning to Earn Badges
            </Link>
          </div>
        )}
      </div>

      {/* Certificate Section */}
      {certificate ? (
        <div className="bg-gradient-to-r from-yellow-600 to-orange-600 rounded-lg p-8 text-white">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold mb-2">🎓 Certificate of Completion</h2>
              <p className="text-yellow-100 mb-1">
                Congratulations! You've completed the IntelliStack program.
              </p>
              <p className="text-sm text-yellow-200">
                Issued: {new Date(certificate.issued_at).toLocaleDateString()}
              </p>
            </div>
            <button className="px-6 py-3 bg-white text-orange-600 font-bold rounded-lg hover:bg-yellow-50 transition-colors">
              Download Certificate
            </button>
          </div>
        </div>
      ) : earnedBadges.length === 5 ? (
        <div className="bg-slate-800 border-2 border-dashed border-slate-700 rounded-lg p-8 text-center">
          <div className="text-6xl mb-4">🎓</div>
          <h3 className="text-xl font-bold text-white mb-2">Almost There!</h3>
          <p className="text-slate-400 mb-4">
            Complete your capstone project to receive your certificate
          </p>
          <Link
            href="/learn/stage-5"
            className="inline-block px-6 py-3 bg-yellow-600 hover:bg-yellow-700 text-white font-medium rounded-lg transition-colors"
          >
            Start Capstone Project
          </Link>
        </div>
      ) : (
        <div className="bg-slate-800 border border-slate-700 rounded-lg p-8 text-center">
          <div className="text-6xl mb-4">🎯</div>
          <h3 className="text-xl font-bold text-white mb-2">Keep Going!</h3>
          <p className="text-slate-400">
            Complete all 5 stages and your capstone project to earn your certificate
          </p>
        </div>
      )}

      {/* Activity Timeline */}
      <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
        <h2 className="text-2xl font-bold text-white mb-6">Recent Activity</h2>
        <div className="space-y-4">
          {earnedBadges.map((badge) => (
            <div key={badge.id} className="flex items-center gap-4 p-4 bg-slate-900 rounded-lg">
              <div className="w-12 h-12 rounded-full bg-yellow-600 flex items-center justify-center text-2xl">
                {badge.icon}
              </div>
              <div className="flex-1">
                <p className="text-white font-medium">{badge.name}</p>
                <p className="text-sm text-slate-400">
                  {badge.earned_at && new Date(badge.earned_at).toLocaleDateString()}
                </p>
              </div>
              <div className="text-green-400 text-sm font-medium">Completed</div>
            </div>
          ))}

          {earnedBadges.length === 0 && (
            <p className="text-center text-slate-400 py-8">No activity yet. Start learning!</p>
          )}
        </div>
      </div>

      {/* Badge Notification */}
      {showBadgeNotification && earnedBadge && (
        <BadgeNotification
          badge={earnedBadge}
          onClose={() => setShowBadgeNotification(false)}
        />
      )}
    </div>
  );
}
