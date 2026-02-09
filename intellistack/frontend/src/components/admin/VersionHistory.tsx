/**
 * VersionHistory Component
 *
 * Displays version history with diff view and rollback capability.
 */
'use client';

import { useState } from 'react';
import { cn } from '@/lib/utils';

export interface ContentVersion {
  id: string;
  version_number: string;
  change_summary: string;
  created_by: string;
  created_at: string;
  reviewed_by?: string;
  reviewed_at?: string;
}

interface VersionHistoryProps {
  versions: ContentVersion[];
  currentVersionId: string;
  onRestore?: (versionId: string) => void;
  onViewDiff?: (versionId: string) => void;
  className?: string;
}

export function VersionHistory({
  versions,
  currentVersionId,
  onRestore,
  onViewDiff,
  className,
}: VersionHistoryProps) {
  const [expandedVersion, setExpandedVersion] = useState<string | null>(null);

  return (
    <div className={cn('space-y-3', className)}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-bold text-white">Version History</h3>
        <span className="text-sm text-slate-400">{versions.length} versions</span>
      </div>

      {versions.map((version, index) => {
        const isCurrent = version.id === currentVersionId;
        const isExpanded = expandedVersion === version.id;
        const isLatest = index === 0;

        return (
          <div
            key={version.id}
            className={cn(
              'border rounded-lg transition-all',
              isCurrent
                ? 'border-blue-600 bg-blue-600/10'
                : 'border-slate-700 bg-slate-800 hover:bg-slate-750'
            )}
          >
            {/* Version Header */}
            <button
              onClick={() => setExpandedVersion(isExpanded ? null : version.id)}
              className="w-full p-4 text-left"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className="text-white font-semibold">v{version.version_number}</span>
                    {isCurrent && (
                      <span className="px-2 py-0.5 bg-blue-600 text-white text-xs rounded-full">
                        Current
                      </span>
                    )}
                    {isLatest && !isCurrent && (
                      <span className="px-2 py-0.5 bg-green-600 text-white text-xs rounded-full">
                        Latest
                      </span>
                    )}
                    {version.reviewed_by && (
                      <span className="px-2 py-0.5 bg-green-600/20 text-green-400 text-xs rounded-full">
                        ✓ Reviewed
                      </span>
                    )}
                  </div>
                  <p className="text-slate-300 text-sm mb-1">{version.change_summary}</p>
                  <div className="flex items-center gap-4 text-xs text-slate-400">
                    <span>By {version.created_by}</span>
                    <span>•</span>
                    <span>{new Date(version.created_at).toLocaleString()}</span>
                  </div>
                </div>
                <div className="text-slate-400">
                  <svg
                    className={cn('w-5 h-5 transition-transform', isExpanded && 'rotate-180')}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </div>
              </div>
            </button>

            {/* Expanded Details */}
            {isExpanded && (
              <div className="px-4 pb-4 border-t border-slate-700 pt-4 mt-2">
                {version.reviewed_by && (
                  <div className="bg-slate-900 rounded-lg p-3 mb-3">
                    <div className="text-sm text-slate-300 mb-1">
                      Reviewed by {version.reviewed_by}
                    </div>
                    <div className="text-xs text-slate-400">
                      {version.reviewed_at && new Date(version.reviewed_at).toLocaleString()}
                    </div>
                  </div>
                )}

                <div className="flex gap-2">
                  {onViewDiff && (
                    <button
                      onClick={() => onViewDiff(version.id)}
                      className="flex-1 px-3 py-2 bg-slate-700 hover:bg-slate-600 text-white text-sm rounded transition-colors"
                    >
                      View Changes
                    </button>
                  )}
                  {onRestore && !isCurrent && (
                    <button
                      onClick={() => onRestore(version.id)}
                      className="flex-1 px-3 py-2 bg-yellow-600 hover:bg-yellow-700 text-white text-sm rounded transition-colors"
                    >
                      Restore This Version
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>
        );
      })}

      {versions.length === 0 && (
        <div className="text-center py-12 text-slate-400">
          <p>No version history available</p>
        </div>
      )}
    </div>
  );
}

/**
 * DiffViewer Component
 *
 * Shows differences between two versions
 */
interface DiffViewerProps {
  oldContent: string;
  newContent: string;
  oldVersion: string;
  newVersion: string;
  className?: string;
}

export function DiffViewer({
  oldContent,
  newContent,
  oldVersion,
  newVersion,
  className,
}: DiffViewerProps) {
  // Simple line-by-line diff
  const oldLines = oldContent.split('\n');
  const newLines = newContent.split('\n');
  const maxLength = Math.max(oldLines.length, newLines.length);

  return (
    <div className={cn('bg-slate-900 rounded-lg overflow-hidden', className)}>
      <div className="flex items-center justify-between p-4 bg-slate-800 border-b border-slate-700">
        <span className="text-sm text-red-400">v{oldVersion}</span>
        <span className="text-slate-400">→</span>
        <span className="text-sm text-green-400">v{newVersion}</span>
      </div>

      <div className="grid grid-cols-2 gap-px bg-slate-700">
        {/* Old Version */}
        <div className="bg-slate-900 p-4">
          <div className="text-xs text-red-400 font-semibold mb-2">REMOVED</div>
          <pre className="text-sm text-slate-300 font-mono overflow-x-auto">
            {oldLines.map((line, i) => (
              <div
                key={i}
                className={cn(
                  'leading-relaxed',
                  !newLines[i] || newLines[i] !== line ? 'bg-red-900/30 text-red-300' : ''
                )}
              >
                {line || '\u00A0'}
              </div>
            ))}
          </pre>
        </div>

        {/* New Version */}
        <div className="bg-slate-900 p-4">
          <div className="text-xs text-green-400 font-semibold mb-2">ADDED</div>
          <pre className="text-sm text-slate-300 font-mono overflow-x-auto">
            {newLines.map((line, i) => (
              <div
                key={i}
                className={cn(
                  'leading-relaxed',
                  !oldLines[i] || oldLines[i] !== line ? 'bg-green-900/30 text-green-300' : ''
                )}
              >
                {line || '\u00A0'}
              </div>
            ))}
          </pre>
        </div>
      </div>
    </div>
  );
}
