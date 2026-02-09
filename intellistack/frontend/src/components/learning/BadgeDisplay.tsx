/**
 * BadgeDisplay Component
 *
 * Displays earned badges with animations and details.
 */
import { useState } from 'react';
import { cn } from '@/lib/utils';

export interface Badge {
  id: string;
  name: string;
  description: string;
  icon?: string;
  earned_at?: string;
  stage_id?: string;
}

interface BadgeDisplayProps {
  badge: Badge;
  size?: 'sm' | 'md' | 'lg';
  showDetails?: boolean;
  isLocked?: boolean;
  className?: string;
}

export function BadgeDisplay({
  badge,
  size = 'md',
  showDetails = true,
  isLocked = false,
  className,
}: BadgeDisplayProps) {
  const [showTooltip, setShowTooltip] = useState(false);

  const sizeClasses = {
    sm: 'w-16 h-16',
    md: 'w-24 h-24',
    lg: 'w-32 h-32',
  };

  const iconSizeClasses = {
    sm: 'text-2xl',
    md: 'text-4xl',
    lg: 'text-5xl',
  };

  return (
    <div className={cn('relative inline-block', className)}>
      <div
        className="relative group cursor-pointer"
        onMouseEnter={() => setShowTooltip(true)}
        onMouseLeave={() => setShowTooltip(false)}
      >
        {/* Badge Circle */}
        <div
          className={cn(
            'rounded-full flex items-center justify-center transition-all duration-300',
            sizeClasses[size],
            isLocked
              ? 'bg-slate-700 border-2 border-slate-600 opacity-50'
              : 'bg-gradient-to-br from-yellow-400 to-yellow-600 border-4 border-yellow-300 shadow-lg group-hover:scale-110 group-hover:shadow-yellow-500/50'
          )}
        >
          {isLocked ? (
            <span className="text-3xl">🔒</span>
          ) : (
            <span className={cn(iconSizeClasses[size])}>{badge.icon || '🏆'}</span>
          )}
        </div>

        {/* Shine Effect */}
        {!isLocked && (
          <div className="absolute inset-0 rounded-full bg-gradient-to-tr from-white/0 via-white/40 to-white/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
        )}

        {/* Tooltip */}
        {showTooltip && showDetails && (
          <div className="absolute z-50 w-64 p-4 bg-slate-800 border border-slate-700 rounded-lg shadow-xl -top-2 left-full ml-4 transform">
            <div className="absolute w-3 h-3 bg-slate-800 border-l border-t border-slate-700 transform rotate-45 -left-1.5 top-6" />
            <h4 className="text-white font-bold mb-2">{badge.name}</h4>
            <p className="text-slate-300 text-sm mb-2">{badge.description}</p>
            {badge.earned_at && (
              <p className="text-slate-400 text-xs">
                Earned: {new Date(badge.earned_at).toLocaleDateString()}
              </p>
            )}
            {isLocked && (
              <p className="text-slate-400 text-xs italic">
                Complete the requirements to earn this badge
              </p>
            )}
          </div>
        )}
      </div>

      {/* Badge Name (below) */}
      {showDetails && (
        <div className="text-center mt-2">
          <p className={cn('font-medium', isLocked ? 'text-slate-500' : 'text-white')}>
            {badge.name}
          </p>
        </div>
      )}
    </div>
  );
}

/**
 * BadgeGrid Component
 *
 * Displays a grid of badges
 */
interface BadgeGridProps {
  badges: Badge[];
  lockedBadges?: Badge[];
  columns?: number;
  className?: string;
}

export function BadgeGrid({ badges, lockedBadges = [], columns = 4, className }: BadgeGridProps) {
  const allBadges = [...badges, ...lockedBadges];

  return (
    <div
      className={cn(
        'grid gap-6',
        columns === 3 && 'grid-cols-3',
        columns === 4 && 'grid-cols-2 md:grid-cols-4',
        columns === 5 && 'grid-cols-2 md:grid-cols-5',
        className
      )}
    >
      {allBadges.map((badge, index) => {
        const isLocked = index >= badges.length;
        return <BadgeDisplay key={badge.id} badge={badge} isLocked={isLocked} />;
      })}
    </div>
  );
}

/**
 * BadgeNotification Component
 *
 * Animated notification when a badge is earned
 */
interface BadgeNotificationProps {
  badge: Badge;
  onClose: () => void;
}

export function BadgeNotification({ badge, onClose }: BadgeNotificationProps) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm animate-in fade-in">
      <div className="bg-slate-800 border-2 border-yellow-500 rounded-xl p-8 max-w-md mx-4 shadow-2xl animate-in zoom-in duration-500">
        {/* Celebration Effect */}
        <div className="text-center mb-6">
          <div className="inline-block animate-bounce">
            <div className="w-32 h-32 rounded-full bg-gradient-to-br from-yellow-400 to-yellow-600 flex items-center justify-center text-6xl border-4 border-yellow-300 shadow-lg shadow-yellow-500/50">
              {badge.icon || '🏆'}
            </div>
          </div>
        </div>

        <div className="text-center">
          <h2 className="text-3xl font-bold text-white mb-2">Badge Earned! 🎉</h2>
          <h3 className="text-xl font-semibold text-yellow-400 mb-3">{badge.name}</h3>
          <p className="text-slate-300 mb-6">{badge.description}</p>

          <button
            onClick={onClose}
            className="w-full py-3 px-6 bg-yellow-600 hover:bg-yellow-700 text-white font-semibold rounded-lg transition-colors"
          >
            Continue Learning
          </button>
        </div>
      </div>
    </div>
  );
}
