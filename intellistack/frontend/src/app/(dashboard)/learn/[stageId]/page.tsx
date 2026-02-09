"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api, type ContentItem } from "@/lib/api";
import { useLearningStore } from "@/stores/learningStore";
import Link from "next/link";
import { cn, formatDuration } from "@/lib/utils";
import { useParams, useRouter } from "next/navigation";

export default function StagePage() {
  const params = useParams();
  const stageId = params.stageId as string;
  const router = useRouter();
  const queryClient = useQueryClient();

  const { data: stage, isLoading: stageLoading } = useQuery({
    queryKey: ["stage", stageId],
    queryFn: () => api.learning.getStage(stageId),
  });

  const { data: content, isLoading: contentLoading } = useQuery({
    queryKey: ["stageContent", stageId],
    queryFn: () => api.learning.getStageContent(stageId),
    enabled: !!stage?.is_accessible,
  });

  const markComplete = useMutation({
    mutationFn: (contentId: string) =>
      api.learning.completeContent(contentId, { time_spent_minutes: 15 }),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["stageContent", stageId] });
      queryClient.invalidateQueries({ queryKey: ["stage", stageId] });
      queryClient.invalidateQueries({ queryKey: ["learningPath"] });

      if (data.badge_earned) {
        alert(`🎉 Badge Earned: ${data.badge_earned}`);
      }
    },
  });

  if (stageLoading || contentLoading) {
    return <LoadingSkeleton />;
  }

  if (!stage) {
    return (
      <div className="text-center py-12">
        <p className="text-red-400">Stage not found</p>
        <Link href="/learn" className="mt-4 text-blue-400 hover:underline">
          Back to Learning Path
        </Link>
      </div>
    );
  }

  // Show lock screen if not accessible
  if (!stage.is_accessible) {
    return (
      <div className="max-w-lg mx-auto text-center py-12">
        <div className="text-6xl mb-4">🔒</div>
        <h1 className="text-2xl font-bold text-white mb-2">{stage.name}</h1>
        <p className="text-slate-400 mb-6">
          Complete the prerequisite stage to unlock this content.
        </p>
        <Link
          href="/learn"
          className="px-6 py-3 bg-blue-600 rounded-lg font-medium hover:bg-blue-700"
        >
          Back to Learning Path
        </Link>
      </div>
    );
  }

  const completedCount = content?.filter((c) => c.is_completed).length || 0;
  const totalCount = content?.length || 0;

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center gap-2 text-sm text-slate-400">
        <Link href="/learn" className="hover:text-white">
          Learning Path
        </Link>
        <span>/</span>
        <span className="text-white">Stage {stage.number}</span>
      </div>

      <div className="bg-slate-800 rounded-xl p-6">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white">{stage.name}</h1>
            <p className="text-slate-400 mt-2">{stage.description}</p>
          </div>
          <div
            className={cn(
              "px-3 py-1 rounded-full text-sm font-medium",
              stage.status === "completed"
                ? "bg-emerald-600/20 text-emerald-400"
                : stage.status === "in_progress"
                ? "bg-blue-600/20 text-blue-400"
                : "bg-slate-700 text-slate-400"
            )}
          >
            {stage.status === "completed"
              ? "Completed"
              : stage.status === "in_progress"
              ? "In Progress"
              : "Available"}
          </div>
        </div>

        {/* Progress */}
        <div className="mt-6">
          <div className="flex justify-between text-sm mb-2">
            <span className="text-slate-400">
              {completedCount} of {totalCount} lessons completed
            </span>
            <span className="text-blue-400">
              {Math.round(stage.percentage_complete)}%
            </span>
          </div>
          <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-blue-500 transition-all duration-300"
              style={{ width: `${stage.percentage_complete}%` }}
            />
          </div>
        </div>

        {/* Learning Objectives */}
        {stage.learning_objectives.length > 0 && (
          <div className="mt-6">
            <h3 className="text-sm font-medium text-slate-300 mb-2">
              Learning Objectives
            </h3>
            <ul className="space-y-1">
              {stage.learning_objectives.map((obj, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-slate-400">
                  <span className="text-blue-400">•</span>
                  {obj}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Content List */}
      <div className="space-y-3">
        <h2 className="text-lg font-semibold text-white">Course Content</h2>

        {content?.map((item, index) => (
          <ContentCard
            key={item.id}
            item={item}
            index={index}
            onComplete={() => markComplete.mutate(item.id)}
            isCompleting={markComplete.isPending}
          />
        ))}
      </div>
    </div>
  );
}

function ContentCard({
  item,
  index,
  onComplete,
  isCompleting,
}: {
  item: ContentItem;
  index: number;
  onComplete: () => void;
  isCompleting: boolean;
}) {
  return (
    <div
      className={cn(
        "flex items-center gap-4 p-4 rounded-lg border transition-all",
        item.is_completed
          ? "bg-emerald-950/20 border-emerald-600/30"
          : "bg-slate-800 border-slate-700 hover:border-slate-600"
      )}
    >
      {/* Completion indicator */}
      <div
        className={cn(
          "w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium flex-shrink-0",
          item.is_completed ? "bg-emerald-600" : "bg-slate-700"
        )}
      >
        {item.is_completed ? "✓" : index + 1}
      </div>

      {/* Content info */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2">
          <h3
            className={cn(
              "font-medium",
              item.is_completed ? "text-emerald-400" : "text-white"
            )}
          >
            {item.title}
          </h3>
          {item.is_required && (
            <span className="text-xs px-1.5 py-0.5 bg-slate-700 rounded text-slate-400">
              Required
            </span>
          )}
        </div>
        <div className="flex items-center gap-3 mt-1 text-xs text-slate-500">
          <span>
            {item.content_type === "lesson"
              ? "📖"
              : item.content_type === "exercise"
              ? "💻"
              : "📝"}{" "}
            {item.content_type}
          </span>
          <span>⏱️ {formatDuration(item.estimated_minutes)}</span>
        </div>
      </div>

      {/* Action */}
      {!item.is_completed && (
        <button
          onClick={onComplete}
          disabled={isCompleting}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 rounded-lg text-sm font-medium transition-colors"
        >
          {isCompleting ? "..." : "Mark Complete"}
        </button>
      )}
    </div>
  );
}

function LoadingSkeleton() {
  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-pulse">
      <div className="h-4 bg-slate-800 rounded w-32" />
      <div className="h-48 bg-slate-800 rounded-xl" />
      <div className="space-y-3">
        {[1, 2, 3, 4, 5].map((i) => (
          <div key={i} className="h-20 bg-slate-800 rounded-lg" />
        ))}
      </div>
    </div>
  );
}
