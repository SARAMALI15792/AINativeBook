/**
 * Cohort Detail Page
 *
 * Displays individual cohort details with student list,
 * instructor assignments, and enrollment management.
 */

'use client';

import { use } from 'react';
import { ArrowLeft, UserPlus, Users } from 'lucide-react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { EnrollmentList } from '@/components/institution/EnrollmentList';
import { InstructorList } from '@/components/institution/InstructorList';
import { CohortStats } from '@/components/institution/CohortStats';

interface CohortDetailPageProps {
  params: Promise<{ cohortId: string }>;
}

export default function CohortDetailPage({ params }: CohortDetailPageProps) {
  const { cohortId } = use(params);

  return (
    <div className="space-y-6">
      {/* Breadcrumb */}
      <Link
        href="/cohorts"
        className="inline-flex items-center text-sm text-muted-foreground hover:text-foreground"
      >
        <ArrowLeft className="h-4 w-4 mr-2" />
        Back to Cohorts
      </Link>

      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">
            Spring 2026 Cohort
          </h1>
          <p className="text-muted-foreground mt-2">
            Jan 15, 2026 - May 15, 2026 • 45 students enrolled
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">
            <Users className="h-4 w-4 mr-2" />
            Manage Instructors
          </Button>
          <Button>
            <UserPlus className="h-4 w-4 mr-2" />
            Enroll Student
          </Button>
        </div>
      </div>

      {/* Stats Overview */}
      <CohortStats cohortId={cohortId} />

      {/* Tabs */}
      <Tabs defaultValue="students" className="space-y-6">
        <TabsList>
          <TabsTrigger value="students">Students</TabsTrigger>
          <TabsTrigger value="instructors">Instructors</TabsTrigger>
          <TabsTrigger value="settings">Settings</TabsTrigger>
        </TabsList>

        <TabsContent value="students" className="space-y-4">
          <EnrollmentList cohortId={cohortId} />
        </TabsContent>

        <TabsContent value="instructors" className="space-y-4">
          <InstructorList cohortId={cohortId} />
        </TabsContent>

        <TabsContent value="settings" className="space-y-4">
          <div className="rounded-lg border bg-card p-6">
            <h3 className="text-lg font-semibold mb-4">Cohort Settings</h3>
            <p className="text-sm text-muted-foreground">
              Settings management coming soon...
            </p>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
