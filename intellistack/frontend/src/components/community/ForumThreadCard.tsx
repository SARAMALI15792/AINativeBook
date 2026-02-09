import React from 'react';
import Link from 'next/link';
import { formatDistanceToNow } from 'date-fns';
import { MessageSquare, Eye, Pin } from 'lucide-react';
import { Card, CardContent, CardHeader } from '@/components/ui/card';

interface ForumThreadCardProps {
  id: string;
  title: string;
  category: string;
  author: string;
  replies: number;
  views: number;
  isPinned: boolean;
  createdAt: Date;
  lastActivity?: Date;
}

export function ForumThreadCard({
  id,
  title,
  category,
  author,
  replies,
  views,
  isPinned,
  createdAt,
  lastActivity,
}: ForumThreadCardProps) {
  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-2">
              {isPinned && <Pin className="w-4 h-4 text-yellow-500" />}
              <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                {category}
              </span>
            </div>
            <Link href={`/community/forums/${id}`}>
              <h3 className="font-semibold text-lg hover:text-blue-600 line-clamp-2 cursor-pointer">
                {title}
              </h3>
            </Link>
            <p className="text-sm text-gray-600 mt-2">
              by {author} · {formatDistanceToNow(createdAt, { addSuffix: true })}
            </p>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="flex items-center gap-6 text-sm text-gray-600">
          <div className="flex items-center gap-2">
            <MessageSquare className="w-4 h-4" />
            <span>{replies} replies</span>
          </div>
          <div className="flex items-center gap-2">
            <Eye className="w-4 h-4" />
            <span>{views} views</span>
          </div>
          {lastActivity && (
            <div className="text-xs text-gray-500 ml-auto">
              Last: {formatDistanceToNow(lastActivity, { addSuffix: true })}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
