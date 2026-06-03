import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { User, UserSettings } from '../types';
import { getUser, createUser, updateSettings, getUsers, setAuthToken } from '../utils/api';

interface UserContextType {
  user: User | null;
  users: User[];
  isLoading: boolean;
  error: string | null;
  login: (userId: number) => Promise<void>;
  createNewUser: (name: string) => Promise<User>;
  updateUserSettings: (settings: Partial<UserSettings>) => Promise<void>;
  logout: () => void;
  refreshUsers: () => Promise<void>;
}

const UserContext = createContext<UserContextType | null>(null);

export function UserProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refreshUsers = useCallback(async () => {
    try {
      const allUsers = await getUsers();
      setUsers(allUsers);
    } catch (err) {
      console.error('Failed to fetch users:', err);
    }
  }, []);

  // Load user from localStorage on mount
  useEffect(() => {
    const loadUser = async () => {
      const savedUserId = localStorage.getItem('mathTutorUserId');
      const savedToken = localStorage.getItem('mathTutorToken');
      if (savedUserId && savedToken) {
        setAuthToken(savedToken);
        try {
          const userData = await getUser(parseInt(savedUserId, 10));
          setUser(userData);
        } catch (err) {
          localStorage.removeItem('mathTutorUserId');
          localStorage.removeItem('mathTutorToken');
          setAuthToken(null);
        }
      }
      await refreshUsers();
      setIsLoading(false);
    };
    loadUser();
  }, [refreshUsers]);

  const login = async (userId: number) => {
    setIsLoading(true);
    setError(null);
    try {
      const userData = await getUser(userId);
      setUser(userData);
      localStorage.setItem('mathTutorUserId', userId.toString());
      if (userData.token) {
        localStorage.setItem('mathTutorToken', userData.token);
        setAuthToken(userData.token);
      }
    } catch (err) {
      setError('Failed to log in. Please try again.');
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const createNewUser = async (name: string): Promise<User> => {
    setError(null);
    try {
      const newUser = await createUser(name);
      setUser(newUser);
      localStorage.setItem('mathTutorUserId', newUser.id.toString());
      if (newUser.token) {
        localStorage.setItem('mathTutorToken', newUser.token);
        setAuthToken(newUser.token);
      }
      await refreshUsers();
      return newUser;
    } catch (err) {
      setError('Failed to create profile. Please try again.');
      throw err;
    }
  };

  const updateUserSettings = async (settings: Partial<UserSettings>) => {
    if (!user) return;
    setError(null);
    try {
      const updatedUser = await updateSettings(user.id, settings);
      setUser(updatedUser);
    } catch (err) {
      setError('Failed to update settings. Please try again.');
      throw err;
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('mathTutorUserId');
    localStorage.removeItem('mathTutorToken');
    setAuthToken(null);
  };

  return (
    <UserContext.Provider
      value={{
        user,
        users,
        isLoading,
        error,
        login,
        createNewUser,
        updateUserSettings,
        logout,
        refreshUsers,
      }}
    >
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
}
