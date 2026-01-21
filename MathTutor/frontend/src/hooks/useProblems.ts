import { useState, useEffect } from 'react';
import { Topic, Theme, Difficulty } from '../types';
import { getTopics, getThemes, getDifficulties } from '../utils/api';

export function useProblems() {
  const [topics, setTopics] = useState<Topic[]>([]);
  const [themes, setThemes] = useState<Theme[]>([]);
  const [difficulties, setDifficulties] = useState<Difficulty[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadMetadata = async () => {
      try {
        const [topicsData, themesData, difficultiesData] = await Promise.all([
          getTopics(),
          getThemes(),
          getDifficulties(),
        ]);
        setTopics(topicsData);
        setThemes(themesData);
        setDifficulties(difficultiesData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load metadata');
      } finally {
        setIsLoading(false);
      }
    };
    loadMetadata();
  }, []);

  return { topics, themes, difficulties, isLoading, error };
}
