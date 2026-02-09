/**
 * StageCard Component
 *
 * Displays a learning stage with status, progress, and lock state.
 */
import Link from 'next/link';
import { cn } from '@/lib/utils';
import { ProgressBar } from './ProgressBar';

export type StageStatus = 'locked' | 'available' | 'in_progress' | 'completed';

interface StageCardProps {
  stageNumber: number;
  title: string;
  description: string;
  status: StageStatus;
  progress: number;
  estimatedHours: number;
  contentCount: number;
  isAccessible: boolean;
  href?: string;
  prerequisite?: string;
  className?: string;
}

const statusConfig = {
  locked: {
    badge: 'Locked',
    badgeColor: 'bg-slate-700 text-slate-400',
    borderColor: 'border-slate-700',
    bgColor: 'bg-slate-800/50',
    icon: '🔒',
  },
  available: {
    badge: 'Available',
    badgeColor: 'bg-blue-600 text-white',
    borderColor: 'border-blue-600',
    bgColor: 'bg-slate-800',
    icon: '📚',
  },
  in_progress: {
    badge: 'In Progress',
    badgeColor: 'bg-yellow-600 text-white',
    borderColor: 'border-yellow-600',
    bgColor: 'bg-slate-800',
    icon: '⚡',
  },
  completed: {
    badge: 'Completed',
    badgeColor: 'bg-green-600 text-white',
    borderColor: 'border-green-600',
    bgColor: 'bg-slate-800',
    icon: '✅',
  },
};

export function StageCard({
  stageNumber,
  title,
  description,
  status,
  progress,
  estimatedHours,
  contentCount,
  isAccessible,
  href,
  prerequisite,
  className,
}: StageCardProps) {
  const config = statusConfig[status];
  const CardWrapper = isAccessible && href ? Link : 'div';

  return (
    <CardWrapper
      href={href || '#'}
      className={cn(
        'block rounded-lg border-2 p-6 transition-all duration-200',
        config.borderColor,
        config.bgColor,
        isAccessible && href
          ? 'hover:scale-[1.02] hover:shadow-xl cursor-pointer'
          : 'opacity-75 cursor-not-allowed',
        className
      )}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div
            className={cn(
              'w-12 h-12 rounded-full flex items-center justify-center text-xl font-bold',
              status === 'completed'
                ? 'bg-green-600 text-white'
                : status === 'in_progress'
                ? 'bg-yellow-600 text-white'
                : status === 'available'
                ? 'bg-blue-600 text-white'
                : 'bg-slate-700 text-slate-500'
            )}
          >
            {status === 'locked' ? config.icon : stageNumber}
          </div>
          <div>
            <h3 className="text-xl font-bold text-white">Stage {stageNumber}</h3>
            <p className="text-sm text-slate-400">{title}</p>
          </div>
        </div>
        <span className={cn('px-3 py-1 rounded-full text-xs font-semibold', config.badgeColor)}>
          {config.badge}
        </span>
      </div>

      {/* Description */}
      <p className="text-slate-300 text-sm mb-4 line-clamp-2">{description}</p>

      {/* Progress */}
      {status !== 'locked' && (
        <div className="mb-4">
          <ProgressBar
            percentage={progress}
            size="md"
            variant={
              status === 'completed'
                ? 'success'
                : status === 'in_progress'
                ? 'default'
                : 'default'
            }
          />
        </div>
      )}

      {/* Metadata */}
      <div className="flex items-center gap-4 text-sm text-slate-400">
        <div className="flex items-center gap-1">
          <span>📝</span>
          <span>{contentCount} lessons</span>
        </div>
        <div className="flex items-center gap-1">
          <span>⏱️</span>
          <span>{estimatedHours}h</span>
        </div>
        {status === 'completed' && (
          <div className="flex items-center gap-1 text-green-400">
            <span>🏆</span>
            <span>Badge Earned</span>
          </div>
        )}
      </div>

      {/* Lock Message */}
      {status === 'locked' && prerequisite && (
        <div className="mt-4 pt-4 border-t border-slate-700">
          <p className="text-xs text-slate-400 flex items-center gap-2">
            <span>🔒</span>
            <span>Complete {prerequisite} to unlock</span>
          </p>
        </div>
      )}

      {/* Call to Action */}
      {status === 'available' && (
        <div className="mt-4">
          <div className="text-sm text-blue-400 font-medium flex items-center gap-2">
            <span>Start Learning</span>
            <span>→</span>
          </div>
        </div>
      )}

      {status === 'in_progress' && (
        <div className="mt-4">
          <div className="text-sm text-yellow-400 font-medium flex items-center gap-2">
            <span>Continue Learning</span>
            <span>→</span>
          </div>
        </div>
      )}
    </CardWrapper>
  );
}

/**
 * StageCardSkeleton - Loading state
 */
export function StageCardSkeleton() {
  return (
    <div className="rounded-lg border-2 border-slate-700 bg-slate-800/50 p-6 animate-pulse">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-full bg-slate-700" />
          <div>
            <div className="h-6 w-24 bg-slate-700 rounded mb-2" />
            <div className="h-4 w-32 bg-slate-700 rounded" />
          </div>
        </div>
        <div className="h-6 w-20 bg-slate-700 rounded-full" />
      </div>
      <div className="h-10 bg-slate-700 rounded mb-4" />
      <div className="h-2 bg-slate-700 rounded mb-4" />
      <div className="flex gap-4">
        <div className="h-4 w-20 bg-slate-700 rounded" />
        <div className="h-4 w-16 bg-slate-700 rounded" />
      </div>
    </div>
  );
}
