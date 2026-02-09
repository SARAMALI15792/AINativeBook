/**
 * Rubric Display Component
 * Shows rubric criteria and scoring (FR-045)
 */

'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { Progress } from '../ui/progress';

interface RubricCriterion {
  id: string;
  name: string;
  description: string;
  max_points: number;
  levels: Array<{
    level: number;
    description: string;
    points: number;
  }>;
}

interface RubricDisplayProps {
  rubric: {
    title: string;
    description?: string;
    criteria: RubricCriterion[];
  };
  scores?: Record<string, { level: number; points: number; feedback?: string }>;
  showScores?: boolean;
}

export function RubricDisplay({ rubric, scores, showScores = false }: RubricDisplayProps) {
  const totalMaxPoints = rubric.criteria.reduce((sum, c) => sum + c.max_points, 0);
  const totalEarned = scores
    ? Object.values(scores).reduce((sum, s) => sum + s.points, 0)
    : 0;
  const percentage = totalMaxPoints > 0 ? (totalEarned / totalMaxPoints) * 100 : 0;

  return (
    <div className="space-y-6">
      {/* Rubric Header */}
      <Card>
        <CardHeader>
          <CardTitle>{rubric.title}</CardTitle>
          {rubric.description && <CardDescription>{rubric.description}</CardDescription>}
        </CardHeader>
        {showScores && scores && (
          <CardContent>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="font-medium">Total Score</span>
                <span>
                  {totalEarned.toFixed(1)} / {totalMaxPoints.toFixed(1)} points (
                  {percentage.toFixed(1)}%)
                </span>
              </div>
              <Progress value={percentage} className="h-2" />
            </div>
          </CardContent>
        )}
      </Card>

      {/* Criteria */}
      {rubric.criteria.map((criterion) => {
        const score = scores?.[criterion.id];

        return (
          <Card key={criterion.id}>
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <CardTitle className="text-lg">{criterion.name}</CardTitle>
                  <CardDescription>{criterion.description}</CardDescription>
                </div>
                <Badge variant="outline">{criterion.max_points} pts</Badge>
              </div>
            </CardHeader>
            <CardContent>
              {/* Levels */}
              <div className="space-y-3">
                {criterion.levels
                  .sort((a, b) => b.level - a.level)
                  .map((level) => {
                    const isSelected = score && score.level === level.level;

                    return (
                      <div
                        key={level.level}
                        className={`border rounded-lg p-4 ${
                          isSelected ? 'border-blue-500 bg-blue-50' : 'border-gray-200'
                        }`}
                      >
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex items-center space-x-2">
                            <Badge
                              variant={isSelected ? 'default' : 'secondary'}
                              className={isSelected ? 'bg-blue-600' : ''}
                            >
                              Level {level.level}
                            </Badge>
                            {isSelected && <Badge variant="outline">Selected</Badge>}
                          </div>
                          <span className="font-medium">{level.points} pts</span>
                        </div>
                        <p className="text-sm text-muted-foreground">{level.description}</p>
                      </div>
                    );
                  })}
              </div>

              {/* Feedback */}
              {showScores && score?.feedback && (
                <div className="mt-4 bg-yellow-50 border border-yellow-200 rounded p-3">
                  <div className="text-sm font-medium text-yellow-800 mb-1">Feedback:</div>
                  <p className="text-sm text-yellow-700">{score.feedback}</p>
                </div>
              )}
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}
