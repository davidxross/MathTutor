// User types
export interface UserSettings {
  theme: string;
  difficulty: string;
  daily_goal: number;
  sound_enabled: boolean;
}

export interface User {
  id: number;
  name: string;
  created_at: string;
  settings: UserSettings;
  token?: string;
}

// Problem types
export interface Problem {
  question: string;
  difficulty: string;
  topic: string;
  problem_type: string;
  theme: string;
  theme_name: string;
}

export interface PointsResult {
  base_points: number;
  first_try_bonus: number;
  streak_bonus: number;
  total_points: number;
  new_streak: number;
}

export interface Achievement {
  id: string;
  name: string;
  description: string;
  icon: string;
  earned?: boolean;
  earned_at?: string;
}

export interface AnswerResult {
  correct: boolean;
  answer?: string;
  solution?: string[];
  points?: PointsResult;
  new_achievements?: Achievement[];
  attempts?: number;
  hint?: string;
  show_solution?: boolean;
}

// Progress types
export interface DayProgress {
  id: number;
  user_id: number;
  date: string;
  points_earned: number;
  problems_attempted: number;
  problems_correct: number;
  topics_practiced: string[];
  achievements_earned: string[];
}

export interface TopicStats {
  topic: string;
  attempts: number;
  correct_count: number;
  points: number;
}

export interface TotalStats {
  total_points: number;
  total_attempted: number;
  total_correct: number;
}

export interface SessionStats {
  points: number;
  problems: number;
  correct: number;
}

export interface ProgressData {
  today: DayProgress;
  history: DayProgress[];
  total: TotalStats;
  by_topic: TopicStats[];
  current_streak: number;
  goal_streak: number;
  daily_goal: number;
  session: SessionStats;
}

export interface AchievementsData {
  earned: Achievement[];
  available: Achievement[];
  total_earned: number;
  total_available: number;
}

// Metadata types
export interface Topic {
  id: string;
  name: string;
  icon: string;
}

export interface Theme {
  id: string;
  name: string;
  description: string;
}

export interface Difficulty {
  id: string;
  name: string;
  points: number;
}

// Game state
export interface GameState {
  currentProblem: Problem | null;
  isLoading: boolean;
  answerResult: AnswerResult | null;
  showSolution: boolean;
  streak: number;
  sessionPoints: number;
  sessionProblems: number;
  sessionCorrect: number;
}
