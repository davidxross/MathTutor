import React from 'react';
import { DayProgress } from '../types';

interface CalendarProps {
  history: DayProgress[];
  dailyGoal: number;
}

export function Calendar({ history, dailyGoal }: CalendarProps) {
  // Get last 30 days
  const days = [];
  const today = new Date();

  for (let i = 29; i >= 0; i--) {
    const date = new Date(today);
    date.setDate(date.getDate() - i);
    days.push(date.toISOString().split('T')[0]);
  }

  const progressMap = new Map(history.map((p) => [p.date, p]));

  const getDayStatus = (dateStr: string) => {
    const progress = progressMap.get(dateStr);
    if (!progress) return 'empty';
    if (progress.problems_correct >= dailyGoal) return 'complete';
    if (progress.problems_correct > 0) return 'partial';
    return 'empty';
  };

  const statusColors = {
    empty: 'bg-gray-100',
    partial: 'bg-primary-200',
    complete: 'bg-success-400',
  };

  return (
    <div className="space-y-2">
      <h3 className="text-lg font-semibold text-gray-800">Last 30 Days</h3>
      <div className="grid grid-cols-10 gap-1">
        {days.map((day) => {
          const status = getDayStatus(day);
          const progress = progressMap.get(day);
          const dayNum = new Date(day).getDate();

          return (
            <div
              key={day}
              className={`
                aspect-square rounded-md flex items-center justify-center
                text-xs font-medium transition-colors cursor-default
                ${statusColors[status]}
                ${status === 'complete' ? 'text-white' : 'text-gray-600'}
              `}
              title={`${day}: ${progress?.problems_correct || 0}/${dailyGoal} problems`}
            >
              {dayNum}
            </div>
          );
        })}
      </div>
      <div className="flex items-center gap-4 text-xs text-gray-500 mt-2">
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded bg-gray-100" />
          <span>No activity</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded bg-primary-200" />
          <span>Some progress</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded bg-success-400" />
          <span>Goal met!</span>
        </div>
      </div>
    </div>
  );
}
