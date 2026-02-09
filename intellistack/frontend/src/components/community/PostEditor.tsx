import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Bold, Italic, Code, Link as LinkIcon } from 'lucide-react';

interface PostEditorProps {
  onSubmit: (content: string) => void;
  isLoading?: boolean;
  placeholder?: string;
  isReply?: boolean;
}

export function PostEditor({
  onSubmit,
  isLoading = false,
  placeholder = 'Write your response...',
  isReply = false,
}: PostEditorProps) {
  const [content, setContent] = useState('');

  const handleSubmit = () => {
    if (content.trim()) {
      onSubmit(content);
      setContent('');
    }
  };

  const insertMarkdown = (before: string, after: string = '') => {
    const textarea = document.querySelector('textarea');
    if (textarea) {
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const selectedText = content.substring(start, end);
      const newContent =
        content.substring(0, start) +
        before +
        selectedText +
        after +
        content.substring(end);
      setContent(newContent);
    }
  };

  return (
    <div className="space-y-3">
      <div className="flex gap-2 pb-2 border-b">
        <Button
          variant="ghost"
          size="sm"
          onClick={() => insertMarkdown('**', '**')}
          title="Bold"
        >
          <Bold className="w-4 h-4" />
        </Button>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => insertMarkdown('*', '*')}
          title="Italic"
        >
          <Italic className="w-4 h-4" />
        </Button>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => insertMarkdown('`', '`')}
          title="Code"
        >
          <Code className="w-4 h-4" />
        </Button>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => insertMarkdown('[', '](url)')}
          title="Link"
        >
          <LinkIcon className="w-4 h-4" />
        </Button>
      </div>

      <Textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder={placeholder}
        className="min-h-24 resize-none"
      />

      <div className="flex justify-end gap-2">
        <Button variant="outline" disabled={isLoading || !content.trim()}>
          Draft
        </Button>
        <Button onClick={handleSubmit} disabled={isLoading || !content.trim()}>
          {isLoading ? 'Posting...' : 'Post'}
        </Button>
      </div>
    </div>
  );
}
