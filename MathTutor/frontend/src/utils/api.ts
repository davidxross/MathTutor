import {
  User,
  Problem,
  AnswerResult,
  ProgressData,
  AchievementsData,
  Topic,
  Theme,
  Difficulty,
} from '../types';

const API_BASE = 'http://localhost:5001/api';

async function fetchApi<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Unknown error' }));
    throw new Error(error.error || `HTTP error ${response.status}`);
  }

  return response.json();
}

// User API
export async function createUser(name: string, settings?: Partial<User['settings']>): Promise<User> {
  return fetchApi<User>('/user', {
    method: 'POST',
    body: JSON.stringify({ name, settings }),
  });
}

export async function getUser(userId: number): Promise<User> {
  return fetchApi<User>(`/user/${userId}`);
}

export async function getUsers(): Promise<User[]> {
  return fetchApi<User[]>('/users');
}

export async function updateSettings(userId: number, settings: Partial<User['settings']>): Promise<User> {
  return fetchApi<User>(`/settings/${userId}`, {
    method: 'PUT',
    body: JSON.stringify(settings),
  });
}

// Problem API
export async function getProblem(
  topic: string,
  difficulty: string,
  theme: string,
  userId?: number
): Promise<Problem> {
  const params = new URLSearchParams({ topic, difficulty, theme });
  if (userId) params.append('user_id', userId.toString());
  return fetchApi<Problem>(`/problem?${params}`);
}

export async function submitAnswer(userId: number, answer: string): Promise<AnswerResult> {
  return fetchApi<AnswerResult>('/answer', {
    method: 'POST',
    body: JSON.stringify({ user_id: userId, answer }),
  });
}

export async function skipProblem(userId: number): Promise<{ skipped: boolean; solution: string[]; answer: string }> {
  return fetchApi('/skip', {
    method: 'POST',
    body: JSON.stringify({ user_id: userId }),
  });
}

// Progress API
export async function getProgress(userId: number, days: number = 30): Promise<ProgressData> {
  return fetchApi<ProgressData>(`/progress/${userId}?days=${days}`);
}

export async function getAchievements(userId: number): Promise<AchievementsData> {
  return fetchApi<AchievementsData>(`/achievements/${userId}`);
}

// Metadata API
export async function getTopics(): Promise<Topic[]> {
  return fetchApi<Topic[]>('/topics');
}

export async function getThemes(): Promise<Theme[]> {
  return fetchApi<Theme[]>('/themes');
}

export async function getDifficulties(): Promise<Difficulty[]> {
  return fetchApi<Difficulty[]>('/difficulties');
}
