'use client';

import React, { useState } from 'react';
import { Plus } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { StudyGroupCard } from '@/components/community';

// Mock study groups
const mockGroups = [
  {
    id: '1',
    name: 'ROS 2 Gazebo Masters',
    description: 'Advanced simulation techniques and optimization',
    stage: 'Stage 2',
    members: 8,
    maxMembers: 12,
    isOpen: true,
    createdAt: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000),
    isMember: false,
  },
  {
    id: '2',
    name: 'Computer Vision Study Circle',
    description: 'Deep dive into perception algorithms',
    stage: 'Stage 3',
    members: 12,
    maxMembers: 12,
    isOpen: false,
    createdAt: new Date(Date.now() - 20 * 24 * 60 * 60 * 1000),
    isMember: true,
  },
  {
    id: '3',
    name: 'ML for Robotics',
    description: 'Learning reinforcement learning applications',
    stage: 'Stage 4',
    members: 5,
    maxMembers: 10,
    isOpen: true,
    createdAt: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000),
    isMember: false,
  },
];

export default function StudyGroupsPage() {
  const [groups, setGroups] = useState(mockGroups);
  const [selectedStage, setSelectedStage] = useState<string | null>(null);

  const stages = ['Stage 1', 'Stage 2', 'Stage 3', 'Stage 4', 'Stage 5'];

  const filteredGroups = selectedStage
    ? groups.filter((g) => g.stage === selectedStage)
    : groups;

  const handleJoinGroup = (groupId: string) => {
    setGroups(
      groups.map((g) =>
        g.id === groupId ? { ...g, isMember: true, members: g.members + 1 } : g
      )
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Study Groups</h2>
        <Button>
          <Plus className="w-4 h-4 mr-2" />
          Create Group
        </Button>
      </div>

      {/* Stage Filter */}
      <div className="flex gap-2 flex-wrap">
        <button
          onClick={() => setSelectedStage(null)}
          className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
            selectedStage === null
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          All
        </button>
        {stages.map((stage) => (
          <button
            key={stage}
            onClick={() => setSelectedStage(stage)}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
              selectedStage === stage
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            {stage}
          </button>
        ))}
      </div>

      {/* Groups Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredGroups.length > 0 ? (
          filteredGroups.map((group) => (
            <StudyGroupCard
              key={group.id}
              {...group}
              onJoin={() => handleJoinGroup(group.id)}
            />
          ))
        ) : (
          <div className="col-span-2 text-center py-12 bg-gray-50 rounded-lg">
            <p className="text-gray-600">No groups found in this stage</p>
          </div>
        )}
      </div>
    </div>
  );
}
