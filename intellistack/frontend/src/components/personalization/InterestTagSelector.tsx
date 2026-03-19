'use client';

import React, { useState } from 'react';

interface InterestTag {
  id: string;
  label: string;
  category: 'robotics' | 'ai' | 'hardware' | 'application';
}

interface InterestTagSelectorProps {
  value: string[];
  onChange: (tags: string[]) => void;
  maxSelection?: number;
  className?: string;
}

export function InterestTagSelector({
  value,
  onChange,
  maxSelection = 10,
  className = '',
}: InterestTagSelectorProps) {
  const [searchQuery, setSearchQuery] = useState('');

  const allTags: InterestTag[] = [
    // Robotics
    { id: 'ros2', label: 'ROS 2', category: 'robotics' },
    { id: 'navigation', label: 'Navigation', category: 'robotics' },
    { id: 'manipulation', label: 'Manipulation', category: 'robotics' },
    { id: 'slam', label: 'SLAM', category: 'robotics' },
    { id: 'path-planning', label: 'Path Planning', category: 'robotics' },
    { id: 'kinematics', label: 'Kinematics', category: 'robotics' },
    { id: 'dynamics', label: 'Dynamics', category: 'robotics' },
    { id: 'control-systems', label: 'Control Systems', category: 'robotics' },

    // AI
    { id: 'computer-vision', label: 'Computer Vision', category: 'ai' },
    { id: 'machine-learning', label: 'Machine Learning', category: 'ai' },
    { id: 'deep-learning', label: 'Deep Learning', category: 'ai' },
    { id: 'reinforcement-learning', label: 'Reinforcement Learning', category: 'ai' },
    { id: 'object-detection', label: 'Object Detection', category: 'ai' },
    { id: 'semantic-segmentation', label: 'Semantic Segmentation', category: 'ai' },
    { id: 'nlp', label: 'Natural Language Processing', category: 'ai' },
    { id: 'sensor-fusion', label: 'Sensor Fusion', category: 'ai' },

    // Hardware
    { id: 'sensors', label: 'Sensors', category: 'hardware' },
    { id: 'actuators', label: 'Actuators', category: 'hardware' },
    { id: 'embedded-systems', label: 'Embedded Systems', category: 'hardware' },
    { id: 'microcontrollers', label: 'Microcontrollers', category: 'hardware' },
    { id: 'lidar', label: 'LiDAR', category: 'hardware' },
    { id: 'cameras', label: 'Cameras', category: 'hardware' },
    { id: 'imu', label: 'IMU', category: 'hardware' },

    // Applications
    { id: 'autonomous-vehicles', label: 'Autonomous Vehicles', category: 'application' },
    { id: 'humanoid-robots', label: 'Humanoid Robots', category: 'application' },
    { id: 'drones', label: 'Drones', category: 'application' },
    { id: 'industrial-automation', label: 'Industrial Automation', category: 'application' },
    { id: 'service-robots', label: 'Service Robots', category: 'application' },
    { id: 'medical-robotics', label: 'Medical Robotics', category: 'application' },
    { id: 'space-robotics', label: 'Space Robotics', category: 'application' },
    { id: 'agricultural-robotics', label: 'Agricultural Robotics', category: 'application' },
  ];

  const filteredTags = searchQuery
    ? allTags.filter((tag) =>
        tag.label.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : allTags;

  const groupedTags = filteredTags.reduce((acc, tag) => {
    if (!acc[tag.category]) {
      acc[tag.category] = [];
    }
    acc[tag.category].push(tag);
    return acc;
  }, {} as Record<string, InterestTag[]>);

  const toggleTag = (tagId: string) => {
    if (value.includes(tagId)) {
      onChange(value.filter((id) => id !== tagId));
    } else if (value.length < maxSelection) {
      onChange([...value, tagId]);
    }
  };

  const categoryLabels = {
    robotics: 'Robotics',
    ai: 'Artificial Intelligence',
    hardware: 'Hardware',
    application: 'Applications',
  };

  const categoryColors = {
    robotics: 'from-accent-cyan to-accent-teal',
    ai: 'from-accent-violet to-pink-500',
    hardware: 'from-accent-teal to-green-500',
    application: 'from-accent-cyan to-accent-violet',
  };

  return (
    <div className={`space-y-6 ${className}`}>
      <div className="space-y-2">
        <h2 className="text-2xl font-bold text-text-primary">What interests you most?</h2>
        <p className="text-text-secondary">
          Select up to {maxSelection} topics you'd like to focus on
        </p>
      </div>

      {/* Selection Counter */}
      <div className="glass backdrop-blur-md rounded-lg p-4 border border-glass-border">
        <div className="flex items-center justify-between">
          <span className="text-text-secondary">Selected topics</span>
          <span className={`text-lg font-semibold ${value.length >= maxSelection ? 'text-accent-violet' : 'text-accent-cyan'}`}>
            {value.length} / {maxSelection}
          </span>
        </div>
        {value.length >= maxSelection && (
          <p className="text-sm text-accent-violet mt-2">
            Maximum selection reached. Deselect a topic to choose another.
          </p>
        )}
      </div>

      {/* Search */}
      <div className="relative">
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search topics..."
          className="w-full px-4 py-3 pl-12 bg-glass-highlight border border-glass-border rounded-lg text-text-primary placeholder-text-tertiary focus:outline-none focus:ring-2 focus:ring-accent-cyan transition-all"
        />
        <svg
          className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-text-tertiary"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
      </div>

      {/* Tags by Category */}
      <div className="space-y-6">
        {Object.entries(groupedTags).map(([category, tags]) => (
          <div key={category} className="space-y-3">
            <div className="flex items-center space-x-2">
              <div className={`w-1 h-6 rounded-full bg-gradient-to-b ${categoryColors[category as keyof typeof categoryColors]}`} />
              <h3 className="text-lg font-semibold text-text-primary">
                {categoryLabels[category as keyof typeof categoryLabels]}
              </h3>
            </div>

            <div className="flex flex-wrap gap-2">
              {tags.map((tag) => {
                const isSelected = value.includes(tag.id);
                const isDisabled = !isSelected && value.length >= maxSelection;

                return (
                  <button
                    key={tag.id}
                    onClick={() => toggleTag(tag.id)}
                    disabled={isDisabled}
                    className={`px-4 py-2 rounded-lg font-medium transition-all focus:outline-none focus:ring-2 focus:ring-accent-cyan ${
                      isSelected
                        ? `bg-gradient-to-r ${categoryColors[category as keyof typeof categoryColors]} text-white shadow-glow-cyan`
                        : isDisabled
                        ? 'bg-glass-highlight text-text-tertiary cursor-not-allowed opacity-50'
                        : 'bg-glass-highlight text-text-secondary hover:bg-glass-border hover:text-text-primary'
                    }`}
                  >
                    {tag.label}
                    {isSelected && (
                      <svg className="inline-block w-4 h-4 ml-2" fill="currentColor" viewBox="0 0 20 20">
                        <path
                          fillRule="evenodd"
                          d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                          clipRule="evenodd"
                        />
                      </svg>
                    )}
                  </button>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      {/* Helper Text */}
      {value.length > 0 && (
        <div className="flex items-start space-x-2 text-sm text-text-tertiary glass backdrop-blur-md rounded-lg p-4 border border-glass-border">
          <svg className="w-5 h-5 flex-shrink-0 mt-0.5 text-accent-cyan" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <p>
            Great choices! We'll prioritize content related to these topics in your learning path.
          </p>
        </div>
      )}
    </div>
  );
}
