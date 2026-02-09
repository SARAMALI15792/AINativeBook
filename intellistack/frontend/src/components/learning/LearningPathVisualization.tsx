/**
 * LearningPathVisualization Component
 *
 * Visual representation of the learning journey with all stages.
 */
import { cn } from '@/lib/utils';
import { StageStatus } from './StageCard';

export interface PathStage {
  id: string;
  number: number;
  name: string;
  status: StageStatus;
  progress: number;
}

interface LearningPathVisualizationProps {
  stages: PathStage[];
  currentStageId?: string;
  orientation?: 'horizontal' | 'vertical';
  className?: string;
  onStageClick?: (stageId: string) => void;
}

export function LearningPathVisualization({
  stages,
  currentStageId,
  orientation = 'vertical',
  className,
  onStageClick,
}: LearningPathVisualizationProps) {
  return (
    <div className={cn('relative', className)}>
      {orientation === 'vertical' ? (
        <VerticalPath
          stages={stages}
          currentStageId={currentStageId}
          onStageClick={onStageClick}
        />
      ) : (
        <HorizontalPath
          stages={stages}
          currentStageId={currentStageId}
          onStageClick={onStageClick}
        />
      )}
    </div>
  );
}

function VerticalPath({
  stages,
  currentStageId,
  onStageClick,
}: {
  stages: PathStage[];
  currentStageId?: string;
  onStageClick?: (stageId: string) => void;
}) {
  return (
    <div className="space-y-4">
      {stages.map((stage, index) => {
        const isLast = index === stages.length - 1;
        const isCurrent = stage.id === currentStageId;

        return (
          <div key={stage.id} className="relative">
            {/* Connection Line */}
            {!isLast && (
              <div className="absolute left-6 top-14 w-0.5 h-10 bg-slate-700">
                {stage.status === 'completed' && (
                  <div className="w-full bg-green-500 h-full" />
                )}
              </div>
            )}

            {/* Stage Node */}
            <button
              onClick={() => onStageClick?.(stage.id)}
              disabled={stage.status === 'locked'}
              className={cn(
                'w-full flex items-start gap-4 p-4 rounded-lg transition-all',
                stage.status !== 'locked' && 'hover:bg-slate-800 cursor-pointer',
                isCurrent && 'bg-slate-800 ring-2 ring-blue-500'
              )}
            >
              {/* Stage Circle */}
              <div
                className={cn(
                  'flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center font-bold text-lg transition-all',
                  stage.status === 'completed' && 'bg-green-600 text-white',
                  stage.status === 'in_progress' && 'bg-yellow-600 text-white animate-pulse',
                  stage.status === 'available' && 'bg-blue-600 text-white',
                  stage.status === 'locked' && 'bg-slate-700 text-slate-500'
                )}
              >
                {stage.status === 'completed' ? '✓' : stage.number}
              </div>

              {/* Stage Info */}
              <div className="flex-1 text-left">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-semibold text-white">Stage {stage.number}</span>
                  {stage.status === 'locked' && <span className="text-slate-500 text-sm">🔒</span>}
                </div>
                <p className="text-sm text-slate-300 mb-2">{stage.name}</p>

                {/* Progress Bar */}
                {stage.status !== 'locked' && (
                  <div className="w-full bg-slate-700 rounded-full h-1.5">
                    <div
                      className={cn(
                        'h-full rounded-full transition-all duration-500',
                        stage.status === 'completed' && 'bg-green-500',
                        stage.status === 'in_progress' && 'bg-yellow-500',
                        stage.status === 'available' && 'bg-blue-500'
                      )}
                      style={{ width: `${stage.progress}%` }}
                    />
                  </div>
                )}

                {/* Status Badge */}
                <div className="mt-2">
                  <span
                    className={cn(
                      'text-xs px-2 py-0.5 rounded-full',
                      stage.status === 'completed' && 'bg-green-600/20 text-green-400',
                      stage.status === 'in_progress' && 'bg-yellow-600/20 text-yellow-400',
                      stage.status === 'available' && 'bg-blue-600/20 text-blue-400',
                      stage.status === 'locked' && 'bg-slate-700/50 text-slate-500'
                    )}
                  >
                    {stage.status === 'completed' && 'Completed'}
                    {stage.status === 'in_progress' && 'In Progress'}
                    {stage.status === 'available' && 'Available'}
                    {stage.status === 'locked' && 'Locked'}
                  </span>
                </div>
              </div>

              {/* Arrow */}
              {stage.status !== 'locked' && (
                <div className="text-slate-400">
                  <svg
                    className="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 5l7 7-7 7"
                    />
                  </svg>
                </div>
              )}
            </button>
          </div>
        );
      })}
    </div>
  );
}

function HorizontalPath({
  stages,
  currentStageId,
  onStageClick,
}: {
  stages: PathStage[];
  currentStageId?: string;
  onStageClick?: (stageId: string) => void;
}) {
  return (
    <div className="relative">
      {/* Connection Line */}
      <div className="absolute top-6 left-0 right-0 h-0.5 bg-slate-700" />

      {/* Stages */}
      <div className="relative flex justify-between items-start">
        {stages.map((stage) => {
          const isCurrent = stage.id === currentStageId;

          return (
            <button
              key={stage.id}
              onClick={() => onStageClick?.(stage.id)}
              disabled={stage.status === 'locked'}
              className={cn(
                'flex flex-col items-center gap-2 transition-all',
                stage.status !== 'locked' && 'hover:scale-110 cursor-pointer',
                stage.status === 'locked' && 'opacity-50'
              )}
            >
              {/* Stage Circle */}
              <div
                className={cn(
                  'w-12 h-12 rounded-full flex items-center justify-center font-bold text-lg border-4 border-slate-900 transition-all z-10',
                  stage.status === 'completed' && 'bg-green-600 text-white',
                  stage.status === 'in_progress' && 'bg-yellow-600 text-white animate-pulse',
                  stage.status === 'available' && 'bg-blue-600 text-white',
                  stage.status === 'locked' && 'bg-slate-700 text-slate-500',
                  isCurrent && 'ring-4 ring-blue-500'
                )}
              >
                {stage.status === 'completed' ? '✓' : stage.number}
              </div>

              {/* Stage Name */}
              <div className="text-center max-w-[100px]">
                <p className="text-xs font-medium text-white truncate">{stage.name}</p>
                <p className="text-xs text-slate-400">{stage.progress}%</p>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}

/**
 * CompactPathProgress Component
 *
 * Compact version showing just the progress dots
 */
interface CompactPathProgressProps {
  totalStages: number;
  completedStages: number;
  currentStage: number;
  className?: string;
}

export function CompactPathProgress({
  totalStages,
  completedStages,
  currentStage,
  className,
}: CompactPathProgressProps) {
  return (
    <div className={cn('flex items-center gap-2', className)}>
      {Array.from({ length: totalStages }, (_, i) => i + 1).map((stage) => (
        <div
          key={stage}
          className={cn(
            'w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition-all',
            stage <= completedStages && 'bg-green-600 text-white',
            stage === currentStage && stage > completedStages && 'bg-yellow-600 text-white',
            stage > currentStage && 'bg-slate-700 text-slate-500'
          )}
        >
          {stage <= completedStages ? '✓' : stage}
        </div>
      ))}
    </div>
  );
}
