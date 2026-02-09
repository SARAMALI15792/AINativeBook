"use client";

import { useQuery } from "@tanstack/react-query";
import { api, type StageWithStatus } from "@/lib/api";
import { useLearningStore } from "@/stores/learningStore";
import { useEffect } from "react";
import Link from "next/link";
import { cn, formatPercentage } from "@/lib/utils";

export default function LearnPage() {
  const { data: learningPath, isLoading, error } = useQuery({
    queryKey: ["learningPath"],
    queryFn: () => api.learning.getLearningPath(),
  });

  const setLearningPath = useLearningStore((s) => s.setLearningPath);

  useEffect(() => {
    if (learningPath) {
      setLearningPath(learningPath);
    }
  }, [learningPath, setLearningPath]);

  if (isLoading) {
    return <LoadingSkeleton />;
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-400">Failed to load learning path</p>
        <button
          onClick={() => window.location.reload()}
          className="mt-4 px-4 py-2 bg-blue-600 rounded-lg"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">Your Learning Path</h1>
          <p className="text-slate-400 mt-1">
            Master Physical AI & Humanoid Robotics
          </p>
        </div>

        {learningPath && (
          <div className="flex items-center gap-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-400">
                {formatPercentage(learningPath.overall_percentage)}
              </div>
              <div className="text-xs text-slate-400">Complete</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-cyan-400">
                {learningPath.total_badges_earned}
              </div>
              <div className="text-xs text-slate-400">Badges</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-emerald-400">
                {learningPath.estimated_hours_remaining}h
              </div>
              <div className="text-xs text-slate-400">Remaining</div>
            </div>
          </div>
        )}
      </div>

      {/* Overall Progress Bar */}
      {learningPath && (
        <div className="bg-slate-800 rounded-lg p-4">
          <div className="flex justify-between text-sm mb-2">
            <span className="text-slate-400">Overall Progress</span>
            <span className="text-white">
              {formatPercentage(learningPath.overall_percentage)}
            </span>
          </div>
          <div className="h-3 bg-slate-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-blue-500 to-cyan-500 transition-all duration-500"
              style={{ width: `${learningPath.overall_percentage}%` }}
            />
          </div>
        </div>
      )}

      {/* Stage Cards */}
      <div className="grid gap-4">
        {learningPath?.stages.map((stage, index) => (
          <StageCard key={stage.id} stage={stage} index={index} />
        ))}
      </div>
    </div>
  );
}

function StageCard({
  stage,
  index,
}: {
  stage: StageWithStatus;
  index: number;
}) {
  const isLocked = stage.status === "locked";
  const isCompleted = stage.status === "completed";
  const isInProgress = stage.status === "in_progress";

  return (
    <div
      className={cn(
        "relative rounded-xl border p-6 transition-all",
        isLocked
          ? "border-slate-700 bg-slate-800/50 opacity-60"
          : isCompleted
          ? "border-emerald-600/50 bg-emerald-950/20"
          : isInProgress
          ? "border-blue-600/50 bg-blue-950/20"
          : "border-slate-700 bg-slate-800 hover:border-slate-600"
      )}
    >
      <div className="flex items-start gap-4">
        {/* Stage Number */}
        <div
          className={cn(
            "flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center text-lg font-bold",
            isCompleted
              ? "bg-emerald-600"
              : isInProgress
              ? "bg-blue-600"
              : isLocked
              ? "bg-slate-700"
              : "bg-slate-600"
          )}
        >
          {isCompleted ? "✓" : index + 1}
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <h3 className="text-lg font-semibold text-white">{stage.name}</h3>
            {isLocked && (
              <span className="text-xs px-2 py-0.5 bg-slate-700 rounded-full text-slate-400">
                🔒 Locked
              </span>
            )}
            {isInProgress && (
              <span className="text-xs px-2 py-0.5 bg-blue-600/20 text-blue-400 rounded-full">
                In Progress
              </span>
            )}
            {isCompleted && (
              <span className="text-xs px-2 py-0.5 bg-emerald-600/20 text-emerald-400 rounded-full">
                Completed
              </span>
            )}
          </div>

          <p className="text-slate-400 text-sm mt-1 line-clamp-2">
            {stage.description}
          </p>

          {/* Progress for in-progress stages */}
          {isInProgress && (
            <div className="mt-3">
              <div className="flex justify-between text-xs mb-1">
                <span className="text-slate-400">Progress</span>
                <span className="text-blue-400">
                  {formatPercentage(stage.percentage_complete)}
                </span>
              </div>
              <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
                <div
                  className="h-full bg-blue-500 transition-all"
                  style={{ width: `${stage.percentage_complete}%` }}
                />
              </div>
            </div>
          )}

          {/* Meta info */}
          <div className="flex items-center gap-4 mt-3 text-xs text-slate-500">
            <span>⏱️ {stage.estimated_hours} hours</span>
            <span>📄 {stage.content_count} lessons</span>
          </div>
        </div>

        {/* Action */}
        <div className="flex-shrink-0">
          {!isLocked && (
            <Link
              href={`/learn/${stage.id}`}
              className={cn(
                "px-4 py-2 rounded-lg font-medium transition-colors",
                isCompleted
                  ? "bg-slate-700 text-slate-300 hover:bg-slate-600"
                  : "bg-blue-600 text-white hover:bg-blue-700"
              )}
            >
              {isCompleted ? "Review" : isInProgress ? "Continue" : "Start"}
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}

function LoadingSkeleton() {
  return (
    <div className="space-y-8 animate-pulse">
      <div className="h-8 bg-slate-800 rounded w-64" />
      <div className="h-16 bg-slate-800 rounded-lg" />
      {[1, 2, 3, 4, 5].map((i) => (
        <div key={i} className="h-32 bg-slate-800 rounded-xl" />
      ))}
    </div>
  );
}
