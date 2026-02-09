'use client';

import React, { useState } from 'react';
import { Search } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { MentorMatchCard } from '@/components/community';

// Mock mentor data
const mockMentors = [
  {
    id: '1',
    mentorName: 'Dr. Emma Wilson',
    stage: 'Stage 5 - Capstone Expert',
    expertise: ['ROS 2', 'Gazebo', 'Python'],
    compatibility: 92,
    availability: '3-5 hours/week',
  },
  {
    id: '2',
    mentorName: 'James Chen',
    stage: 'Stage 4 - ML Integration',
    expertise: ['Machine Learning', 'TensorFlow', 'Computer Vision'],
    compatibility: 78,
    availability: '2-3 hours/week',
  },
  {
    id: '3',
    mentorName: 'Sarah Ahmed',
    stage: 'Stage 3 - Perception',
    expertise: ['OpenCV', 'Point Clouds', 'Simulation'],
    compatibility: 65,
    availability: '4-6 hours/week',
  },
  {
    id: '4',
    mentorName: 'Michael Rodriguez',
    stage: 'Stage 4 - ML Integration',
    expertise: ['Reinforcement Learning', 'PyTorch', 'Sim-to-Real'],
    compatibility: 88,
    availability: '2-4 hours/week',
  },
];

export default function MentorshipPage() {
  const [mentors, setMentors] = useState(mockMentors);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeConnections, setActiveConnections] = useState<Set<string>>(new Set());
  const [loadingMentors, setLoadingMentors] = useState<Set<string>>(new Set());

  const filteredMentors = mentors.filter(
    (m) =>
      m.mentorName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      m.expertise.some((e) => e.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  const handleConnect = (mentorId: string) => {
    setLoadingMentors(new Set(loadingMentors).add(mentorId));
    // Simulate API call
    setTimeout(() => {
      setActiveConnections(new Set(activeConnections).add(mentorId));
      setLoadingMentors((prev) => {
        const newSet = new Set(prev);
        newSet.delete(mentorId);
        return newSet;
      });
    }, 1000);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold mb-2">Find a Mentor</h2>
        <p className="text-gray-600">
          Connect with experienced learners who can guide your learning journey
        </p>
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
        <Input
          placeholder="Search by name or expertise..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="pl-10"
        />
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
          <p className="text-sm text-blue-600 font-semibold">Available Mentors</p>
          <p className="text-3xl font-bold text-blue-900">{filteredMentors.length}</p>
        </div>
        <div className="bg-purple-50 rounded-lg p-4 border border-purple-200">
          <p className="text-sm text-purple-600 font-semibold">Your Connections</p>
          <p className="text-3xl font-bold text-purple-900">{activeConnections.size}</p>
        </div>
        <div className="bg-green-50 rounded-lg p-4 border border-green-200">
          <p className="text-sm text-green-600 font-semibold">Avg Compatibility</p>
          <p className="text-3xl font-bold text-green-900">
            {Math.round(
              filteredMentors.reduce((sum, m) => sum + m.compatibility, 0) /
                filteredMentors.length
            )}
            %
          </p>
        </div>
      </div>

      {/* Mentor Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredMentors.length > 0 ? (
          filteredMentors.map((mentor) => (
            <MentorMatchCard
              key={mentor.id}
              {...mentor}
              onConnect={() => handleConnect(mentor.id)}
              isLoading={loadingMentors.has(mentor.id)}
            />
          ))
        ) : (
          <div className="col-span-2 text-center py-12 bg-gray-50 rounded-lg">
            <p className="text-gray-600">No mentors found matching your search</p>
          </div>
        )}
      </div>

      {/* Active Connections */}
      {activeConnections.size > 0 && (
        <div className="bg-green-50 rounded-lg p-6 border border-green-200">
          <h3 className="text-lg font-semibold text-green-900 mb-3">Active Mentorships</h3>
          <p className="text-green-700">
            You have {activeConnections.size} active mentorship connection
            {activeConnections.size > 1 ? 's' : ''}. Check your messages to chat with your
            mentors.
          </p>
        </div>
      )}
    </div>
  );
}
