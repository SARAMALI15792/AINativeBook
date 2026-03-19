'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Header } from '@/components/layout/Header';
import { Footer } from '@/components/layout/Footer';
import { getSession, getJwtToken } from '@/lib/auth';

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

interface Stage {
  id: string;
  number: number;
  name: string;
  slug: string;
  description: string;
  learning_objectives: string[];
  estimated_hours: number;
  content_count: number;
  prerequisite_stage_id: string | null;
  is_active: boolean;
  status: string;
  percentage_complete: number;
  is_accessible: boolean;
}

const STAGE_SLUG = 'stage-5';
const STAGE_NUMBER = 5;
const DOCUSAURUS_URL = process.env.NEXT_PUBLIC_DOCUSAURUS_URL || 'http://localhost:3005/AINativeBook';
const STAGE_DOC_URL = `${DOCUSAURUS_URL}/${STAGE_SLUG}/intro`;

export default function Stage5Page() {
  const router = useRouter();
  const [stage, setStage] = useState<Stage | null>(null);
  const [contentItems, setContentItems] = useState<ContentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [backendDown, setBackendDown] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadStageData = async () => {
      try {
        setLoading(true);

        // Check if user is authenticated
        const user = await getSession();
        if (!user) {
          router.push(`/auth/login?redirect=/curriculum/${STAGE_SLUG}`);
          return;
        }

        const token = await getJwtToken();
        const authHeaders: HeadersInit = token ? { Authorization: `Bearer ${token}` } : {};

        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 5000);

        try {
          const stageResponse = await fetch(
            `${process.env.NEXT_PUBLIC_API_URL}/learning/stages/${STAGE_SLUG}`,
            { headers: authHeaders, credentials: 'include', signal: controller.signal },
          );
          clearTimeout(timeout);

          if (!stageResponse.ok) throw new Error('Failed to fetch stage data');
          const stageData = await stageResponse.json();

          if (!stageData.is_accessible) {
            router.push('/curriculum');
            return;
          }

          setStage(stageData);

          const contentResponse = await fetch(
            `${process.env.NEXT_PUBLIC_API_URL}/learning/stages/${STAGE_SLUG}/content`,
            { headers: authHeaders, credentials: 'include' },
          );
          if (!contentResponse.ok) throw new Error('Failed to fetch content items');
          setContentItems(await contentResponse.json());

        } catch (fetchErr: any) {
          clearTimeout(timeout);
          if (fetchErr.name === 'AbortError' || fetchErr.message?.includes('fetch')) {
            // Backend is unreachable — fall back to Docusaurus link
            setBackendDown(true);
          } else {
            throw fetchErr;
          }
        }

      } catch (err) {
        console.error('Error loading stage data:', err);
        setError('Failed to load stage content. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    loadStageData();
  }, [router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-accent-cyan mb-4" />
          <p className="text-text-primary">Loading stage content...</p>
        </div>
      </div>
    );
  }

  // Backend is offline — show a helpful fallback with Docusaurus link
  if (backendDown) {
    return (
      <main className="relative min-h-screen">
        <Header />
        <div className="container mx-auto px-4 py-20 max-w-2xl">
          <button
            onClick={() => router.push('/curriculum')}
            className="flex items-center text-accent-cyan hover:underline mb-8"
          >
            <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back to Curriculum
          </button>

          <div className="glass backdrop-blur-md rounded-xl p-8 border border-glass-border text-center space-y-6">
            <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-accent-cyan to-accent-violet flex items-center justify-center text-white font-bold text-2xl mx-auto">
              {STAGE_NUMBER}
            </div>
            <h1 className="text-3xl font-bold text-text-primary">Stage {STAGE_NUMBER}: Capstone Project</h1>
            <p className="text-text-secondary">
              The learning content for this stage lives in the Docusaurus platform.
              Click below to open it directly.
            </p>
            <a
              href={STAGE_DOC_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-6 py-3 bg-accent-cyan text-bg-primary rounded-lg font-semibold hover:opacity-90 transition-all hover:shadow-glow-cyan"
            >
              Open Stage {STAGE_NUMBER} in Learning Platform
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
            </a>
            <p className="text-text-tertiary text-xs">Progress tracking requires the backend service to be running.</p>
          </div>
        </div>
        <Footer />
      </main>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center max-w-md mx-auto p-6">
          <div className="text-red-500 text-2xl mb-2">⚠️</div>
          <h2 className="text-xl font-bold text-text-primary mb-2">Error Loading Content</h2>
          <p className="text-text-secondary mb-4">{error}</p>
          <div className="flex gap-3 justify-center">
            <button
              onClick={() => router.push('/curriculum')}
              className="px-4 py-2 bg-accent-cyan text-bg-primary rounded hover:opacity-90 transition-colors"
            >
              Return to Curriculum
            </button>
            <a
              href={STAGE_DOC_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="px-4 py-2 border border-accent-cyan text-accent-cyan rounded hover:bg-accent-cyan/10 transition-colors"
            >
              Open in Docusaurus
            </a>
          </div>
        </div>
      </div>
    );
  }

  if (!stage || contentItems.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-bold text-text-primary mb-2">No Content Available</h2>
          <p className="text-text-secondary">This stage doesn't have any content yet.</p>
        </div>
      </div>
    );
  }

  return (
    <main className="relative min-h-screen">
      <Header />

      <div className="container mx-auto px-4 py-12">
        <div className="mb-8">
          <nav className="mb-6">
            <button
              onClick={() => router.push('/curriculum')}
              className="flex items-center text-accent-cyan hover:underline"
            >
              <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
              Back to Curriculum
            </button>
          </nav>

          <div className="glass backdrop-blur-md rounded-xl p-6 mb-8 border border-glass-border">
            <div className="flex items-start justify-between">
              <div>
                <h1 className="text-3xl md:text-4xl font-bold text-text-primary mb-2">
                  Stage {stage.number}: {stage.name}
                </h1>
                <p className="text-xl text-text-secondary mb-4">{stage.description}</p>
                <div className="flex flex-wrap gap-4 text-sm">
                  <div className="flex items-center">
                    <svg className="w-5 h-5 mr-1 text-accent-cyan" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    ~{stage.estimated_hours} hours
                  </div>
                  <div className="flex items-center">
                    <svg className="w-5 h-5 mr-1 text-accent-cyan" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    {stage.content_count} lessons
                  </div>
                  <div className="flex items-center">
                    <svg className="w-5 h-5 mr-1 text-accent-cyan" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    {stage.percentage_complete.toFixed(0)}% complete
                  </div>
                </div>
              </div>
              <div className="bg-gradient-to-br from-accent-cyan to-accent-violet rounded-lg p-4 text-white text-center min-w-[80px]">
                <div className="text-2xl font-bold">{stage.number}</div>
                <div className="text-xs opacity-90">Stage</div>
              </div>
            </div>
          </div>
        </div>

        <div className="grid gap-4">
          {contentItems.map((item) => (
            <div
              key={item.id}
              className={`glass backdrop-blur-md rounded-xl p-6 border border-glass-border transition-all ${
                item.is_completed ? 'border-accent-cyan bg-accent-cyan/5' : 'hover:border-accent-cyan/50'
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h3 className="text-xl font-semibold text-text-primary mb-2">
                    {item.title}
                    {!item.is_required && (
                      <span className="ml-2 text-xs bg-accent-violet/20 text-accent-violet px-2 py-1 rounded-full">
                        Optional
                      </span>
                    )}
                  </h3>
                  <div className="flex items-center text-sm text-text-tertiary mb-2">
                    <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    {item.estimated_minutes} min
                    {item.is_completed && (
                      <span className="ml-2 text-xs bg-green-500/20 text-green-500 px-2 py-1 rounded-full">
                        Completed
                      </span>
                    )}
                  </div>
                  <p className="text-text-secondary mb-3">
                    {item.content_type.charAt(0).toUpperCase() + item.content_type.slice(1)}
                  </p>
                  <button
                    className="text-accent-cyan hover:underline font-medium flex items-center"
                    onClick={() => router.push(`/curriculum/${STAGE_SLUG}/${item.slug}`)}
                  >
                    View content
                    <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                    </svg>
                  </button>
                </div>
                <div className="flex items-center ml-4">
                  {item.is_completed ? (
                    <div className="w-6 h-6 rounded-full bg-green-500 flex items-center justify-center">
                      <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                  ) : (
                    <div className="w-6 h-6 rounded-full border-2 border-text-tertiary flex items-center justify-center">
                      <div className="w-3 h-3 rounded-full bg-text-tertiary" />
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <Footer />
    </main>
  );
}
