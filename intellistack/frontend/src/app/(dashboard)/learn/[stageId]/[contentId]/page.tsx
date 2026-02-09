'use client';

import { useEffect, useRef, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { useLearningStore } from '@/stores/learningStore';
import { ProgressBar } from '@/components/learning/ProgressBar';
import { BadgeNotification } from '@/components/learning/BadgeDisplay';

export default function ContentViewerPage() {
  const params = useParams();
  const router = useRouter();
  const { completeContent } = useLearningStore();

  const contentRef = useRef<HTMLDivElement>(null);
  const [scrollPercentage, setScrollPercentage] = useState(0);
  const [isCompleted, setIsCompleted] = useState(false);
  const [showBadgeNotification, setShowBadgeNotification] = useState(false);
  const [earnedBadge, setEarnedBadge] = useState<any>(null);
  const [startTime] = useState(Date.now());

  const stageId = params.stageId as string;
  const contentId = params.contentId as string;

  // Track scroll position
  useEffect(() => {
    const handleScroll = () => {
      if (!contentRef.current) return;

      const element = contentRef.current;
      const scrollTop = window.scrollY;
      const scrollHeight = element.scrollHeight - window.innerHeight;
      const percentage = (scrollTop / scrollHeight) * 100;

      setScrollPercentage(Math.min(percentage, 100));

      // Mark complete when scrolled to 90% or bottom
      if (percentage >= 90 && !isCompleted) {
        handleContentComplete();
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [isCompleted]);

  const handleContentComplete = async () => {
    if (isCompleted) return;

    const timeSpentMinutes = Math.floor((Date.now() - startTime) / 60000);

    try {
      const result = await completeContent(contentId, {
        time_spent_minutes: timeSpentMinutes,
      });

      setIsCompleted(true);

      // Show badge notification if earned
      if (result?.badge_earned) {
        setEarnedBadge(result.badge_earned);
        setShowBadgeNotification(true);
      }
    } catch (error) {
      console.error('Failed to mark content complete:', error);
    }
  };

  const handleManualComplete = () => {
    handleContentComplete();
  };

  // Mock content data (replace with API call)
  const content = {
    title: 'Python Programming Basics',
    stage: 'Stage 1: Foundations',
    estimatedMinutes: 45,
    nextContentId: 'linux-fundamentals',
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Progress Indicator (Sticky) */}
      <div className="sticky top-0 z-40 bg-slate-900 border-b border-slate-800 py-3 -mx-4 px-4">
        <div className="flex items-center justify-between mb-2">
          <Link
            href={`/learn/${stageId}`}
            className="text-sm text-slate-400 hover:text-white flex items-center gap-2"
          >
            <span>←</span>
            <span>Back to {content.stage}</span>
          </Link>
          <span className="text-sm text-slate-400">
            {content.estimatedMinutes} min read
          </span>
        </div>
        <ProgressBar
          percentage={scrollPercentage}
          label="Reading Progress"
          size="sm"
          variant={isCompleted ? 'success' : 'default'}
        />
      </div>

      {/* Content */}
      <div ref={contentRef} className="py-8 prose prose-invert max-w-none">
        <h1 className="text-4xl font-bold text-white mb-6">{content.title}</h1>

        {/* Placeholder: Actual content would be loaded from API or MDX */}
        <div className="space-y-6 text-slate-300">
          <p>
            This is a placeholder for the actual lesson content. In production, this would be
            fetched from the Docusaurus content API or rendered from MDX.
          </p>

          <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
            <h2 className="text-2xl font-bold text-white mb-4">Learning Objectives</h2>
            <ul className="space-y-2">
              <li>✅ Understand Python syntax and data types</li>
              <li>✅ Write functions and classes</li>
              <li>✅ Use NumPy for numerical computing</li>
              <li>✅ Apply Python to robotics problems</li>
            </ul>
          </div>

          {/* Simulated long content */}
          {Array.from({ length: 10 }).map((_, i) => (
            <div key={i}>
              <h3 className="text-xl font-bold text-white mb-3">Section {i + 1}</h3>
              <p className="mb-4">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor
                incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud
                exercitation ullamco laboris.
              </p>
              <pre className="bg-slate-900 border border-slate-700 rounded-lg p-4 overflow-x-auto">
                <code className="text-sm text-green-400">
                  {`# Example code for section ${i + 1}\ndef example_function():\n    return "Hello, Robot!"`}
                </code>
              </pre>
            </div>
          ))}
        </div>
      </div>

      {/* Bottom Actions */}
      <div className="border-t border-slate-800 pt-6 pb-12 space-y-4">
        {/* Manual Complete Button */}
        {!isCompleted && (
          <button
            onClick={handleManualComplete}
            className="w-full py-3 px-6 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition-colors flex items-center justify-center gap-2"
          >
            <span>✓</span>
            <span>Mark as Complete</span>
          </button>
        )}

        {isCompleted && (
          <div className="bg-green-600/20 border border-green-600 rounded-lg p-4 text-center">
            <p className="text-green-400 font-semibold mb-2">✅ Content Completed!</p>
            <p className="text-sm text-slate-300">Great job! Continue to the next lesson.</p>
          </div>
        )}

        {/* Navigation */}
        <div className="flex gap-4">
          <Link
            href={`/learn/${stageId}`}
            className="flex-1 py-3 px-6 bg-slate-800 hover:bg-slate-700 text-white font-medium rounded-lg transition-colors text-center"
          >
            ← Back to Stage
          </Link>
          {content.nextContentId && (
            <Link
              href={`/learn/${stageId}/${content.nextContentId}`}
              className="flex-1 py-3 px-6 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors text-center"
            >
              Next Lesson →
            </Link>
          )}
        </div>
      </div>

      {/* Badge Earned Notification */}
      {showBadgeNotification && earnedBadge && (
        <BadgeNotification
          badge={earnedBadge}
          onClose={() => {
            setShowBadgeNotification(false);
            router.push(`/learn/${stageId}`);
          }}
        />
      )}
    </div>
  );
}
