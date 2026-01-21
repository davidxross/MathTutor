import React from 'react';

interface ProgressBarProps {
  current: number;
  goal: number;
  label?: string;
  showCount?: boolean;
}

export function ProgressBar({ current, goal, label, showCount = true }: ProgressBarProps) {
  const percentage = Math.min((current / goal) * 100, 100);
  const isComplete = current >= goal;

  return (
    <div className="space-y-1">
      {(label || showCount) && (
        <div className="flex justify-between items-center text-sm">
          {label && <span className="font-medium text-gray-700">{label}</span>}
          {showCount && (
            <span className={`font-medium ${isComplete ? 'text-success-600' : 'text-gray-600'}`}>
              {current} / {goal}
            </span>
          )}
        </div>
      )}
      <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-500 ease-out ${
            isComplete
              ? 'bg-gradient-to-r from-success-400 to-success-500'
              : 'bg-gradient-to-r from-primary-400 to-primary-500'
          }`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
