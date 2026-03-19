'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import ContentViewer from '@/components/content/ContentViewer';
import { apiClient } from '@/lib/api-client';

interface PageProps {
  params: {
    stageNum: string;
    slug: string;
  };
}

interface ContentItem {
  id: string;
  title: string;
  slug: string;
  content_type: string;
  order: number;
  estimated_minutes: number;
  is_required: boolean;
  is_completed: boolean;
}

interface ContentUrl {
  url: string;
  content_id: string;
  title: string;
  content_type: string;
  estimated_minutes: number;
  stage_id: string;
  stage_number: number;
}

export default function ContentPage({ params }: PageProps) {
  const router = useRouter();
  const { stageNum, slug } = params;
  const [contentItem, setContentItem] = useState<ContentItem | null>(null);
  const [contentUrl, setContentUrl] = useState<ContentUrl | null>(null);
  const [contentItems, setContentItems] = useState<ContentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<{ status?: number; message: string } | null>(null);

  useEffect(() => {
    const loadContent = async () => {
      try {
        setLoading(true);
        setError(null);

        // Get stage content to find the content item by slug
        const stageSlug = `stage-${stageNum}`;
        const items = await apiClient.getStageContent(stageSlug);
        setContentItems(items);

        // Find content item by slug
        const item = items.find((i: ContentItem) => i.slug === slug);
        if (!item) {
          setError({ status: 404, message: 'Content not found' });
          return;
        }
        setContentItem(item);

        // Get Docusaurus URL for this content
        const urlData = await apiClient.getContentUrl(item.id);
        setContentUrl(urlData);

      } catch (err: any) {
        console.error('Error loading content:', err);
        setError({
          status: err?.error?.code === 'PREREQUISITE_NOT_MET' ? 403 : 500,
          message: err?.message || 'Failed to load content'
        });
      } finally {
        setLoading(false);
      }
    };

    loadContent();
  }, [stageNum, slug]);

  const handleComplete = async () => {
    if (!contentItem) return;

    try {
      await apiClient.completeContent(contentItem.id, { time_spent_minutes: 0 });
      // Update local state
      setContentItem({ ...contentItem, is_completed: true });
    } catch (err) {
      console.error('Error completing content:', err);
    }
  };

  const handleNavigateNext = () => {
    if (!contentItem || !contentItems.length) return;
    const currentIndex = contentItems.findIndex(i => i.id === contentItem.id);
    const nextItem = currentIndex < contentItems.length - 1 ? contentItems[currentIndex + 1] : null;
    if (nextItem) {
      router.push(`/curriculum/stage-${stageNum}/${nextItem.slug}`);
    }
  };

  const handleNavigatePrev = () => {
    if (!contentItem || !contentItems.length) return;
    const currentIndex = contentItems.findIndex(i => i.id === contentItem.id);
    const prevItem = currentIndex > 0 ? contentItems[currentIndex - 1] : null;
    if (prevItem) {
      router.push(`/curriculum/stage-${stageNum}/${prevItem.slug}`);
    }
  };

  if (loading) {
    return (
      <div className="h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">Loading content...</p>
        </div>
      </div>
    );
  }

  if (error) {
    // Handle stage locked error
    if (error.status === 403) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="max-w-md text-center">
            <div className="mb-6">
              <svg
                className="w-20 h-20 mx-auto text-yellow-500"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                />
              </svg>
            </div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2">Stage Locked</h1>
            <p className="text-gray-600 mb-6">
              {error.message || 'You need to complete the previous stage first.'}
            </p>
            <button
              onClick={() => router.push('/curriculum')}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Back to Curriculum
            </button>
          </div>
        </div>
      );
    }

    // Handle not found
    if (error.status === 404) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="max-w-md text-center">
            <h1 className="text-2xl font-bold text-gray-900 mb-2">Content Not Found</h1>
            <p className="text-gray-600 mb-6">The content you're looking for doesn't exist.</p>
            <button
              onClick={() => router.push('/curriculum')}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Back to Curriculum
            </button>
          </div>
        </div>
      );
    }

    // Handle other errors
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="max-w-md text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Error Loading Content</h1>
          <p className="text-gray-600 mb-6">{error.message}</p>
          <button
            onClick={() => router.push('/curriculum')}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Back to Curriculum
          </button>
        </div>
      </div>
    );
  }

  if (!contentItem || !contentUrl) {
    return null;
  }

  const currentIndex = contentItems.findIndex(i => i.id === contentItem.id);
  const hasNext = currentIndex < contentItems.length - 1;
  const hasPrev = currentIndex > 0;

  return (
    <div className="h-screen flex flex-col">
      {/* Breadcrumb */}
      <div className="bg-gray-50 border-b border-gray-200 px-6 py-3">
        <nav className="flex items-center gap-2 text-sm text-gray-600">
          <button onClick={() => router.push('/')} className="hover:text-gray-900">
            Home
          </button>
          <span>/</span>
          <button onClick={() => router.push('/curriculum')} className="hover:text-gray-900">
            Curriculum
          </button>
          <span>/</span>
          <button
            onClick={() => router.push(`/curriculum/stage-${stageNum}`)}
            className="hover:text-gray-900"
          >
            Stage {stageNum}
          </button>
          <span>/</span>
          <span className="text-gray-900 font-medium">{contentItem.title}</span>
        </nav>
      </div>

      {/* Content Viewer */}
      <div className="flex-1 overflow-hidden">
        <ContentViewer
          contentId={contentItem.id}
          docusaurusUrl={contentUrl.url}
          title={contentItem.title}
          estimatedMinutes={contentItem.estimated_minutes}
          isCompleted={contentItem.is_completed}
          onComplete={handleComplete}
          onNavigateNext={hasNext ? handleNavigateNext : undefined}
          onNavigatePrev={hasPrev ? handleNavigatePrev : undefined}
        />
      </div>
    </div>
  );
}
