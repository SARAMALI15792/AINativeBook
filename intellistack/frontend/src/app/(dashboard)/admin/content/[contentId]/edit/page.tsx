'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { ContentEditor } from '@/components/admin/ContentEditor';
import { VersionHistory, ContentVersion } from '@/components/admin/VersionHistory';
import { cn } from '@/lib/utils';

export default function ContentEditPage() {
  const params = useParams();
  const router = useRouter();
  const contentId = params.contentId as string;

  const [content, setContent] = useState('');
  const [title, setTitle] = useState('');
  const [metadata, setMetadata] = useState({
    stage: 'stage-1',
    type: 'lesson',
    status: 'draft',
  });
  const [versions, setVersions] = useState<ContentVersion[]>([]);
  const [activeTab, setActiveTab] = useState<'editor' | 'versions' | 'settings'>('editor');
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    if (contentId !== 'new') {
      fetchContent();
      fetchVersions();
    } else {
      setIsLoading(false);
    }
  }, [contentId]);

  const fetchContent = async () => {
    try {
      // TODO: Replace with actual API call
      // const data = await api.fetch(`/api/v1/content/${contentId}`);

      // Mock data
      setTitle('Python Programming Basics');
      setContent('# Python Programming\n\nLearn Python fundamentals...');
      setMetadata({
        stage: 'stage-1',
        type: 'lesson',
        status: 'draft',
      });
    } catch (error) {
      console.error('Failed to fetch content:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchVersions = async () => {
    try {
      // TODO: Replace with actual API call
      // const data = await api.fetch(`/api/v1/content/${contentId}/versions`);

      // Mock data
      setVersions([
        {
          id: '1',
          version_number: '1.0.2',
          change_summary: 'Fixed typos and updated examples',
          created_by: 'john@example.com',
          created_at: '2026-02-08T10:00:00Z',
          reviewed_by: 'reviewer@example.com',
          reviewed_at: '2026-02-08T11:00:00Z',
        },
        {
          id: '2',
          version_number: '1.0.1',
          change_summary: 'Added practice exercises',
          created_by: 'john@example.com',
          created_at: '2026-02-07T14:00:00Z',
        },
        {
          id: '3',
          version_number: '1.0.0',
          change_summary: 'Initial version',
          created_by: 'john@example.com',
          created_at: '2026-02-01T09:00:00Z',
        },
      ]);
    } catch (error) {
      console.error('Failed to fetch versions:', error);
    }
  };

  const handleSave = async (changeSummary: string) => {
    setIsSaving(true);
    try {
      // TODO: Replace with actual API call
      // await api.fetch(`/api/v1/content/${contentId}`, {
      //   method: 'PUT',
      //   body: JSON.stringify({ title, content, change_summary: changeSummary })
      // });

      console.log('Content saved:', { title, content, changeSummary });
      alert('Content saved successfully!');
    } catch (error) {
      console.error('Save failed:', error);
      alert('Failed to save content');
    } finally {
      setIsSaving(false);
    }
  };

  const handleAutoSave = async (content: string) => {
    // Auto-save without creating new version
    console.log('Auto-saving...', content.length);
  };

  const handleSubmitForReview = async () => {
    if (!confirm('Submit this content for review?')) return;

    try {
      // TODO: Replace with actual API call
      // await api.fetch(`/api/v1/content/${contentId}/submit`, { method: 'POST' });

      alert('Content submitted for review!');
      router.push('/admin/content');
    } catch (error) {
      console.error('Submit failed:', error);
      alert('Failed to submit for review');
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-slate-400">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <Link
              href="/admin/content"
              className="text-slate-400 hover:text-white transition-colors"
            >
              ← Back to Content
            </Link>
          </div>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="text-2xl font-bold text-white bg-transparent border-none focus:outline-none focus:ring-0"
            placeholder="Untitled Content"
          />
        </div>

        <div className="flex items-center gap-3">
          <span
            className={cn(
              'px-3 py-1 text-sm font-semibold rounded-full',
              metadata.status === 'published' && 'bg-green-600 text-white',
              metadata.status === 'in_review' && 'bg-yellow-600 text-white',
              metadata.status === 'draft' && 'bg-slate-600 text-white'
            )}
          >
            {metadata.status.replace('_', ' ').toUpperCase()}
          </span>

          {metadata.status === 'draft' && (
            <button
              onClick={handleSubmitForReview}
              className="px-4 py-2 bg-yellow-600 hover:bg-yellow-700 text-white font-medium rounded-lg transition-colors"
            >
              Submit for Review
            </button>
          )}
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-700 mb-6">
        <button
          onClick={() => setActiveTab('editor')}
          className={cn(
            'px-6 py-3 font-medium transition-colors',
            activeTab === 'editor'
              ? 'text-blue-400 border-b-2 border-blue-400'
              : 'text-slate-400 hover:text-white'
          )}
        >
          Editor
        </button>
        <button
          onClick={() => setActiveTab('versions')}
          className={cn(
            'px-6 py-3 font-medium transition-colors',
            activeTab === 'versions'
              ? 'text-blue-400 border-b-2 border-blue-400'
              : 'text-slate-400 hover:text-white'
          )}
        >
          Versions ({versions.length})
        </button>
        <button
          onClick={() => setActiveTab('settings')}
          className={cn(
            'px-6 py-3 font-medium transition-colors',
            activeTab === 'settings'
              ? 'text-blue-400 border-b-2 border-blue-400'
              : 'text-slate-400 hover:text-white'
          )}
        >
          Settings
        </button>
      </div>

      {/* Tab Content */}
      <div className="flex-1 overflow-hidden">
        {activeTab === 'editor' && (
          <ContentEditor
            initialContent={content}
            onSave={(newContent) => {
              const changeSummary = prompt('Describe your changes:');
              if (changeSummary) {
                handleSave(changeSummary);
              }
            }}
            onAutoSave={handleAutoSave}
            className="h-full"
          />
        )}

        {activeTab === 'versions' && (
          <div className="h-full overflow-auto bg-slate-900 rounded-lg p-6">
            <VersionHistory
              versions={versions}
              currentVersionId={versions[0]?.id}
              onRestore={(versionId) => {
                if (confirm('Restore this version? Current changes will be saved as a new version.')) {
                  console.log('Restoring version:', versionId);
                }
              }}
              onViewDiff={(versionId) => {
                console.log('View diff for:', versionId);
                // TODO: Show diff modal
              }}
            />
          </div>
        )}

        {activeTab === 'settings' && (
          <div className="h-full overflow-auto bg-slate-900 rounded-lg p-6">
            <div className="max-w-2xl space-y-6">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Stage</label>
                <select
                  value={metadata.stage}
                  onChange={(e) => setMetadata({ ...metadata, stage: e.target.value })}
                  className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="stage-1">Stage 1: Foundations</option>
                  <option value="stage-2">Stage 2: ROS 2 & Simulation</option>
                  <option value="stage-3">Stage 3: Perception</option>
                  <option value="stage-4">Stage 4: AI Integration</option>
                  <option value="stage-5">Stage 5: Capstone</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Content Type</label>
                <select
                  value={metadata.type}
                  onChange={(e) => setMetadata({ ...metadata, type: e.target.value })}
                  className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="lesson">Lesson</option>
                  <option value="exercise">Exercise</option>
                  <option value="simulation">Simulation</option>
                  <option value="resource">Resource</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Learning Objectives
                </label>
                <textarea
                  rows={4}
                  className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                  placeholder="Enter learning objectives (one per line)"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Estimated Minutes
                </label>
                <input
                  type="number"
                  min="5"
                  max="300"
                  className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="45"
                />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
