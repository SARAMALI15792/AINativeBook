'use client';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export function ProgressDistribution() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Progress Distribution</CardTitle>
      </CardHeader>
      <CardContent className="h-[300px] flex items-center justify-center">
        <p className="text-sm text-muted-foreground">Progress distribution chart placeholder</p>
      </CardContent>
    </Card>
  );
}
