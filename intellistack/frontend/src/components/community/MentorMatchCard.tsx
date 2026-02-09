import React from 'react';
import { Star, MessageCircle } from 'lucide-react';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

interface MentorMatchCardProps {
  id: string;
  mentorName: string;
  stage: string;
  expertise: string[];
  compatibility: number; // 0-100
  availability: string;
  onConnect?: () => void;
  isLoading?: boolean;
}

export function MentorMatchCard({
  id,
  mentorName,
  stage,
  expertise,
  compatibility,
  availability,
  onConnect,
  isLoading = false,
}: MentorMatchCardProps) {
  const getCompatibilityColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-orange-600';
  };

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            <h3 className="font-semibold text-lg">{mentorName}</h3>
            <p className="text-sm text-gray-600">{stage}</p>
          </div>
          <div className={`flex items-center gap-1 ${getCompatibilityColor(compatibility)}`}>
            <Star className="w-5 h-5 fill-current" />
            <span className="font-semibold">{Math.round(compatibility)}%</span>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          <div>
            <p className="text-xs font-semibold text-gray-600 mb-1">Expertise</p>
            <div className="flex flex-wrap gap-1">
              {expertise.slice(0, 3).map((skill) => (
                <span
                  key={skill}
                  className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>
          <div>
            <p className="text-xs font-semibold text-gray-600 mb-1">Availability</p>
            <p className="text-sm text-gray-700">{availability}</p>
          </div>
          <Button
            onClick={onConnect}
            disabled={isLoading}
            className="w-full"
            variant="default"
          >
            <MessageCircle className="w-4 h-4 mr-2" />
            {isLoading ? 'Connecting...' : 'Connect'}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
