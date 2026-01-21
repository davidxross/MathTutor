import React from 'react';
import { Topic } from '../types';
import { useGame } from '../contexts/GameContext';

interface TopicSelectorProps {
  topics: Topic[];
}

export function TopicSelector({ topics }: TopicSelectorProps) {
  const { selectedTopic, setSelectedTopic } = useGame();

  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-gray-700">Topic</label>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
        {topics.map((topic) => (
          <button
            key={topic.id}
            onClick={() => setSelectedTopic(topic.id)}
            className={`
              flex items-center gap-2 p-3 rounded-lg border-2 transition-all
              ${selectedTopic === topic.id
                ? 'border-primary-500 bg-primary-50 text-primary-700'
                : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
              }
            `}
          >
            <span className="text-xl">{topic.icon}</span>
            <span className="font-medium text-sm">{topic.name}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
