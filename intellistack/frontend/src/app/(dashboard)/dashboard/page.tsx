'use client';

import { useEffect } from 'react';
import Link from 'next/link';
import { useUserStore } from '@/stores/userStore';
import { useLearningStore } from '@/stores/learningStore';

export default function DashboardPage() {
  const user = useUserStore((state) => state.user);
  const { progress, fetchProgress } = useLearningStore();

  useEffect(() => {
    fetchProgress();
  }, [fetchProgress]);

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg p-6 text-white">
        <h1 className="text-3xl font-bold mb-2">
          Welcome back, {user?.name?.split(' ')[0] || 'Student'}! 👋
        </h1>
        <p className="text-blue-100">
          Ready to continue your journey in Physical AI and Humanoid Robotics?
        </p>
      </div>

      {/* Progress Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <div className="text-slate-400 text-sm mb-2">Overall Progress</div>
          <div className="text-3xl font-bold text-white mb-2">
            {progress?.overall_percentage.toFixed(0) || 0}%
          </div>
          <div className="w-full bg-slate-700 rounded-full h-2">
            <div
              className="bg-blue-500 h-2 rounded-full transition-all"
              style={{ width: `${progress?.overall_percentage || 0}%` }}
            />
          </div>
        </div>

        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <div className="text-slate-400 text-sm mb-2">Time Invested</div>
          <div className="text-3xl font-bold text-white">
            {Math.floor((progress?.total_time_spent_minutes || 0) / 60)}h
          </div>
          <div className="text-slate-400 text-sm mt-2">
            {(progress?.total_time_spent_minutes || 0) % 60}m
          </div>
        </div>

        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <div className="text-slate-400 text-sm mb-2">Current Stage</div>
          <div className="text-xl font-bold text-white">
            {progress?.current_stage_id ? `Stage ${progress.current_stage_id}` : 'Not Started'}
          </div>
          <div className="text-slate-400 text-sm mt-2">
            Keep up the great work!
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
        <h2 className="text-xl font-bold text-white mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Link
            href="/learn"
            className="bg-slate-700 hover:bg-slate-600 p-4 rounded-lg transition-colors"
          >
            <div className="text-2xl mb-2">📚</div>
            <div className="font-medium text-white">Continue Learning</div>
            <div className="text-sm text-slate-400 mt-1">
              Resume your progress
            </div>
          </Link>

          <Link
            href="/assessments"
            className="bg-slate-700 hover:bg-slate-600 p-4 rounded-lg transition-colors"
          >
            <div className="text-2xl mb-2">📝</div>
            <div className="font-medium text-white">Take Assessment</div>
            <div className="text-sm text-slate-400 mt-1">
              Test your knowledge
            </div>
          </Link>

          <Link
            href="/ai/chatbot"
            className="bg-slate-700 hover:bg-slate-600 p-4 rounded-lg transition-colors"
          >
            <div className="text-2xl mb-2">🤖</div>
            <div className="font-medium text-white">AI Assistant</div>
            <div className="text-sm text-slate-400 mt-1">
              Get help anytime
            </div>
          </Link>

          <Link
            href="/community"
            className="bg-slate-700 hover:bg-slate-600 p-4 rounded-lg transition-colors"
          >
            <div className="text-2xl mb-2">👥</div>
            <div className="font-medium text-white">Community</div>
            <div className="text-sm text-slate-400 mt-1">
              Connect with peers
            </div>
          </Link>
        </div>
      </div>

      {/* Learning Path Preview */}
      <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
        <h2 className="text-xl font-bold text-white mb-4">Your Learning Path</h2>
        <div className="space-y-3">
          {[
            { stage: 1, name: 'Foundations', status: 'completed', percent: 100 },
            { stage: 2, name: 'ROS 2 & Simulation', status: 'in_progress', percent: 45 },
            { stage: 3, name: 'Perception & Planning', status: 'locked', percent: 0 },
            { stage: 4, name: 'AI Integration', status: 'locked', percent: 0 },
            { stage: 5, name: 'Capstone Project', status: 'locked', percent: 0 },
          ].map((stage) => (
            <div key={stage.stage} className="flex items-center gap-4">
              <div
                className={`w-10 h-10 rounded-full flex items-center justify-center font-bold ${
                  stage.status === 'completed'
                    ? 'bg-green-600 text-white'
                    : stage.status === 'in_progress'
                    ? 'bg-blue-600 text-white'
                    : 'bg-slate-700 text-slate-500'
                }`}
              >
                {stage.stage}
              </div>
              <div className="flex-1">
                <div className="text-white font-medium">{stage.name}</div>
                <div className="w-full bg-slate-700 rounded-full h-1.5 mt-1">
                  <div
                    className={`h-1.5 rounded-full ${
                      stage.status === 'completed'
                        ? 'bg-green-500'
                        : stage.status === 'in_progress'
                        ? 'bg-blue-500'
                        : 'bg-slate-600'
                    }`}
                    style={{ width: `${stage.percent}%` }}
                  />
                </div>
              </div>
              <div className="text-slate-400 text-sm">{stage.percent}%</div>
            </div>
          ))}
        </div>
        <Link
          href="/learn"
          className="mt-4 inline-block px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
        >
          View Full Learning Path →
        </Link>
      </div>
    </div>
  );
}
