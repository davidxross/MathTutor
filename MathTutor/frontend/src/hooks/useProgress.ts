import { useState, useEffect, useCallback } from 'react';
import { ProgressData, AchievementsData } from '../types';
import { getProgress, getAchievements } from '../utils/api';
import { useUser } from '../contexts/UserContext';

export function useProgress() {
  const { user } = useUser();
  const [progress, setProgress] = useState<ProgressData | null>(null);
  const [achievements, setAchievements] = useState<AchievementsData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    if (!user) return;
    setIsLoading(true);
    setError(null);
    try {
      const [progressData, achievementsData] = await Promise.all([
        getProgress(user.id),
        getAchievements(user.id),
      ]);
      setProgress(progressData);
      setAchievements(achievementsData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load progress');
    } finally {
      setIsLoading(false);
    }
  }, [user]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  return { progress, achievements, isLoading, error, refresh };
}
