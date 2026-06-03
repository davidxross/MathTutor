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

const API_BASE = process.env.REACT_APP_API_BASE ?? 'http://localhost:5001/api';

let authToken: string | null = null;

export function setAuthToken(token: string | null): void {
  authToken = token;
}

async function fetchApi<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options?.headers as Record<string, string>),
  };
  if (authToken) {
    headers['X-User-Token'] = authToken;
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
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
  theme: string
): Promise<Problem> {
  const params = new URLSearchParams({ topic, difficulty, theme });
  return fetchApi<Problem>(`/problem?${params}`);
}

export async function submitAnswer(answer: string): Promise<AnswerResult> {
  return fetchApi<AnswerResult>('/answer', {
    method: 'POST',
    body: JSON.stringify({ answer }),
  });
}

export async function skipProblem(): Promise<{ skipped: boolean; solution: string[]; answer: string }> {
  return fetchApi('/skip', {
    method: 'POST',
    body: JSON.stringify({}),
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
