/**
 * TextSelectionQuery Component
 *
 * Floating button that appears when text is selected to ask questions (FR-068).
 */

'use client';

import { useState, useEffect, useRef } from 'react';
import { MessageCircleQuestion, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import { Input } from '@/components/ui/input';

interface TextSelectionQueryProps {
  onQuery: (query: string, selectedText: string) => void;
}

export function TextSelectionQuery({ onQuery }: TextSelectionQueryProps) {
  const [selectedText, setSelectedText] = useState('');
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [isVisible, setIsVisible] = useState(false);
  const [query, setQuery] = useState('');
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      const text = selection?.toString().trim();

      if (text && text.length > 0) {
        setSelectedText(text);

        // Get selection position
        const range = selection?.getRangeAt(0);
        const rect = range?.getBoundingClientRect();

        if (rect) {
          setPosition({
            x: rect.left + rect.width / 2,
            y: rect.top - 10,
          });
          setIsVisible(true);
        }
      } else {
        setIsVisible(false);
        setIsOpen(false);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('selectionchange', handleSelection);

    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('selectionchange', handleSelection);
    };
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onQuery(query, selectedText);
      setQuery('');
      setIsVisible(false);
      setIsOpen(false);
      window.getSelection()?.removeAllRanges();
    }
  };

  if (!isVisible) return null;

  return (
    <div
      className="fixed z-50"
      style={{
        left: `${position.x}px`,
        top: `${position.y}px`,
        transform: 'translate(-50%, -100%)',
      }}
    >
      <Popover open={isOpen} onOpenChange={setIsOpen}>
        <PopoverTrigger asChild>
          <Button
            size="sm"
            className="shadow-lg"
            onClick={() => setIsOpen(true)}
          >
            <MessageCircleQuestion className="h-4 w-4 mr-2" />
            Ask about selection
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-80">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <h4 className="font-semibold text-sm">Ask about selected text</h4>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => {
                  setIsOpen(false);
                  setIsVisible(false);
                }}
              >
                <X className="h-4 w-4" />
              </Button>
            </div>

            <div className="p-2 bg-muted rounded text-sm max-h-20 overflow-auto">
              "{selectedText}"
            </div>

            <form onSubmit={handleSubmit} className="space-y-2">
              <Input
                placeholder="What would you like to know?"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                autoFocus
              />
              <Button type="submit" size="sm" className="w-full">
                Ask Question
              </Button>
            </form>
          </div>
        </PopoverContent>
      </Popover>
    </div>
  );
}
