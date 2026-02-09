'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { api } from '@/lib/api';

interface ContentItem {
  id: string;
  title: string;
  stage_id: string;
  content_type: string;
  review_status: string;
  version_number: string;
  created_at: string;
  updated_at: string;
}

export default function ContentListPage() {
  const [contents, setContents] = useState<ContentItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [filter, setFilter] = useState({
    status: '',
    stage: '',
  });

  useEffect(() => {
    fetchContents();
  }, [filter]);

  const fetchContents = async () => {
    setIsLoading(true);
    try {
      // TODO: Replace with actual API call
      // const response = await api.fetch('/api/v1/content', {
      //   params: filter
      // });
      // setContents(response.items);

      // Mock data for now
      setContents([
        {
          id: '1',
          title: 'Python Programming Basics',
          stage_id: 'stage-1',
          content_type: 'lesson',
          review_status: 'published',
          version_number: '1.0.3',
          created_at: '2026-01-15T10:00:00Z',
          updated_at: '2026-02-01T14:30:00Z',
        },
        {
          id: '2',
          title: 'ROS 2 Installation Guide',
          stage_id: 'stage-2',
          content_type: 'lesson',
          review_status: 'in_review',
          version_number: '1.0.0',
          created_at: '2026-02-05T09:00:00Z',
          updated_at: '2026-02-05T09:00:00Z',
        },
      ]);
    } catch (error) {
      console.error('Failed to fetch contents:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const statusColors = {
    draft: 'bg-slate-600 text-white',
    in_review: 'bg-yellow-600 text-white',
    published: 'bg-green-600 text-white',
    archived: 'bg-red-600 text-white',
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Content Management</h1>
          <p className="text-slate-400">Create, edit, and review learning content</p>
        </div>
        <Link
          href="/admin/content/new"
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors"
        >
          + Create New Content
        </Link>
      </div>

      {/* Filters */}
      <div className="bg-slate-800 border border-slate-700 rounded-lg p-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">Status</label>
            <select
              value={filter.status}
              onChange={(e) => setFilter({ ...filter, status: e.target.value })}
              className="w-full px-3 py-2 bg-slate-900 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Statuses</option>
              <option value="draft">Draft</option>
              <option value="in_review">In Review</option>
              <option value="published">Published</option>
              <option value="archived">Archived</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">Stage</label>
            <select
              value={filter.stage}
              onChange={(e) => setFilter({ ...filter, stage: e.target.value })}
              className="w-full px-3 py-2 bg-slate-900 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Stages</option>
              <option value="stage-1">Stage 1: Foundations</option>
              <option value="stage-2">Stage 2: ROS 2</option>
              <option value="stage-3">Stage 3: Perception</option>
              <option value="stage-4">Stage 4: AI</option>
              <option value="stage-5">Stage 5: Capstone</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">Type</label>
            <select className="w-full px-3 py-2 bg-slate-900 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option value="">All Types</option>
              <option value="lesson">Lesson</option>
              <option value="exercise">Exercise</option>
              <option value="simulation">Simulation</option>
              <option value="resource">Resource</option>
            </select>
          </div>
        </div>
      </div>

      {/* Content List */}
      <div className="space-y-3">
        {isLoading ? (
          // Loading skeletons
          Array.from({ length: 3 }).map((_, i) => (
            <div
              key={i}
              className="bg-slate-800 border border-slate-700 rounded-lg p-6 animate-pulse"
            >
              <div className="h-6 bg-slate-700 rounded w-2/3 mb-3" />
              <div className="h-4 bg-slate-700 rounded w-full mb-2" />
              <div className="h-4 bg-slate-700 rounded w-3/4" />
            </div>
          ))
        ) : contents.length > 0 ? (
          contents.map((item) => (
            <Link
              key={item.id}
              href={`/admin/content/${item.id}/edit`}
              className="block bg-slate-800 border border-slate-700 hover:border-slate-600 rounded-lg p-6 transition-all"
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <h3 className="text-xl font-semibold text-white mb-2">{item.title}</h3>
                  <div className="flex items-center gap-3 text-sm text-slate-400">
                    <span>v{item.version_number}</span>
                    <span>•</span>
                    <span className="capitalize">{item.content_type}</span>
                    <span>•</span>
                    <span>Updated {new Date(item.updated_at).toLocaleDateString()}</span>
                  </div>
                </div>
                <span
                  className={cn(
                    'px-3 py-1 text-xs font-semibold rounded-full',
                    statusColors[item.review_status as keyof typeof statusColors]
                  )}
                >
                  {item.review_status.replace('_', ' ').toUpperCase()}
                </span>
              </div>
            </Link>
          ))
        ) : (
          <div className="text-center py-12 bg-slate-800 border border-slate-700 rounded-lg">
            <div className="text-6xl mb-4">📝</div>
            <p className="text-slate-400 mb-4">No content found</p>
            <Link
              href="/admin/content/new"
              className="inline-block px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors"
            >
              Create Your First Content
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}
