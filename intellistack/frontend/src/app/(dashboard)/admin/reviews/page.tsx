'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import {
  ReviewPanel,
  ReviewQueueItem,
  ReviewStats,
  ContentReviewData,
} from '@/components/admin/ReviewPanel';

export default function ReviewsPage() {
  const router = useRouter();
  const [selectedContent, setSelectedContent] = useState<ContentReviewData | null>(null);
  const [reviewQueue, setReviewQueue] = useState<ContentReviewData[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchReviewQueue();
  }, []);

  const fetchReviewQueue = async () => {
    setIsLoading(true);
    try {
      // TODO: Replace with actual API call
      // const response = await api.fetch('/api/v1/content?status=in_review');

      // Mock data
      setReviewQueue([
        {
          contentId: '1',
          title: 'Advanced ROS 2 Navigation',
          author: 'jane.doe@example.com',
          submittedAt: '2026-02-08T09:00:00Z',
          status: 'pending',
          currentVersion: '1.0.0',
        },
        {
          contentId: '2',
          title: 'Computer Vision with OpenCV',
          author: 'john.smith@example.com',
          submittedAt: '2026-02-07T15:30:00Z',
          status: 'pending',
          currentVersion: '1.0.1',
        },
        {
          contentId: '3',
          title: 'Machine Learning Basics',
          author: 'alice@example.com',
          submittedAt: '2026-02-06T11:00:00Z',
          status: 'pending',
          currentVersion: '2.0.0',
        },
      ]);
    } catch (error) {
      console.error('Failed to fetch review queue:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReview = async (decision: any) => {
    if (!selectedContent) return;

    try {
      // TODO: Replace with actual API call
      // await api.fetch(`/api/v1/content/${selectedContent.contentId}/review`, {
      //   method: 'POST',
      //   body: JSON.stringify(decision)
      // });

      console.log('Review submitted:', decision);
      alert(`Content ${decision.status}!`);

      // Remove from queue and close panel
      setReviewQueue(reviewQueue.filter((item) => item.contentId !== selectedContent.contentId));
      setSelectedContent(null);
    } catch (error) {
      console.error('Review submission failed:', error);
      alert('Failed to submit review');
    }
  };

  const stats = {
    pending: reviewQueue.filter((item) => item.status === 'pending').length,
    approved: 0,
    rejected: 0,
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Content Reviews</h1>
        <p className="text-slate-400">Review submitted content before publication</p>
      </div>

      {/* Stats */}
      <ReviewStats
        pending={stats.pending}
        approved={stats.approved}
        rejected={stats.rejected}
      />

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Review Queue */}
        <div className="space-y-4">
          <h2 className="text-xl font-bold text-white">Review Queue</h2>

          {isLoading ? (
            // Loading state
            Array.from({ length: 3 }).map((_, i) => (
              <div key={i} className="bg-slate-800 rounded-lg p-4 animate-pulse">
                <div className="h-6 bg-slate-700 rounded w-3/4 mb-2" />
                <div className="h-4 bg-slate-700 rounded w-full" />
              </div>
            ))
          ) : reviewQueue.length > 0 ? (
            reviewQueue.map((item) => (
              <ReviewQueueItem
                key={item.contentId}
                content={item}
                onSelect={() => setSelectedContent(item)}
              />
            ))
          ) : (
            <div className="text-center py-12 bg-slate-800 border border-slate-700 rounded-lg">
              <div className="text-6xl mb-4">✅</div>
              <p className="text-slate-400">No content awaiting review</p>
            </div>
          )}
        </div>

        {/* Review Panel */}
        <div className="lg:sticky lg:top-24">
          {selectedContent ? (
            <div className="space-y-4">
              {/* Content Preview */}
              <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
                <h3 className="text-lg font-bold text-white mb-4">Content Preview</h3>
                <div className="bg-slate-900 rounded-lg p-4 max-h-64 overflow-auto">
                  <p className="text-slate-300 text-sm">
                    Preview of content would be displayed here. This would show the actual MDX
                    content rendered for review.
                  </p>
                </div>
                <div className="mt-4">
                  <button
                    onClick={() => router.push(`/admin/content/${selectedContent.contentId}/edit`)}
                    className="text-sm text-blue-400 hover:text-blue-300 font-medium"
                  >
                    View Full Content →
                  </button>
                </div>
              </div>

              {/* Review Form */}
              <ReviewPanel content={selectedContent} onReview={handleReview} />
            </div>
          ) : (
            <div className="bg-slate-800 border-2 border-dashed border-slate-700 rounded-lg p-12 text-center">
              <div className="text-6xl mb-4">👈</div>
              <p className="text-slate-400">Select content from the queue to review</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
