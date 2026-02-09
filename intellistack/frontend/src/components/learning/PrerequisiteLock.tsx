/**
 * PrerequisiteLock Component
 *
 * Displays information about locked content with clear unlock requirements.
 */
import Link from 'next/link';
import { cn } from '@/lib/utils';

interface PrerequisiteLockProps {
  title: string;
  prerequisiteName: string;
  prerequisiteHref?: string;
  currentProgress?: number;
  requiredProgress?: number;
  message?: string;
  variant?: 'inline' | 'overlay' | 'banner';
  className?: string;
}

export function PrerequisiteLock({
  title,
  prerequisiteName,
  prerequisiteHref,
  currentProgress = 0,
  requiredProgress = 100,
  message,
  variant = 'inline',
  className,
}: PrerequisiteLockProps) {
  const progressGap = requiredProgress - currentProgress;

  if (variant === 'overlay') {
    return (
      <div
        className={cn(
          'absolute inset-0 bg-slate-900/90 backdrop-blur-sm z-10 flex items-center justify-center rounded-lg',
          className
        )}
      >
        <div className="text-center p-8 max-w-md">
          <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-slate-800 flex items-center justify-center text-4xl">
            🔒
          </div>
          <h3 className="text-2xl font-bold text-white mb-2">{title} is Locked</h3>
          <p className="text-slate-300 mb-6">
            {message || `Complete ${prerequisiteName} to unlock this content.`}
          </p>

          {/* Progress Indicator */}
          {currentProgress > 0 && (
            <div className="mb-6">
              <div className="flex justify-between text-sm text-slate-400 mb-2">
                <span>{prerequisiteName}</span>
                <span>{currentProgress}%</span>
              </div>
              <div className="w-full bg-slate-700 rounded-full h-2">
                <div
                  className="bg-blue-500 h-2 rounded-full transition-all"
                  style={{ width: `${currentProgress}%` }}
                />
              </div>
              <p className="text-xs text-slate-400 mt-2">
                {progressGap}% remaining to unlock
              </p>
            </div>
          )}

          {prerequisiteHref && (
            <Link
              href={prerequisiteHref}
              className="inline-block px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-colors"
            >
              Go to {prerequisiteName} →
            </Link>
          )}
        </div>
      </div>
    );
  }

  if (variant === 'banner') {
    return (
      <div
        className={cn(
          'border-l-4 border-yellow-500 bg-slate-800 p-4 rounded-r-lg',
          className
        )}
      >
        <div className="flex items-start gap-3">
          <div className="flex-shrink-0 w-10 h-10 rounded-full bg-yellow-500/20 flex items-center justify-center text-xl">
            🔒
          </div>
          <div className="flex-1">
            <h4 className="text-white font-semibold mb-1">{title} Requires Prerequisites</h4>
            <p className="text-slate-300 text-sm mb-3">
              {message || `You need to complete ${prerequisiteName} before accessing this content.`}
            </p>

            {currentProgress > 0 && (
              <div className="mb-3">
                <div className="flex justify-between text-xs text-slate-400 mb-1">
                  <span>{prerequisiteName} Progress</span>
                  <span>{currentProgress}% / {requiredProgress}%</span>
                </div>
                <div className="w-full bg-slate-700 rounded-full h-1.5">
                  <div
                    className="bg-yellow-500 h-1.5 rounded-full transition-all"
                    style={{ width: `${(currentProgress / requiredProgress) * 100}%` }}
                  />
                </div>
              </div>
            )}

            {prerequisiteHref && (
              <Link
                href={prerequisiteHref}
                className="text-sm text-yellow-400 hover:text-yellow-300 font-medium inline-flex items-center gap-1"
              >
                <span>Continue {prerequisiteName}</span>
                <span>→</span>
              </Link>
            )}
          </div>
        </div>
      </div>
    );
  }

  // Inline variant (default)
  return (
    <div
      className={cn(
        'flex items-center gap-3 p-4 bg-slate-800 border border-slate-700 rounded-lg',
        className
      )}
    >
      <div className="flex-shrink-0 w-12 h-12 rounded-full bg-slate-700 flex items-center justify-center text-2xl">
        🔒
      </div>
      <div className="flex-1">
        <p className="text-white font-medium mb-1">{title}</p>
        <p className="text-sm text-slate-400">
          {message || `Complete ${prerequisiteName} (${currentProgress}%) to unlock`}
        </p>
      </div>
      {prerequisiteHref && (
        <Link
          href={prerequisiteHref}
          className="flex-shrink-0 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition-colors"
        >
          Go →
        </Link>
      )}
    </div>
  );
}

/**
 * UnlockChecklist Component
 *
 * Shows a checklist of requirements to unlock content
 */
interface UnlockRequirement {
  id: string;
  label: string;
  completed: boolean;
  href?: string;
}

interface UnlockChecklistProps {
  title: string;
  requirements: UnlockRequirement[];
  className?: string;
}

export function UnlockChecklist({ title, requirements, className }: UnlockChecklistProps) {
  const completedCount = requirements.filter((r) => r.completed).length;
  const totalCount = requirements.length;
  const allCompleted = completedCount === totalCount;

  return (
    <div className={cn('bg-slate-800 border border-slate-700 rounded-lg p-6', className)}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-white">{title}</h3>
        <span className="text-sm text-slate-400">
          {completedCount} / {totalCount} completed
        </span>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-slate-700 rounded-full h-2 mb-6">
        <div
          className="bg-green-500 h-2 rounded-full transition-all duration-500"
          style={{ width: `${(completedCount / totalCount) * 100}%` }}
        />
      </div>

      {/* Requirements List */}
      <div className="space-y-3">
        {requirements.map((requirement) => (
          <div
            key={requirement.id}
            className="flex items-center gap-3 p-3 bg-slate-900 rounded-lg"
          >
            <div
              className={cn(
                'flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-sm transition-all',
                requirement.completed
                  ? 'bg-green-600 text-white'
                  : 'bg-slate-700 text-slate-500'
              )}
            >
              {requirement.completed ? '✓' : '○'}
            </div>
            <span
              className={cn(
                'flex-1 text-sm',
                requirement.completed ? 'text-slate-400 line-through' : 'text-white'
              )}
            >
              {requirement.label}
            </span>
            {!requirement.completed && requirement.href && (
              <Link
                href={requirement.href}
                className="text-xs text-blue-400 hover:text-blue-300 font-medium"
              >
                Start →
              </Link>
            )}
          </div>
        ))}
      </div>

      {allCompleted && (
        <div className="mt-6 p-4 bg-green-600/20 border border-green-600 rounded-lg">
          <p className="text-green-400 text-sm font-medium text-center">
            🎉 All requirements completed! This content is now unlocked.
          </p>
        </div>
      )}
    </div>
  );
}
