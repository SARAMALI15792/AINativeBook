'use client';

import Link from 'next/link';
import { useAuth } from '@/hooks/useAuth';
import { cn } from '@/lib/utils';

export default function DashboardPage() {
  const { user } = useAuth();

  // Learning stages data
  const stages = [
    { stage: 1, name: 'Foundations', status: 'completed', percent: 100, icon: '📐', color: 'emerald' },
    { stage: 2, name: 'ROS 2 & Simulation', status: 'in_progress', percent: 45, icon: '🤖', color: 'amber' },
    { stage: 3, name: 'Perception & Planning', status: 'locked', percent: 0, icon: '👁️', color: 'slate' },
    { stage: 4, name: 'AI Integration', status: 'locked', percent: 0, icon: '🧠', color: 'slate' },
    { stage: 5, name: 'Capstone Project', status: 'locked', percent: 0, icon: '🎓', color: 'slate' },
  ];

  const quickActions = [
    { href: '/learn', icon: '📚', title: 'Continue Learning', desc: 'Resume your progress', color: 'blue' },
    { href: '/assessments', icon: '✏️', title: 'Take Assessment', desc: 'Test your knowledge', color: 'purple' },
    { href: '/ai/chatbot', icon: '🎓', title: 'AI Tutor', desc: 'Get help anytime', color: 'amber' },
    { href: '/community', icon: '👥', title: 'Community', desc: 'Connect with peers', color: 'green' },
  ];

  // Mock progress
  const progress = {
    overall_percentage: 45,
    total_time_spent_minutes: 360,
    current_stage_id: 2,
  };

  return (
    <div className="space-y-8">
      {/* Welcome Banner */}
      <div className="relative overflow-hidden rounded-xl bg-gradient-to-r from-primary via-primary-400 to-primary p-8 text-white shadow-lg border border-primary-600">
        <div className="absolute inset-0 opacity-10"
          style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
          }}
        />
        <div className="relative">
          <p className="text-primary-100 text-sm font-medium mb-1">Welcome back to your learning journey</p>
          <h1 className="text-3xl font-bold mb-2 font-serif">
            Hello, {user?.name?.split(' ')[0] || 'Student'}!
          </h1>
          <p className="text-primary-200 max-w-xl">
            Ready to continue mastering Physical AI and Humanoid Robotics? You&apos;re making great progress!
          </p>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard
          title="Overall Progress"
          value={`${progress.overall_percentage}%`}
          icon="📊"
          progress={progress.overall_percentage}
          color="amber"
        />
        <StatCard
          title="Time Invested"
          value={`${Math.floor(progress.total_time_spent_minutes / 60)}h ${progress.total_time_spent_minutes % 60}m`}
          icon="⏱️"
          subtitle="Keep up the momentum!"
          color="blue"
        />
        <StatCard
          title="Current Stage"
          value={`Stage ${progress.current_stage_id}`}
          icon="📖"
          subtitle="ROS 2 & Simulation"
          color="purple"
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Learning Path */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-foreground font-serif">Your Learning Path</h2>
            <Link
              href="/learn"
              className="text-sm text-primary hover:text-primary-600 font-medium flex items-center gap-1"
            >
              View All <span>→</span>
            </Link>
          </div>

          <div className="bg-card rounded-xl shadow-md border border-border overflow-hidden">
            {stages.map((stage, index) => (
              <div
                key={stage.stage}
                className={cn(
                  "flex items-center gap-4 p-4 transition-colors",
                  index !== stages.length - 1 && "border-b border-muted",
                  stage.status === 'in_progress' && "bg-book-highlight"
                )}
              >
                {/* Stage Number */}
                <div
                  className={cn(
                    "flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center text-xl shadow-sm",
                    stage.status === 'completed'
                      ? "bg-emerald-100 text-emerald-700 border-2 border-emerald-300"
                      : stage.status === 'in_progress'
                      ? "bg-amber-100 text-amber-700 border-2 border-amber-400"
                      : "bg-slate-100 text-slate-400 border-2 border-slate-200"
                  )}
                >
                  {stage.status === 'completed' ? '✓' : stage.icon}
                </div>

                {/* Content */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <h3 className={cn(
                      "font-semibold",
                      stage.status === 'locked' ? "text-slate-400" : "text-foreground"
                    )}>
                      Stage {stage.stage}: {stage.name}
                    </h3>
                    {stage.status === 'locked' && (
                      <span className="text-xs px-2 py-0.5 bg-slate-100 text-slate-500 rounded-full">
                        Locked
                      </span>
                    )}
                    {stage.status === 'in_progress' && (
                      <span className="text-xs px-2 py-0.5 bg-amber-100 text-amber-700 rounded-full font-medium">
                        In Progress
                      </span>
                    )}
                    {stage.status === 'completed' && (
                      <span className="text-xs px-2 py-0.5 bg-emerald-100 text-emerald-700 rounded-full font-medium">
                        Completed
                      </span>
                    )}
                  </div>

                  {/* Progress Bar */}
                  <div className="mt-2">
                    <div className="flex justify-between text-xs mb-1">
                      <span className="text-muted-foreground">Progress</span>
                      <span className={cn(
                        "font-medium",
                        stage.status === 'completed' ? "text-emerald-600" : "text-primary"
                      )}>
                        {stage.percent}%
                      </span>
                    </div>
                    <div className="h-2 bg-muted rounded-full overflow-hidden">
                      <div
                        className={cn(
                          "h-full rounded-full transition-all",
                          stage.status === 'completed'
                            ? "bg-emerald-500"
                            : stage.status === 'in_progress'
                            ? "bg-amber-500"
                            : "bg-slate-300"
                        )}
                        style={{ width: `${stage.percent}%` }}
                      />
                    </div>
                  </div>
                </div>

                {/* Action */}
                <div className="flex-shrink-0">
                  {stage.status !== 'locked' && (
                    <Link
                      href={`/learn/stage-${stage.stage}`}
                      className={cn(
                        "px-4 py-2 rounded-lg font-medium text-sm transition-colors",
                        stage.status === 'completed'
                          ? "bg-muted text-muted-foreground hover:bg-border"
                          : "bg-primary text-primary-foreground hover:bg-primary-600"
                      )}
                    >
                      {stage.status === 'completed' ? 'Review' : 'Continue'}
                    </Link>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions & Updates */}
        <div className="space-y-4">
          <h2 className="text-xl font-bold text-foreground font-serif">Quick Actions</h2>
          <div className="space-y-3">
            {quickActions.map((action) => (
              <Link
                key={action.href}
                href={action.href}
                className="flex items-start gap-3 p-4 bg-card rounded-xl shadow-sm border border-border hover:shadow-md hover:border-primary/20 transition-all group"
              >
                <div className={cn(
                  "flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center text-xl",
                  action.color === 'blue' && "bg-blue-50 text-blue-600",
                  action.color === 'purple' && "bg-purple-50 text-purple-600",
                  action.color === 'amber' && "bg-amber-50 text-amber-600",
                  action.color === 'green' && "bg-green-50 text-green-600",
                )}>
                  {action.icon}
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold text-foreground group-hover:text-primary transition-colors">
                    {action.title}
                  </h3>
                  <p className="text-sm text-muted-foreground m-0">{action.desc}</p>
                </div>
              </Link>
            ))}
          </div>

          {/* Recent Achievements */}
          <div className="mt-6">
            <h2 className="text-xl font-bold text-foreground font-serif mb-4">Recent Achievements</h2>
            <div className="bg-gradient-to-br from-amber-50 to-orange-50 rounded-xl p-4 border border-amber-200">
              <div className="flex items-center gap-3">
                <div className="text-3xl">🏆</div>
                <div>
                  <p className="font-semibold text-amber-800 m-0">First Steps</p>
                  <p className="text-sm text-amber-600 m-0">Completed Stage 1</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Quote Section */}
      <div className="bg-card rounded-xl p-6 shadow-md border border-border text-center">
        <blockquote className="text-lg text-foreground italic font-serif">
          &ldquo;The advance of technology is based on making it fit in so that you don&apos;t really even notice it, so it&apos;s part of everyday life.&rdquo;
        </blockquote>
        <cite className="text-sm text-muted-foreground mt-2 block not-italic">— Bill Gates</cite>
      </div>
    </div>
  );
}

// Stat Card Component
function StatCard({
  title,
  value,
  icon,
  subtitle,
  progress,
  color,
}: {
  title: string;
  value: string;
  icon: string;
  subtitle?: string;
  progress?: number;
  color: string;
}) {
  return (
    <div className="bg-card rounded-xl p-6 shadow-md border border-border hover:shadow-lg transition-shadow">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-muted-foreground text-sm font-medium">{title}</p>
          <p className="text-2xl font-bold text-foreground mt-1">{value}</p>
          {subtitle && <p className="text-xs text-secondary mt-1 m-0">{subtitle}</p>}
        </div>
        <div className={cn(
          "w-12 h-12 rounded-xl flex items-center justify-center text-2xl",
          color === 'amber' && "bg-amber-50 text-amber-600",
          color === 'blue' && "bg-blue-50 text-blue-600",
          color === 'purple' && "bg-purple-50 text-purple-600",
          color === 'green' && "bg-green-50 text-green-600",
        )}>
          {icon}
        </div>
      </div>
      {progress !== undefined && (
        <div className="mt-4">
          <div className="h-2 bg-muted rounded-full overflow-hidden">
            <div
              className={cn(
                "h-full rounded-full transition-all",
                color === 'amber' && "bg-amber-500",
                color === 'blue' && "bg-blue-500",
                color === 'purple' && "bg-purple-500",
                color === 'green' && "bg-green-500",
              )}
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      )}
    </div>
  );
}
