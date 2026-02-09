import React from 'react';
import Link from 'next/link';
import { Users, Lock } from 'lucide-react';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

interface StudyGroupCardProps {
  id: string;
  name: string;
  description?: string;
  stage: string;
  members: number;
  maxMembers: number;
  isOpen: boolean;
  createdAt: Date;
  onJoin?: () => void;
  isMember?: boolean;
}

export function StudyGroupCard({
  id,
  name,
  description,
  stage,
  members,
  maxMembers,
  isOpen,
  createdAt,
  onJoin,
  isMember = false,
}: StudyGroupCardProps) {
  const isFull = members >= maxMembers;

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            <span className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded block w-fit mb-2">
              {stage}
            </span>
            <Link href={`/community/groups/${id}`}>
              <h3 className="font-semibold text-lg hover:text-blue-600 line-clamp-2 cursor-pointer">
                {name}
              </h3>
            </Link>
            {description && (
              <p className="text-sm text-gray-600 line-clamp-2 mt-1">{description}</p>
            )}
          </div>
          <div className="flex-shrink-0">
            {!isOpen && <Lock className="w-5 h-5 text-gray-400" />}
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <Users className="w-4 h-4" />
            <span>
              {members}/{maxMembers}
            </span>
          </div>
          {isOpen && !isMember && (
            <Button
              size="sm"
              onClick={onJoin}
              disabled={isFull}
            >
              {isFull ? 'Full' : 'Join'}
            </Button>
          )}
          {isMember && (
            <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded">
              Member
            </span>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
