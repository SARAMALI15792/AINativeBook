/**
 * Cohort Table Component
 *
 * Displays cohorts in a table with search and filter functionality.
 * Acceptance: Cohort table with search/filter.
 */

'use client';

import { useState, useEffect } from 'react';
import { MoreHorizontal, Users, Calendar, TrendingUp } from 'lucide-react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';

interface Cohort {
  id: string;
  name: string;
  start_date: string;
  end_date: string;
  enrolled_count: number;
  enrollment_limit: number | null;
  is_enrollment_open: boolean;
  created_at: string;
}

interface CohortTableProps {
  searchQuery: string;
  statusFilter: string;
}

export function CohortTable({ searchQuery, statusFilter }: CohortTableProps) {
  const [cohorts, setCohorts] = useState<Cohort[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // TODO: Replace with actual API call
  useEffect(() => {
    const mockCohorts: Cohort[] = [
      {
        id: '1',
        name: 'Spring 2026 - Physical AI',
        start_date: '2026-01-15',
        end_date: '2026-05-15',
        enrolled_count: 45,
        enrollment_limit: 50,
        is_enrollment_open: true,
        created_at: '2025-11-01T00:00:00Z',
      },
      {
        id: '2',
        name: 'Fall 2025 - Robotics Fundamentals',
        start_date: '2025-08-20',
        end_date: '2025-12-15',
        enrolled_count: 50,
        enrollment_limit: 50,
        is_enrollment_open: false,
        created_at: '2025-06-01T00:00:00Z',
      },
    ];

    setTimeout(() => {
      setCohorts(mockCohorts);
      setIsLoading(false);
    }, 500);
  }, []);

  const filteredCohorts = cohorts.filter((cohort) => {
    const matchesSearch = cohort.name.toLowerCase().includes(searchQuery.toLowerCase());
    const now = new Date();
    const startDate = new Date(cohort.start_date);
    const endDate = new Date(cohort.end_date);

    let matchesFilter = true;
    if (statusFilter === 'active') {
      matchesFilter = startDate <= now && endDate >= now;
    } else if (statusFilter === 'upcoming') {
      matchesFilter = startDate > now;
    } else if (statusFilter === 'completed') {
      matchesFilter = endDate < now;
    } else if (statusFilter === 'enrollment_open') {
      matchesFilter = cohort.is_enrollment_open;
    }

    return matchesSearch && matchesFilter;
  });

  const getStatusBadge = (cohort: Cohort) => {
    const now = new Date();
    const startDate = new Date(cohort.start_date);
    const endDate = new Date(cohort.end_date);

    if (endDate < now) {
      return <Badge variant="secondary">Completed</Badge>;
    } else if (startDate > now) {
      return <Badge variant="outline">Upcoming</Badge>;
    } else {
      return <Badge variant="default">Active</Badge>;
    }
  };

  if (isLoading) {
    return (
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Cohort Name</TableHead>
              <TableHead>Duration</TableHead>
              <TableHead>Students</TableHead>
              <TableHead>Status</TableHead>
              <TableHead></TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {[...Array(5)].map((_, i) => (
              <TableRow key={i}>
                <TableCell>
                  <Skeleton className="h-4 w-[200px]" />
                </TableCell>
                <TableCell>
                  <Skeleton className="h-4 w-[150px]" />
                </TableCell>
                <TableCell>
                  <Skeleton className="h-4 w-[80px]" />
                </TableCell>
                <TableCell>
                  <Skeleton className="h-6 w-[60px]" />
                </TableCell>
                <TableCell>
                  <Skeleton className="h-8 w-8" />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    );
  }

  if (filteredCohorts.length === 0) {
    return (
      <div className="rounded-md border bg-card p-12 text-center">
        <Users className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
        <h3 className="text-lg font-semibold mb-2">No cohorts found</h3>
        <p className="text-sm text-muted-foreground">
          {searchQuery || statusFilter !== 'all'
            ? 'Try adjusting your search or filters'
            : 'Get started by creating your first cohort'}
        </p>
      </div>
    );
  }

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Cohort Name</TableHead>
            <TableHead>Duration</TableHead>
            <TableHead>Students</TableHead>
            <TableHead>Status</TableHead>
            <TableHead className="w-[50px]"></TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {filteredCohorts.map((cohort) => {
            const enrollmentPercent = cohort.enrollment_limit
              ? Math.round((cohort.enrolled_count / cohort.enrollment_limit) * 100)
              : 0;

            return (
              <TableRow key={cohort.id}>
                <TableCell>
                  <Link
                    href={`/cohorts/${cohort.id}`}
                    className="font-medium hover:underline"
                  >
                    {cohort.name}
                  </Link>
                  {cohort.is_enrollment_open && (
                    <Badge variant="secondary" className="ml-2 text-xs">
                      Enrollment Open
                    </Badge>
                  )}
                </TableCell>
                <TableCell>
                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <Calendar className="h-4 w-4" />
                    {new Date(cohort.start_date).toLocaleDateString()} -{' '}
                    {new Date(cohort.end_date).toLocaleDateString()}
                  </div>
                </TableCell>
                <TableCell>
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <Users className="h-4 w-4 text-muted-foreground" />
                      <span className="font-medium">{cohort.enrolled_count}</span>
                      {cohort.enrollment_limit && (
                        <span className="text-sm text-muted-foreground">
                          / {cohort.enrollment_limit}
                        </span>
                      )}
                    </div>
                    {cohort.enrollment_limit && (
                      <div className="flex items-center gap-2 text-xs text-muted-foreground">
                        <div className="w-16 h-1.5 bg-gray-200 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-primary"
                            style={{ width: `${enrollmentPercent}%` }}
                          />
                        </div>
                        <span>{enrollmentPercent}%</span>
                      </div>
                    )}
                  </div>
                </TableCell>
                <TableCell>{getStatusBadge(cohort)}</TableCell>
                <TableCell>
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                        <MoreHorizontal className="h-4 w-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem asChild>
                        <Link href={`/cohorts/${cohort.id}`}>View Details</Link>
                      </DropdownMenuItem>
                      <DropdownMenuItem>Manage Enrollment</DropdownMenuItem>
                      <DropdownMenuItem>View Analytics</DropdownMenuItem>
                      <DropdownMenuItem className="text-destructive">
                        Archive Cohort
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </div>
  );
}
