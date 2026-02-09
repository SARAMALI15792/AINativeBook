/**
 * ContentEditor Component
 *
 * Rich MDX editor with live preview, syntax highlighting, and auto-save.
 */
'use client';

import { useState, useEffect, useCallback } from 'react';
import { cn } from '@/lib/utils';

interface ContentEditorProps {
  initialContent?: string;
  onSave?: (content: string) => void;
  onAutoSave?: (content: string) => void;
  autoSaveDelay?: number;
  className?: string;
}

export function ContentEditor({
  initialContent = '',
  onSave,
  onAutoSave,
  autoSaveDelay = 3000,
  className,
}: ContentEditorProps) {
  const [content, setContent] = useState(initialContent);
  const [isSaving, setIsSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  const [showPreview, setShowPreview] = useState(true);
  const [isDirty, setIsDirty] = useState(false);

  // Auto-save functionality
  useEffect(() => {
    if (!isDirty || !onAutoSave) return;

    const timer = setTimeout(() => {
      onAutoSave(content);
      setLastSaved(new Date());
      setIsDirty(false);
    }, autoSaveDelay);

    return () => clearTimeout(timer);
  }, [content, isDirty, onAutoSave, autoSaveDelay]);

  const handleContentChange = (newContent: string) => {
    setContent(newContent);
    setIsDirty(true);
  };

  const handleSave = async () => {
    if (!onSave) return;

    setIsSaving(true);
    try {
      await onSave(content);
      setLastSaved(new Date());
      setIsDirty(false);
    } catch (error) {
      console.error('Save failed:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const insertMarkdown = (markdown: string) => {
    const textarea = document.getElementById('mdx-editor') as HTMLTextAreaElement;
    if (!textarea) return;

    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const before = content.substring(0, start);
    const after = content.substring(end);

    const newContent = before + markdown + after;
    setContent(newContent);
    setIsDirty(true);

    // Reset cursor position
    setTimeout(() => {
      textarea.focus();
      textarea.setSelectionRange(start + markdown.length, start + markdown.length);
    }, 0);
  };

  return (
    <div className={cn('flex flex-col h-full', className)}>
      {/* Toolbar */}
      <div className="flex items-center justify-between p-4 bg-slate-800 border-b border-slate-700">
        <div className="flex items-center gap-2">
          {/* Formatting Buttons */}
          <button
            onClick={() => insertMarkdown('**bold text**')}
            className="px-3 py-1.5 bg-slate-700 hover:bg-slate-600 text-white text-sm rounded transition-colors"
            title="Bold"
          >
            <strong>B</strong>
          </button>
          <button
            onClick={() => insertMarkdown('*italic text*')}
            className="px-3 py-1.5 bg-slate-700 hover:bg-slate-600 text-white text-sm rounded transition-colors"
            title="Italic"
          >
            <em>I</em>
          </button>
          <button
            onClick={() => insertMarkdown('\n```python\n# code here\n```\n')}
            className="px-3 py-1.5 bg-slate-700 hover:bg-slate-600 text-white text-sm rounded transition-colors"
            title="Code Block"
          >
            &lt;/&gt;
          </button>
          <button
            onClick={() => insertMarkdown('\n- List item\n')}
            className="px-3 py-1.5 bg-slate-700 hover:bg-slate-600 text-white text-sm rounded transition-colors"
            title="List"
          >
            ≡
          </button>
          <button
            onClick={() => insertMarkdown('[link text](url)')}
            className="px-3 py-1.5 bg-slate-700 hover:bg-slate-600 text-white text-sm rounded transition-colors"
            title="Link"
          >
            🔗
          </button>
        </div>

        <div className="flex items-center gap-4">
          {/* View Toggle */}
          <div className="flex bg-slate-700 rounded-lg p-1">
            <button
              onClick={() => setShowPreview(false)}
              className={cn(
                'px-3 py-1 text-sm rounded transition-colors',
                !showPreview ? 'bg-slate-600 text-white' : 'text-slate-400 hover:text-white'
              )}
            >
              Edit
            </button>
            <button
              onClick={() => setShowPreview(true)}
              className={cn(
                'px-3 py-1 text-sm rounded transition-colors',
                showPreview ? 'bg-slate-600 text-white' : 'text-slate-400 hover:text-white'
              )}
            >
              Preview
            </button>
          </div>

          {/* Save Status */}
          <div className="text-sm text-slate-400">
            {isSaving && 'Saving...'}
            {!isSaving && isDirty && 'Unsaved changes'}
            {!isSaving && !isDirty && lastSaved && `Saved ${lastSaved.toLocaleTimeString()}`}
          </div>

          {/* Save Button */}
          <button
            onClick={handleSave}
            disabled={isSaving || !isDirty}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 disabled:text-slate-500 text-white font-medium rounded-lg transition-colors"
          >
            {isSaving ? 'Saving...' : 'Save'}
          </button>
        </div>
      </div>

      {/* Editor/Preview Area */}
      <div className="flex-1 flex overflow-hidden">
        {/* Editor */}
        {!showPreview && (
          <div className="flex-1 flex flex-col">
            <textarea
              id="mdx-editor"
              value={content}
              onChange={(e) => handleContentChange(e.target.value)}
              className="flex-1 w-full p-4 bg-slate-900 text-slate-100 font-mono text-sm resize-none focus:outline-none"
              placeholder="Start writing your content in MDX format..."
              spellCheck={false}
            />
          </div>
        )}

        {/* Preview */}
        {showPreview && (
          <div className="flex-1 overflow-auto p-6 bg-slate-900">
            <div className="prose prose-invert max-w-none">
              <MDXPreview content={content} />
            </div>
          </div>
        )}
      </div>

      {/* Character Count */}
      <div className="px-4 py-2 bg-slate-800 border-t border-slate-700 text-xs text-slate-400">
        {content.length} characters | {content.split(/\s+/).filter(Boolean).length} words
      </div>
    </div>
  );
}

/**
 * MDXPreview Component
 *
 * Renders MDX content with basic markdown parsing (simplified preview)
 */
function MDXPreview({ content }: { content: string }) {
  // Basic markdown to HTML conversion (simplified)
  const renderMarkdown = (text: string) => {
    return text
      .split('\n')
      .map((line, i) => {
        // Headers
        if (line.startsWith('# ')) {
          return <h1 key={i} className="text-3xl font-bold mb-4">{line.slice(2)}</h1>;
        }
        if (line.startsWith('## ')) {
          return <h2 key={i} className="text-2xl font-bold mb-3">{line.slice(3)}</h2>;
        }
        if (line.startsWith('### ')) {
          return <h3 key={i} className="text-xl font-bold mb-2">{line.slice(4)}</h3>;
        }

        // Code blocks
        if (line.startsWith('```')) {
          return null; // Handled separately
        }

        // Bold
        let processed = line.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        // Italic
        processed = processed.replace(/\*(.+?)\*/g, '<em>$1</em>');
        // Links
        processed = processed.replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2">$1</a>');

        // Lists
        if (line.startsWith('- ')) {
          return (
            <li key={i} className="mb-1">
              <span dangerouslySetInnerHTML={{ __html: processed.slice(2) }} />
            </li>
          );
        }

        // Paragraphs
        if (line.trim()) {
          return (
            <p key={i} className="mb-4">
              <span dangerouslySetInnerHTML={{ __html: processed }} />
            </p>
          );
        }

        return <br key={i} />;
      });
  };

  // Extract code blocks
  const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
  const parts: JSX.Element[] = [];
  let lastIndex = 0;
  let match;

  while ((match = codeBlockRegex.exec(content)) !== null) {
    // Add text before code block
    if (match.index > lastIndex) {
      const textBefore = content.slice(lastIndex, match.index);
      parts.push(<div key={`text-${lastIndex}`}>{renderMarkdown(textBefore)}</div>);
    }

    // Add code block
    const language = match[1] || 'text';
    const code = match[2];
    parts.push(
      <pre key={`code-${match.index}`} className="bg-slate-800 p-4 rounded-lg overflow-x-auto mb-4">
        <code className={`language-${language} text-sm`}>{code}</code>
      </pre>
    );

    lastIndex = match.index + match[0].length;
  }

  // Add remaining text
  if (lastIndex < content.length) {
    const textAfter = content.slice(lastIndex);
    parts.push(<div key={`text-${lastIndex}`}>{renderMarkdown(textAfter)}</div>);
  }

  return <div>{parts.length > 0 ? parts : renderMarkdown(content)}</div>;
}

/**
 * EditorToolbar Component
 *
 * Standalone toolbar for editor actions
 */
interface EditorToolbarProps {
  onInsert: (text: string) => void;
  onSave?: () => void;
  onPreview?: () => void;
  showPreview?: boolean;
  isSaving?: boolean;
  isDirty?: boolean;
}

export function EditorToolbar({
  onInsert,
  onSave,
  onPreview,
  showPreview,
  isSaving,
  isDirty,
}: EditorToolbarProps) {
  const tools = [
    { label: 'H1', insert: '# Heading 1\n', title: 'Heading 1' },
    { label: 'H2', insert: '## Heading 2\n', title: 'Heading 2' },
    { label: 'B', insert: '**bold**', title: 'Bold' },
    { label: 'I', insert: '*italic*', title: 'Italic' },
    { label: 'Code', insert: '`code`', title: 'Inline Code' },
    { label: 'Block', insert: '\n```\ncode block\n```\n', title: 'Code Block' },
    { label: 'Link', insert: '[text](url)', title: 'Link' },
    { label: 'Image', insert: '![alt](url)', title: 'Image' },
    { label: 'List', insert: '\n- Item 1\n- Item 2\n', title: 'List' },
    { label: 'Quote', insert: '> Quote\n', title: 'Quote' },
  ];

  return (
    <div className="flex items-center gap-2 flex-wrap">
      {tools.map((tool) => (
        <button
          key={tool.label}
          onClick={() => onInsert(tool.insert)}
          className="px-3 py-1.5 bg-slate-700 hover:bg-slate-600 text-white text-xs font-medium rounded transition-colors"
          title={tool.title}
        >
          {tool.label}
        </button>
      ))}
    </div>
  );
}
