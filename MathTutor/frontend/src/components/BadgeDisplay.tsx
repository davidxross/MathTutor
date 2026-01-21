import React from 'react';
import { Achievement } from '../types';

interface BadgeDisplayProps {
  earned: Achievement[];
  available: Achievement[];
}

export function BadgeDisplay({ earned, available }: BadgeDisplayProps) {
  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-800">
        Achievements ({earned.length}/{earned.length + available.length})
      </h3>

      {earned.length > 0 && (
        <div>
          <h4 className="text-sm font-medium text-gray-600 mb-2">Earned</h4>
          <div className="flex flex-wrap gap-3">
            {earned.map((badge) => (
              <div
                key={badge.id}
                className="flex items-center gap-2 bg-gradient-to-br from-yellow-50 to-amber-50
                           border border-yellow-200 rounded-lg px-3 py-2 shadow-sm"
                title={badge.description}
              >
                <span className="text-2xl">{badge.icon}</span>
                <div>
                  <p className="font-medium text-sm text-gray-800">{badge.name}</p>
                  <p className="text-xs text-gray-500">{badge.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {available.length > 0 && (
        <div>
          <h4 className="text-sm font-medium text-gray-600 mb-2">Available</h4>
          <div className="flex flex-wrap gap-3">
            {available.map((badge) => (
              <div
                key={badge.id}
                className="flex items-center gap-2 bg-gray-50 border border-gray-200
                           rounded-lg px-3 py-2 opacity-60"
                title={badge.description}
              >
                <span className="text-2xl grayscale">{badge.icon}</span>
                <div>
                  <p className="font-medium text-sm text-gray-600">{badge.name}</p>
                  <p className="text-xs text-gray-400">{badge.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
