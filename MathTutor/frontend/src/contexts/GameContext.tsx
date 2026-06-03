import React, { createContext, useContext, useState, useCallback } from 'react';
import { Problem, AnswerResult, GameState } from '../types';
import { getProblem, submitAnswer, skipProblem } from '../utils/api';
import { useUser } from './UserContext';

interface GameContextType extends GameState {
  selectedTopic: string;
  selectedDifficulty: string;
  selectedTheme: string;
  setSelectedTopic: (topic: string) => void;
  setSelectedDifficulty: (difficulty: string) => void;
  setSelectedTheme: (theme: string) => void;
  fetchNewProblem: () => Promise<void>;
  submitUserAnswer: (answer: string) => Promise<AnswerResult>;
  skip: () => Promise<void>;
  clearResult: () => void;
}

const GameContext = createContext<GameContextType | null>(null);

export function GameProvider({ children }: { children: React.ReactNode }) {
  const { user } = useUser();

  const [selectedTopic, setSelectedTopic] = useState('number_sense');
  const [selectedDifficulty, setSelectedDifficulty] = useState('easy');
  const [selectedTheme, setSelectedTheme] = useState('classic');

  const [currentProblem, setCurrentProblem] = useState<Problem | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [answerResult, setAnswerResult] = useState<AnswerResult | null>(null);
  const [showSolution, setShowSolution] = useState(false);
  const [streak, setStreak] = useState(0);
  const [sessionPoints, setSessionPoints] = useState(0);
  const [sessionProblems, setSessionProblems] = useState(0);
  const [sessionCorrect, setSessionCorrect] = useState(0);

  const fetchNewProblem = useCallback(async () => {
    if (!user) return;
    setIsLoading(true);
    setAnswerResult(null);
    setShowSolution(false);
    try {
      const problem = await getProblem(selectedTopic, selectedDifficulty, selectedTheme);
      setCurrentProblem(problem);
    } catch (err) {
      // Silently fail — user sees the empty problem state
    } finally {
      setIsLoading(false);
    }
  }, [user, selectedTopic, selectedDifficulty, selectedTheme]);

  const submitUserAnswer = useCallback(async (answer: string): Promise<AnswerResult> => {
    if (!user) throw new Error('No user');
    const result = await submitAnswer(answer);
    setAnswerResult(result);

    if (result.correct) {
      setStreak(result.points?.new_streak || 0);
      setSessionPoints(prev => prev + (result.points?.total_points || 0));
      setSessionCorrect(prev => prev + 1);
      setSessionProblems(prev => prev + 1);
      setShowSolution(true);
    } else if (result.show_solution) {
      setShowSolution(true);
      setStreak(0);
    }

    return result;
  }, [user]);

  const skip = useCallback(async () => {
    if (!user) return;
    const result = await skipProblem();
    setAnswerResult({
      correct: false,
      answer: result.answer,
      solution: result.solution,
      show_solution: true,
    });
    setShowSolution(true);
    setStreak(0);
  }, [user]);

  const clearResult = useCallback(() => {
    setAnswerResult(null);
    setShowSolution(false);
    setCurrentProblem(null);
  }, []);

  return (
    <GameContext.Provider
      value={{
        currentProblem,
        isLoading,
        answerResult,
        showSolution,
        streak,
        sessionPoints,
        sessionProblems,
        sessionCorrect,
        selectedTopic,
        selectedDifficulty,
        selectedTheme,
        setSelectedTopic,
        setSelectedDifficulty,
        setSelectedTheme,
        fetchNewProblem,
        submitUserAnswer,
        skip,
        clearResult,
      }}
    >
      {children}
    </GameContext.Provider>
  );
}

export function useGame() {
  const context = useContext(GameContext);
  if (!context) {
    throw new Error('useGame must be used within a GameProvider');
  }
  return context;
}
