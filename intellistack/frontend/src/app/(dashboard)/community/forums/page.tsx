'use client';

import React, { useState } from 'react';
import { Plus } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ForumThreadCard } from '@/components/community';

// Mock data for demo
const mockThreads = [
  {
    id: '1',
    title: 'How do I set up ROS 2 on Ubuntu?',
    category: 'Q&A',
    author: 'Alice Johnson',
    replies: 5,
    views: 42,
    isPinned: true,
    createdAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000), // 2 days ago
    lastActivity: new Date(Date.now() - 1 * 60 * 60 * 1000), // 1 hour ago
  },
  {
    id: '2',
    title: 'Gazebo simulation performance tips',
    category: 'Tips & Tricks',
    author: 'Bob Smith',
    replies: 12,
    views: 89,
    isPinned: false,
    createdAt: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000), // 5 days ago
    lastActivity: new Date(Date.now() - 3 * 60 * 60 * 1000), // 3 hours ago
  },
  {
    id: '3',
    title: 'My capstone project showcase',
    category: 'Projects',
    author: 'Carol Davis',
    replies: 8,
    views: 156,
    isPinned: false,
    createdAt: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000), // 1 day ago
    lastActivity: new Date(Date.now() - 30 * 60 * 1000), // 30 minutes ago
  },
];

export default function ForumsPage() {
  const [threads, setThreads] = useState(mockThreads);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  const categories = ['Q&A', 'Announcements', 'Tips & Tricks', 'Projects', 'Peer Review'];

  const filteredThreads = selectedCategory
    ? threads.filter((t) => t.category === selectedCategory)
    : threads;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Forums</h2>
        <Button>
          <Plus className="w-4 h-4 mr-2" />
          New Thread
        </Button>
      </div>

      {/* Category Filter */}
      <div className="flex gap-2 flex-wrap">
        <button
          onClick={() => setSelectedCategory(null)}
          className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
            selectedCategory === null
              ? 'bg-purple-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          All
        </button>
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
              selectedCategory === cat
                ? 'bg-purple-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Thread List */}
      <div className="space-y-3">
        {filteredThreads.length > 0 ? (
          filteredThreads.map((thread) => (
            <ForumThreadCard key={thread.id} {...thread} />
          ))
        ) : (
          <div className="text-center py-12 bg-gray-50 rounded-lg">
            <p className="text-gray-600">No threads found in this category</p>
          </div>
        )}
      </div>
    </div>
  );
}
