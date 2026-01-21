import React from 'react';
import { Theme } from '../types';
import { useGame } from '../contexts/GameContext';

interface ThemeSelectorProps {
  themes: Theme[];
}

const themeIcons: Record<string, string> = {
  classic: '📚',
  stranger_things: '🔦',
  puppy: '🐕',
};

const themeColors: Record<string, string> = {
  classic: 'border-gray-400 bg-gray-50',
  stranger_things: 'border-red-400 bg-red-50',
  puppy: 'border-amber-400 bg-amber-50',
};

export function ThemeSelector({ themes }: ThemeSelectorProps) {
  const { selectedTheme, setSelectedTheme } = useGame();

  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-gray-700">Theme</label>
      <div className="flex flex-wrap gap-2">
        {themes.map((theme) => (
          <button
            key={theme.id}
            onClick={() => setSelectedTheme(theme.id)}
            className={`
              flex items-center gap-2 px-4 py-2 rounded-full border-2 transition-all
              ${selectedTheme === theme.id
                ? `${themeColors[theme.id] || 'border-primary-500 bg-primary-50'} ring-2 ring-offset-1 ring-primary-500`
                : 'border-gray-200 hover:border-gray-300'
              }
            `}
          >
            <span>{themeIcons[theme.id] || '🎨'}</span>
            <span className="font-medium">{theme.name}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
