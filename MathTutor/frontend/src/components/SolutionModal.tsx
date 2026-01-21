import React from 'react';
import { PointsResult, Achievement } from '../types';

interface SolutionModalProps {
  isOpen: boolean;
  correct: boolean;
  answer: string;
  solution: string[];
  points?: PointsResult;
  newAchievements?: Achievement[];
  onNext: () => void;
}

export function SolutionModal({
  isOpen,
  correct,
  answer,
  solution,
  points,
  newAchievements,
  onNext,
}: SolutionModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div
        className={`
          bg-white rounded-2xl shadow-2xl max-w-lg w-full max-h-[90vh] overflow-y-auto
          animate-bounce-in
        `}
      >
        {/* Header */}
        <div
          className={`
            p-6 text-center
            ${correct
              ? 'bg-gradient-to-br from-success-400 to-success-500'
              : 'bg-gradient-to-br from-orange-400 to-orange-500'
            }
          `}
        >
          <div className="text-5xl mb-2">{correct ? '🎉' : '📚'}</div>
          <h2 className="text-2xl font-bold text-white">
            {correct ? 'Correct!' : 'Keep Learning!'}
          </h2>
          {correct && points && (
            <div className="mt-3 flex justify-center gap-4 text-white/90">
              <span>+{points.total_points} points</span>
              {points.first_try_bonus > 0 && <span>First try bonus!</span>}
              {points.streak_bonus > 0 && <span>Streak bonus!</span>}
            </div>
          )}
        </div>

        {/* Content */}
        <div className="p-6 space-y-4">
          {/* Answer */}
          <div className="text-center">
            <p className="text-sm text-gray-500 mb-1">The answer is</p>
            <p className="text-2xl font-bold text-gray-800">{answer}</p>
          </div>

          {/* Solution Steps */}
          <div>
            <h3 className="font-semibold text-gray-700 mb-2">How to solve it:</h3>
            <ol className="space-y-2">
              {solution.map((step, index) => (
                <li key={index} className="flex gap-2 text-gray-600">
                  <span className="flex-shrink-0 w-6 h-6 rounded-full bg-primary-100 text-primary-600
                                   text-sm font-medium flex items-center justify-center">
                    {index + 1}
                  </span>
                  <span className="pt-0.5">{step}</span>
                </li>
              ))}
            </ol>
          </div>

          {/* New Achievements */}
          {newAchievements && newAchievements.length > 0 && (
            <div className="mt-4 p-4 bg-gradient-to-br from-yellow-50 to-amber-50 rounded-xl border border-yellow-200">
              <h3 className="font-semibold text-amber-800 mb-2">New Achievement!</h3>
              {newAchievements.map((achievement) => (
                <div key={achievement.id} className="flex items-center gap-3">
                  <span className="text-3xl">{achievement.icon}</span>
                  <div>
                    <p className="font-medium text-gray-800">{achievement.name}</p>
                    <p className="text-sm text-gray-600">{achievement.description}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-6 pt-0">
          <button
            onClick={onNext}
            className="w-full py-3 px-6 bg-primary-500 hover:bg-primary-600
                       text-white font-semibold rounded-xl transition-colors"
          >
            Next Problem
          </button>
        </div>
      </div>
    </div>
  );
}
