'use client';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export function CompletionRatesChart() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Completion Rates</CardTitle>
      </CardHeader>
      <CardContent className="h-[300px] flex items-center justify-center">
        <p className="text-sm text-muted-foreground">Completion rates chart placeholder</p>
      </CardContent>
    </Card>
  );
}
