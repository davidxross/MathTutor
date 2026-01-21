import React, { useEffect } from 'react';
import { useUser } from '../contexts/UserContext';
import { useGame } from '../contexts/GameContext';
import { useProblems } from '../hooks/useProblems';
import { useProgress } from '../hooks/useProgress';
import { TopicSelector } from './TopicSelector';
import { ThemeSelector } from './ThemeSelector';
import { ProblemView } from './ProblemView';
import { ProgressBar } from './ProgressBar';
import { StatsPanel } from './StatsPanel';
import { BadgeDisplay } from './BadgeDisplay';
import { Calendar } from './Calendar';

export function Dashboard() {
  const { user, logout } = useUser();
  const { streak, sessionPoints, sessionCorrect } = useGame();
  const { topics, themes, difficulties, isLoading: metaLoading } = useProblems();
  const { progress, achievements, refresh } = useProgress();

  // Refresh progress when session stats change
  useEffect(() => {
    if (sessionCorrect > 0) {
      refresh();
    }
  }, [sessionCorrect, refresh]);

  if (!user) return null;
  if (metaLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin text-4xl mb-4">🔄</div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-100">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="text-3xl">🧮</span>
              <div>
                <h1 className="text-xl font-bold text-gray-800">Math Tutor</h1>
                <p className="text-sm text-gray-500">Grade 5 Canadian Curriculum</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="font-medium text-gray-800">{user.name}</p>
                <p className="text-sm text-gray-500">
                  {sessionPoints > 0 && `+${sessionPoints} pts this session`}
                </p>
              </div>
              <button
                onClick={logout}
                className="text-sm text-gray-500 hover:text-gray-700"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-6 space-y-6">
        {/* Daily Progress */}
        {progress && (
          <div className="bg-white rounded-xl p-4 shadow-sm">
            <ProgressBar
              current={progress.today.problems_correct}
              goal={progress.daily_goal}
              label="Daily Goal"
            />
          </div>
        )}

        {/* Stats */}
        {progress && <StatsPanel progress={progress} streak={streak} />}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Settings & Problem */}
          <div className="lg:col-span-2 space-y-6">
            {/* Selectors */}
            <div className="bg-white rounded-xl p-6 shadow-sm space-y-4">
              <TopicSelector topics={topics} />
              <ThemeSelector themes={themes} />
            </div>

            {/* Problem View */}
            <ProblemView difficulties={difficulties} />
          </div>

          {/* Right Column - Progress & Achievements */}
          <div className="space-y-6">
            {/* Achievements */}
            {achievements && (
              <div className="bg-white rounded-xl p-6 shadow-sm">
                <BadgeDisplay
                  earned={achievements.earned}
                  available={achievements.available}
                />
              </div>
            )}

            {/* Calendar */}
            {progress && (
              <div className="bg-white rounded-xl p-6 shadow-sm">
                <Calendar history={progress.history} dailyGoal={progress.daily_goal} />
              </div>
            )}

            {/* Topic Progress */}
            {progress && progress.by_topic.length > 0 && (
              <div className="bg-white rounded-xl p-6 shadow-sm">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Topic Progress</h3>
                <div className="space-y-3">
                  {progress.by_topic.map((topic) => {
                    const accuracy = topic.attempts > 0
                      ? Math.round((topic.correct_count / topic.attempts) * 100)
                      : 0;
                    const topicName = topics.find(t => t.id === topic.topic)?.name || topic.topic;

                    return (
                      <div key={topic.topic}>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-gray-700">{topicName}</span>
                          <span className="text-gray-500">
                            {topic.correct_count} correct ({accuracy}%)
                          </span>
                        </div>
                        <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-primary-500 rounded-full"
                            style={{ width: `${Math.min(accuracy, 100)}%` }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
