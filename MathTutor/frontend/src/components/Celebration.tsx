import React, { useEffect } from 'react';
import confetti from 'canvas-confetti';

interface CelebrationProps {
  trigger: boolean;
  intensity?: 'low' | 'medium' | 'high';
}

export function Celebration({ trigger, intensity = 'medium' }: CelebrationProps) {
  useEffect(() => {
    if (!trigger) return;

    const configs = {
      low: { particleCount: 50, spread: 60 },
      medium: { particleCount: 100, spread: 80 },
      high: { particleCount: 200, spread: 120 },
    };

    const config = configs[intensity];

    // Fire confetti from both sides
    confetti({
      ...config,
      origin: { x: 0.1, y: 0.6 },
      angle: 60,
      colors: ['#22c55e', '#0ea5e9', '#f59e0b', '#ec4899'],
    });

    confetti({
      ...config,
      origin: { x: 0.9, y: 0.6 },
      angle: 120,
      colors: ['#22c55e', '#0ea5e9', '#f59e0b', '#ec4899'],
    });

    // Extra burst for high intensity
    if (intensity === 'high') {
      setTimeout(() => {
        confetti({
          particleCount: 80,
          spread: 100,
          origin: { x: 0.5, y: 0.4 },
          colors: ['#fbbf24', '#f97316', '#ef4444'],
        });
      }, 200);
    }
  }, [trigger, intensity]);

  return null;
}
