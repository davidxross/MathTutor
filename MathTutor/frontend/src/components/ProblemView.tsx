import React, { useState, useEffect } from 'react';
import { useGame } from '../contexts/GameContext';
import { SolutionModal } from './SolutionModal';
import { Celebration } from './Celebration';
import { Difficulty } from '../types';

interface ProblemViewProps {
  difficulties: Difficulty[];
}

export function ProblemView({ difficulties }: ProblemViewProps) {
  const {
    currentProblem,
    isLoading,
    answerResult,
    showSolution,
    streak,
    selectedDifficulty,
    setSelectedDifficulty,
    fetchNewProblem,
    submitUserAnswer,
    skip,
    clearResult,
  } = useGame();

  const [userAnswer, setUserAnswer] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showCelebration, setShowCelebration] = useState(false);
  const [shake, setShake] = useState(false);

  // Reset answer when getting new problem
  useEffect(() => {
    setUserAnswer('');
  }, [currentProblem]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!userAnswer.trim() || isSubmitting) return;

    setIsSubmitting(true);
    try {
      const result = await submitUserAnswer(userAnswer);
      if (result.correct) {
        setShowCelebration(true);
        setTimeout(() => setShowCelebration(false), 100);
      } else if (!result.show_solution) {
        setShake(true);
        setTimeout(() => setShake(false), 500);
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleSkip = async () => {
    await skip();
  };

  const handleNext = () => {
    clearResult();
    fetchNewProblem();
  };

  const difficultyColors: Record<string, string> = {
    easy: 'bg-success-100 text-success-700 border-success-200',
    medium: 'bg-warning-100 text-warning-700 border-warning-200',
    hard: 'bg-danger-100 text-danger-600 border-danger-200',
  };

  if (!currentProblem && !isLoading) {
    return (
      <div className="bg-white rounded-2xl shadow-lg p-8 text-center">
        <div className="text-6xl mb-4">🧮</div>
        <h2 className="text-xl font-semibold text-gray-800 mb-2">Ready to practice?</h2>
        <p className="text-gray-600 mb-6">Choose your settings and start solving!</p>

        {/* Difficulty selector */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Difficulty</label>
          <div className="flex justify-center gap-2">
            {difficulties.map((diff) => (
              <button
                key={diff.id}
                onClick={() => setSelectedDifficulty(diff.id)}
                className={`
                  px-4 py-2 rounded-lg border-2 font-medium transition-all
                  ${selectedDifficulty === diff.id
                    ? `${difficultyColors[diff.id]} ring-2 ring-offset-1 ring-primary-500`
                    : 'border-gray-200 hover:border-gray-300'
                  }
                `}
              >
                {diff.name} ({diff.points}pts)
              </button>
            ))}
          </div>
        </div>

        <button
          onClick={fetchNewProblem}
          className="px-8 py-3 bg-primary-500 hover:bg-primary-600 text-white
                     font-semibold rounded-xl transition-colors text-lg"
        >
          Start Practice
        </button>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="bg-white rounded-2xl shadow-lg p-8 text-center">
        <div className="animate-spin text-4xl mb-4">🔄</div>
        <p className="text-gray-600">Loading problem...</p>
      </div>
    );
  }

  return (
    <>
      <Celebration trigger={showCelebration} intensity={streak >= 5 ? 'high' : streak >= 3 ? 'medium' : 'low'} />

      <div className={`bg-white rounded-2xl shadow-lg overflow-hidden ${shake ? 'animate-shake' : ''}`}>
        {/* Header */}
        <div className="bg-gradient-to-r from-primary-500 to-primary-600 p-4 text-white">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className={`px-3 py-1 rounded-full text-sm font-medium border ${difficultyColors[currentProblem!.difficulty]}`}>
                {currentProblem!.difficulty}
              </span>
              <span className="text-white/80 text-sm">{currentProblem!.theme_name} Theme</span>
            </div>
            {streak > 0 && (
              <div className="flex items-center gap-1 bg-white/20 px-3 py-1 rounded-full">
                <span>🔥</span>
                <span className="font-bold">{streak}</span>
              </div>
            )}
          </div>
        </div>

        {/* Problem */}
        <div className="p-6">
          <div className="text-lg text-gray-800 whitespace-pre-wrap leading-relaxed mb-6">
            {currentProblem!.question}
          </div>

          {/* Answer input */}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Your Answer
              </label>
              <input
                type="text"
                value={userAnswer}
                onChange={(e) => setUserAnswer(e.target.value)}
                placeholder="Type your answer here..."
                className={`
                  w-full px-4 py-3 border-2 rounded-xl text-lg
                  focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500
                  ${answerResult && !answerResult.correct && !answerResult.show_solution
                    ? 'border-danger-300 bg-danger-50'
                    : 'border-gray-200'
                  }
                `}
                disabled={showSolution}
                autoFocus
              />
              {answerResult && !answerResult.correct && !answerResult.show_solution && (
                <p className="mt-2 text-danger-600 text-sm">
                  {answerResult.hint || `Attempt ${answerResult.attempts}/3`}
                </p>
              )}
            </div>

            <div className="flex gap-3">
              <button
                type="submit"
                disabled={!userAnswer.trim() || isSubmitting || showSolution}
                className="flex-1 py-3 px-6 bg-primary-500 hover:bg-primary-600
                           disabled:bg-gray-300 disabled:cursor-not-allowed
                           text-white font-semibold rounded-xl transition-colors"
              >
                {isSubmitting ? 'Checking...' : 'Submit Answer'}
              </button>
              <button
                type="button"
                onClick={handleSkip}
                disabled={showSolution}
                className="py-3 px-6 border-2 border-gray-300 hover:border-gray-400
                           text-gray-600 font-medium rounded-xl transition-colors
                           disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Skip
              </button>
            </div>
          </form>
        </div>
      </div>

      <SolutionModal
        isOpen={showSolution}
        correct={answerResult?.correct || false}
        answer={answerResult?.answer || ''}
        solution={answerResult?.solution || []}
        points={answerResult?.points}
        newAchievements={answerResult?.new_achievements}
        onNext={handleNext}
      />
    </>
  );
}
