import React from 'react';
import { ProgressData } from '../types';

interface StatsPanelProps {
  progress: ProgressData;
  streak: number;
}

export function StatsPanel({ progress, streak }: StatsPanelProps) {
  const accuracy = progress.total.total_attempted > 0
    ? Math.round((progress.total.total_correct / progress.total.total_attempted) * 100)
    : 0;

  const stats = [
    {
      label: 'Current Streak',
      value: streak,
      icon: '🔥',
      color: 'text-orange-500',
    },
    {
      label: 'Day Streak',
      value: progress.goal_streak,
      icon: '📅',
      color: 'text-blue-500',
    },
    {
      label: 'Total Points',
      value: progress.total.total_points,
      icon: '⭐',
      color: 'text-yellow-500',
    },
    {
      label: 'Problems Solved',
      value: progress.total.total_correct,
      icon: '✅',
      color: 'text-green-500',
    },
    {
      label: 'Accuracy',
      value: `${accuracy}%`,
      icon: '🎯',
      color: 'text-purple-500',
    },
  ];

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
      {stats.map((stat) => (
        <div
          key={stat.label}
          className="bg-white rounded-xl p-4 shadow-sm border border-gray-100"
        >
          <div className="flex items-center gap-2 mb-1">
            <span className="text-lg">{stat.icon}</span>
            <span className={`text-2xl font-bold ${stat.color}`}>{stat.value}</span>
          </div>
          <p className="text-xs text-gray-500">{stat.label}</p>
        </div>
      ))}
    </div>
  );
}
