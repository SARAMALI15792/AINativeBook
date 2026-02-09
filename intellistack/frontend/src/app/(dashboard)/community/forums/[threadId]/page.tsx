'use client';

import React, { useState } from 'react';
import { useParams } from 'next/navigation';
import { ThumbsUp, Reply } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { PostEditor } from '@/components/community';

// Mock thread data
const mockThread = {
  id: '1',
  title: 'How do I set up ROS 2 on Ubuntu?',
  content:
    'I am trying to set up ROS 2 on my Ubuntu 22.04 machine but keep running into dependency issues. Has anyone successfully done this? What steps did you follow?',
  author: 'Alice Johnson',
  authorId: 'alice-123',
  createdAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
  replies: 5,
  views: 42,
  isLocked: false,
};

const mockPosts = [
  {
    id: 'post-1',
    author: 'Bob Smith',
    content:
      'Great question! I recently did this. First, make sure you have the right Ubuntu version. ROS 2 Humble works best with Ubuntu 22.04. Follow the official docs at docs.ros.org.',
    createdAt: new Date(Date.now() - 1.5 * 24 * 60 * 60 * 1000),
    isAnswer: true,
    reactions: 8,
  },
  {
    id: 'post-2',
    author: 'Carol Davis',
    content:
      'Also helpful: add the ROS 2 repository to your apt sources. This usually resolves most dependency issues.',
    createdAt: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000),
    isAnswer: false,
    reactions: 3,
  },
];

export default function ThreadPage() {
  const params = useParams();
  const threadId = params.threadId;
  const [posts, setPosts] = useState(mockPosts);
  const [isReplying, setIsReplying] = useState(false);

  const handlePostReply = (content: string) => {
    const newPost = {
      id: `post-${Date.now()}`,
      author: 'Current User',
      content,
      createdAt: new Date(),
      isAnswer: false,
      reactions: 0,
    };
    setPosts([...posts, newPost]);
    setIsReplying(false);
  };

  return (
    <div className="space-y-6">
      {/* Thread Header */}
      <div className="bg-white rounded-lg p-6 border border-gray-200">
        <h1 className="text-2xl font-bold mb-4">{mockThread.title}</h1>

        <div className="mb-4 text-sm text-gray-600">
          Asked by <span className="font-medium">{mockThread.author}</span> ·{' '}
          {mockThread.createdAt.toLocaleDateString()} · {mockThread.views} views
        </div>

        <p className="text-lg text-gray-800 mb-6">{mockThread.content}</p>

        <div className="flex gap-3">
          <Button variant="outline" size="sm">
            <ThumbsUp className="w-4 h-4 mr-2" /> Upvote
          </Button>
          <Button variant="outline" size="sm">
            <Reply className="w-4 h-4 mr-2" /> Share
          </Button>
        </div>
      </div>

      {/* Answers */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold">{posts.length} Answers</h2>

        {posts.map((post) => (
          <div key={post.id} className="bg-white rounded-lg p-6 border border-gray-200">
            {post.isAnswer && (
              <div className="mb-3 inline-block px-3 py-1 bg-green-100 text-green-700 rounded text-sm font-medium">
                ✓ Accepted Answer
              </div>
            )}

            <div className="mb-4 text-sm text-gray-600">
              <span className="font-medium text-gray-900">{post.author}</span> ·{' '}
              {post.createdAt.toLocaleDateString()}
            </div>

            <p className="text-gray-800 mb-4">{post.content}</p>

            <div className="flex gap-3">
              <Button variant="ghost" size="sm">
                <ThumbsUp className="w-4 h-4 mr-2" /> {post.reactions}
              </Button>
              <Button variant="ghost" size="sm">
                Reply
              </Button>
              {post.isAnswer && (
                <Button variant="ghost" size="sm" disabled>
                  Mark as Answer
                </Button>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Reply Section */}
      {!mockThread.isLocked && (
        <div className="bg-white rounded-lg p-6 border border-gray-200">
          <h3 className="text-lg font-bold mb-4">Your Answer</h3>

          {!isReplying ? (
            <Button onClick={() => setIsReplying(true)} className="w-full">
              Add Your Answer
            </Button>
          ) : (
            <PostEditor
              onSubmit={handlePostReply}
              placeholder="Provide your answer..."
              isReply
            />
          )}
        </div>
      )}
    </div>
  );
}
