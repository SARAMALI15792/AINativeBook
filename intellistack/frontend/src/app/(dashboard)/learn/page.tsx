"use client";

import { useQuery } from "@tanstack/react-query";
import { api, type StageWithStatus } from "@lib/api";
import BookLayout from "@components/layout/BookLayout";
import Link from "next/link";
import { cn } from "@lib/utils";

export default function LearnPage() {
  const { data: learningPath, isLoading, error } = useQuery({
    queryKey: ["learningPath"],
    queryFn: () => api.learning.getLearningPath(),
  });

  // Transform stages to chapters format
  const chapters = learningPath?.stages.map((stage, index) => ({
    id: stage.id,
    title: stage.name,
    slug: stage.slug,
    order: index + 1,
    status: stage.status,
    percentage: stage.percentage_complete,
    subsections: [],
  })) || [];

  if (isLoading) {
    return (
      <BookLayout
        title="Learning Path"
        subtitle="Physical AI & Humanoid Robotics"
        chapters={[]}
        showProgress={false}
      >
        <LoadingState />
      </BookLayout>
    );
  }

  if (error) {
    return (
      <BookLayout
        title="Learning Path"
        subtitle="Physical AI & Humanoid Robotics"
        chapters={chapters}
        overallProgress={learningPath?.overall_percentage || 0}
      >
        <ErrorState />
      </BookLayout>
    );
  }

  return (
    <BookLayout
      title="Learning Path"
      subtitle="Physical AI & Humanoid Robotics"
      chapters={chapters}
      overallProgress={learningPath?.overall_percentage || 0}
    >
      {/* Right Side Content - Welcome to Learning */}
      <div className="space-y-8">
        {/* Header */}
        <div className="border-b-2 border-[#e8e0d5] pb-6">
          <p className="text-[#a67c52] text-sm font-medium mb-2">📚 Learning Path</p>
          <h1 className="text-3xl font-bold text-[#3d3229] font-serif">
            Master Physical AI & Humanoid Robotics
          </h1>
          <p className="text-[#6b5a4a] mt-3 leading-relaxed">
            Welcome to your comprehensive journey through the world of Physical AI. This learning path
            is structured like a book, with each stage representing a chapter in your education.
            Navigate through the chapters using the table of contents on the left.
          </p>
        </div>

        {/* Overall Progress */}
        {learningPath && (
          <div className="bg-gradient-to-r from-[#fefcf8] to-[#faf8f5] rounded-xl p-6 border border-[#e8e0d5]">
            <div className="flex items-center gap-6 flex-wrap">
              <div className="text-center">
                <div className="text-4xl font-bold text-[#8b6914]">
                  {Math.round(learningPath.overall_percentage)}%
                </div>
                <div className="text-xs text-[#8b7355] mt-1">Complete</div>
              </div>
              <div className="h-12 w-px bg-[#e8e0d5] hidden sm:block" />
              <div className="text-center">
                <div className="text-4xl font-bold text-[#a67c52]">
                  {learningPath.total_badges_earned}
                </div>
                <div className="text-xs text-[#8b7355] mt-1">Badges Earned</div>
              </div>
              <div className="h-12 w-px bg-[#e8e0d5] hidden sm:block" />
              <div className="text-center">
                <div className="text-4xl font-bold text-[#6b5a4a]">
                  {learningPath.estimated_hours_remaining}h
                </div>
                <div className="text-xs text-[#8b7355] mt-1">Remaining</div>
              </div>
              <div className="flex-1" />
              <Link
                href={learningPath.current_stage ? `/learn/${learningPath.current_stage.id}` : "/learn/stage-1"}
                className="px-6 py-3 bg-[#8b6914] hover:bg-[#6b5014] text-white rounded-lg font-medium transition-colors shadow-md"
              >
                {learningPath.current_stage ? "Continue Reading →" : "Start Learning →"}
              </Link>
            </div>

            {/* Overall Progress Bar */}
            <div className="mt-4">
              <div className="h-3 bg-[#e8e0d5] rounded-full overflow-hidden border border-[#d4c5b5]">
                <div
                  className="h-full bg-gradient-to-r from-[#8b6914] to-[#a67c52] transition-all duration-500"
                  style={{ width: `${learningPath.overall_percentage}%` }}
                />
              </div>
            </div>
          </div>
        )}

        {/* Stage Cards - Book Style */}
        <div className="space-y-4">
          <h2 className="text-xl font-bold text-[#3d3229] font-serif">Chapters Overview</h2>
          <div className="grid gap-4">
            {learningPath?.stages.map((stage, index) => (
              <StageCard key={stage.id} stage={stage} index={index} />
            ))}
          </div>
        </div>

        {/* Learning Tips */}
        <div className="bg-blue-50 rounded-xl p-6 border border-blue-100">
          <h3 className="font-bold text-blue-800 mb-3 flex items-center gap-2">
            <span>💡</span> Learning Tips
          </h3>
          <ul className="space-y-2 text-sm text-blue-700">
            <li className="flex items-start gap-2">
              <span className="text-blue-400">•</span>
              <span>Complete each chapter sequentially to build a strong foundation</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-400">•</span>
              <span>Take notes as you read - this helps with retention</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-400">•</span>
              <span>Practice the exercises at the end of each chapter</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-400">•</span>
              <span>Use the AI Tutor if you get stuck or need clarification</span>
            </li>
          </ul>
        </div>

        {/* Quote */}
        <blockquote className="border-l-4 border-[#a67c52] pl-6 py-2 italic text-[#5c4a3d] text-lg">
          "The best way to predict the future is to invent it."
          <cite className="block text-sm text-[#8b7355] mt-2 not-italic">— Alan Kay</cite>
        </blockquote>
      </div>
    </BookLayout>
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
        "relative rounded-xl border p-5 transition-all",
        isLocked
          ? "border-[#e8e0d5] bg-[#faf8f5] opacity-60"
          : isCompleted
          ? "border-emerald-200 bg-emerald-50/30"
          : isInProgress
          ? "border-amber-200 bg-amber-50/30 shadow-md"
          : "border-[#e8e0d5] bg-white hover:shadow-md"
      )}
    >
      <div className="flex items-start gap-4">
        {/* Chapter Number */}
        <div
          className={cn(
            "flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center text-lg font-bold border-2",
            isCompleted
              ? "bg-emerald-600 border-emerald-600 text-white"
              : isInProgress
              ? "bg-amber-500 border-amber-500 text-white"
              : isLocked
              ? "bg-[#e8e0d5] border-[#d4c5b5] text-[#a09080]"
              : "bg-white border-[#c4b5a5] text-[#6b5a4a]"
          )}
        >
          {isCompleted ? "✓" : index + 1}
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <h3 className="text-lg font-semibold text-[#3d3229]">{stage.name}</h3>
            {isLocked && (
              <span className="text-xs px-2 py-0.5 bg-[#e8e0d5] rounded-full text-[#8b7355]">
                🔒 Locked
              </span>
            )}
            {isInProgress && (
              <span className="text-xs px-2 py-0.5 bg-amber-100 text-amber-700 rounded-full font-medium">
                Reading Now
              </span>
            )}
            {isCompleted && (
              <span className="text-xs px-2 py-0.5 bg-emerald-100 text-emerald-700 rounded-full font-medium">
                Completed
              </span>
            )}
          </div>

          <p className="text-[#6b5a4a] text-sm mt-2 line-clamp-2">{stage.description}</p>

          {/* Progress for in-progress chapters */}
          {isInProgress && (
            <div className="mt-3">
              <div className="flex justify-between text-xs mb-1">
                <span className="text-[#8b7355]">Progress</span>
                <span className="text-amber-600 font-medium">
                  {Math.round(stage.percentage_complete)}%
                </span>
              </div>
              <div className="h-2 bg-[#e8e0d5] rounded-full overflow-hidden border border-[#d4c5b5]">
                <div
                  className="h-full bg-amber-500 transition-all"
                  style={{ width: `${stage.percentage_complete}%` }}
                />
              </div>
            </div>
          )}

          {/* Meta info */}
          <div className="flex items-center gap-4 mt-3 text-xs text-[#8b7355]">
            <span>⏱️ {stage.estimated_hours} hours to read</span>
            <span>📄 {stage.content_count} sections</span>
          </div>
        </div>

        {/* Action */}
        <div className="flex-shrink-0">
          {!isLocked && (
            <Link
              href={`/learn/${stage.id}`}
              className={cn(
                "px-4 py-2 rounded-lg font-medium text-sm transition-colors",
                isCompleted
                  ? "bg-[#e8e0d5] text-[#5c4a3d] hover:bg-[#ded5c8]"
                  : "bg-[#8b6914] text-white hover:bg-[#6b5014]"
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

function LoadingState() {
  return (
    <div className="space-y-6 animate-pulse">
      <div className="h-8 bg-[#e8e0d5] rounded w-2/3" />
      <div className="h-4 bg-[#e8e0d5] rounded w-full" />
      <div className="h-4 bg-[#e8e0d5] rounded w-4/5" />
      <div className="h-24 bg-[#e8e0d5] rounded-xl" />
      <div className="space-y-3">
        {[1, 2, 3].map((i) => (
          <div key={i} className="h-24 bg-[#e8e0d5] rounded-xl" />
        ))}
      </div>
    </div>
  );
}

function ErrorState() {
  return (
    <div className="text-center py-12">
      <div className="text-6xl mb-4">📚</div>
      <h2 className="text-xl font-bold text-[#3d3229] mb-2">Failed to Load Learning Path</h2>
      <p className="text-[#6b5a4a] mb-4">We couldn't fetch your learning progress. Please try again.</p>
      <button
        onClick={() => window.location.reload()}
        className="px-4 py-2 bg-[#8b6914] text-white rounded-lg hover:bg-[#6b5014] transition-colors"
      >
        Retry
      </button>
    </div>
  );
}
