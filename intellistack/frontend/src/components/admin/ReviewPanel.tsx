/**
 * ReviewPanel Component
 *
 * Interface for reviewing and approving/rejecting content.
 */
'use client';

import { useState } from 'react';
import { cn } from '@/lib/utils';

export interface ContentReviewData {
  contentId: string;
  title: string;
  author: string;
  submittedAt: string;
  status: 'pending' | 'approved' | 'rejected';
  currentVersion: string;
}

interface ReviewPanelProps {
  content: ContentReviewData;
  onReview?: (decision: ReviewDecision) => void;
  className?: string;
}

interface ReviewDecision {
  status: 'approved' | 'rejected' | 'changes_requested';
  comments: string;
  rating?: number;
}

export function ReviewPanel({ content, onReview, className }: ReviewPanelProps) {
  const [decision, setDecision] = useState<'approved' | 'rejected' | 'changes_requested' | null>(
    null
  );
  const [comments, setComments] = useState('');
  const [rating, setRating] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async () => {
    if (!decision || !onReview) return;

    setIsSubmitting(true);
    try {
      await onReview({
        status: decision,
        comments,
        rating: rating > 0 ? rating : undefined,
      });
    } catch (error) {
      console.error('Review submission failed:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className={cn('bg-slate-800 border border-slate-700 rounded-lg p-6', className)}>
      <h3 className="text-xl font-bold text-white mb-4">Review Content</h3>

      {/* Content Info */}
      <div className="bg-slate-900 rounded-lg p-4 mb-6">
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-slate-400">Title:</span>
            <span className="text-white ml-2">{content.title}</span>
          </div>
          <div>
            <span className="text-slate-400">Author:</span>
            <span className="text-white ml-2">{content.author}</span>
          </div>
          <div>
            <span className="text-slate-400">Version:</span>
            <span className="text-white ml-2">v{content.currentVersion}</span>
          </div>
          <div>
            <span className="text-slate-400">Submitted:</span>
            <span className="text-white ml-2">
              {new Date(content.submittedAt).toLocaleDateString()}
            </span>
          </div>
        </div>
      </div>

      {/* Decision Buttons */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-slate-300 mb-3">Decision</label>
        <div className="grid grid-cols-3 gap-3">
          <button
            onClick={() => setDecision('approved')}
            className={cn(
              'py-3 px-4 rounded-lg font-medium transition-all',
              decision === 'approved'
                ? 'bg-green-600 text-white ring-2 ring-green-400'
                : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
            )}
          >
            ✓ Approve
          </button>
          <button
            onClick={() => setDecision('changes_requested')}
            className={cn(
              'py-3 px-4 rounded-lg font-medium transition-all',
              decision === 'changes_requested'
                ? 'bg-yellow-600 text-white ring-2 ring-yellow-400'
                : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
            )}
          >
            ⚠ Request Changes
          </button>
          <button
            onClick={() => setDecision('rejected')}
            className={cn(
              'py-3 px-4 rounded-lg font-medium transition-all',
              decision === 'rejected'
                ? 'bg-red-600 text-white ring-2 ring-red-400'
                : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
            )}
          >
            ✗ Reject
          </button>
        </div>
      </div>

      {/* Rating */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-slate-300 mb-3">
          Quality Rating (Optional)
        </label>
        <div className="flex gap-2">
          {[1, 2, 3, 4, 5].map((star) => (
            <button
              key={star}
              onClick={() => setRating(star)}
              className={cn(
                'w-10 h-10 rounded transition-all',
                star <= rating
                  ? 'text-yellow-400 text-2xl'
                  : 'text-slate-600 hover:text-yellow-400 text-2xl'
              )}
            >
              ★
            </button>
          ))}
        </div>
      </div>

      {/* Comments */}
      <div className="mb-6">
        <label htmlFor="review-comments" className="block text-sm font-medium text-slate-300 mb-2">
          Comments {decision === 'changes_requested' && <span className="text-red-400">*</span>}
        </label>
        <textarea
          id="review-comments"
          value={comments}
          onChange={(e) => setComments(e.target.value)}
          rows={6}
          className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          placeholder={
            decision === 'approved'
              ? 'Optional: Add praise or suggestions...'
              : decision === 'changes_requested'
              ? 'Specify what changes are needed...'
              : decision === 'rejected'
              ? 'Explain why this content should be rejected...'
              : 'Provide feedback to the author...'
          }
        />
      </div>

      {/* Submit Button */}
      <button
        onClick={handleSubmit}
        disabled={!decision || isSubmitting || (decision === 'changes_requested' && !comments)}
        className="w-full py-3 px-6 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 disabled:text-slate-500 text-white font-semibold rounded-lg transition-colors"
      >
        {isSubmitting ? 'Submitting...' : 'Submit Review'}
      </button>
    </div>
  );
}

/**
 * ReviewQueueItem Component
 *
 * Card for content awaiting review
 */
interface ReviewQueueItemProps {
  content: ContentReviewData;
  onSelect?: () => void;
  className?: string;
}

export function ReviewQueueItem({ content, onSelect, className }: ReviewQueueItemProps) {
  const statusConfig = {
    pending: { color: 'text-yellow-400', bg: 'bg-yellow-600/20', label: 'Pending Review' },
    approved: { color: 'text-green-400', bg: 'bg-green-600/20', label: 'Approved' },
    rejected: { color: 'text-red-400', bg: 'bg-red-600/20', label: 'Rejected' },
  };

  const config = statusConfig[content.status];

  return (
    <button
      onClick={onSelect}
      className={cn(
        'w-full text-left p-4 bg-slate-800 border border-slate-700 hover:border-slate-600 rounded-lg transition-all',
        className
      )}
    >
      <div className="flex items-start justify-between mb-3">
        <h4 className="text-white font-semibold">{content.title}</h4>
        <span className={cn('px-2 py-1 text-xs rounded-full font-medium', config.bg, config.color)}>
          {config.label}
        </span>
      </div>

      <div className="flex items-center gap-4 text-sm text-slate-400">
        <span>By {content.author}</span>
        <span>•</span>
        <span>v{content.currentVersion}</span>
        <span>•</span>
        <span>{new Date(content.submittedAt).toLocaleDateString()}</span>
      </div>
    </button>
  );
}

/**
 * ReviewStats Component
 *
 * Summary stats for review queue
 */
interface ReviewStatsProps {
  pending: number;
  approved: number;
  rejected: number;
  className?: string;
}

export function ReviewStats({ pending, approved, rejected, className }: ReviewStatsProps) {
  return (
    <div className={cn('grid grid-cols-3 gap-4', className)}>
      <div className="bg-slate-800 border border-yellow-600 rounded-lg p-4">
        <div className="text-3xl font-bold text-yellow-400 mb-1">{pending}</div>
        <div className="text-sm text-slate-400">Pending Review</div>
      </div>
      <div className="bg-slate-800 border border-green-600 rounded-lg p-4">
        <div className="text-3xl font-bold text-green-400 mb-1">{approved}</div>
        <div className="text-sm text-slate-400">Approved</div>
      </div>
      <div className="bg-slate-800 border border-red-600 rounded-lg p-4">
        <div className="text-3xl font-bold text-red-400 mb-1">{rejected}</div>
        <div className="text-sm text-slate-400">Rejected</div>
      </div>
    </div>
  );
}
