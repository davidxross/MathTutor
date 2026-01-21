import React, { useState } from 'react';
import { useUser } from '../contexts/UserContext';

export function Login() {
  const { users, login, createNewUser, isLoading, error } = useUser();
  const [showCreate, setShowCreate] = useState(false);
  const [newName, setNewName] = useState('');
  const [isCreating, setIsCreating] = useState(false);

  const handleLogin = async (userId: number) => {
    try {
      await login(userId);
    } catch (err) {
      // Error is handled by context
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newName.trim()) return;

    setIsCreating(true);
    try {
      await createNewUser(newName.trim());
    } catch (err) {
      // Error is handled by context
    } finally {
      setIsCreating(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-100 via-white to-primary-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-xl max-w-md w-full overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-primary-500 to-primary-600 p-8 text-center text-white">
          <div className="text-6xl mb-4">🧮</div>
          <h1 className="text-2xl font-bold">Math Tutor</h1>
          <p className="text-primary-100">Grade 5 Canadian Curriculum</p>
        </div>

        <div className="p-6">
          {error && (
            <div className="mb-4 p-3 bg-danger-50 text-danger-600 rounded-lg text-sm">
              {error}
            </div>
          )}

          {isLoading ? (
            <div className="text-center py-8">
              <div className="animate-spin text-4xl mb-4">🔄</div>
              <p className="text-gray-600">Loading...</p>
            </div>
          ) : showCreate ? (
            // Create New User Form
            <form onSubmit={handleCreate} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  What's your name?
                </label>
                <input
                  type="text"
                  value={newName}
                  onChange={(e) => setNewName(e.target.value)}
                  placeholder="Enter your name"
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl
                             focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  autoFocus
                  maxLength={50}
                />
              </div>
              <button
                type="submit"
                disabled={!newName.trim() || isCreating}
                className="w-full py-3 bg-primary-500 hover:bg-primary-600
                           disabled:bg-gray-300 disabled:cursor-not-allowed
                           text-white font-semibold rounded-xl transition-colors"
              >
                {isCreating ? 'Creating...' : 'Start Learning!'}
              </button>
              <button
                type="button"
                onClick={() => setShowCreate(false)}
                className="w-full py-2 text-gray-500 hover:text-gray-700"
              >
                Back to user list
              </button>
            </form>
          ) : (
            // User Selection
            <div className="space-y-4">
              <h2 className="text-lg font-semibold text-gray-800 text-center">
                Who's practicing today?
              </h2>

              {users.length > 0 ? (
                <div className="space-y-2">
                  {users.map((user) => (
                    <button
                      key={user.id}
                      onClick={() => handleLogin(user.id)}
                      className="w-full p-4 bg-gray-50 hover:bg-primary-50
                                 border-2 border-gray-200 hover:border-primary-300
                                 rounded-xl transition-all flex items-center gap-3"
                    >
                      <div className="w-10 h-10 bg-primary-100 rounded-full
                                      flex items-center justify-center text-lg">
                        {user.name.charAt(0).toUpperCase()}
                      </div>
                      <span className="font-medium text-gray-800">{user.name}</span>
                    </button>
                  ))}
                </div>
              ) : (
                <p className="text-center text-gray-500 py-4">
                  No users yet. Create your first profile!
                </p>
              )}

              <div className="pt-4 border-t">
                <button
                  onClick={() => setShowCreate(true)}
                  className="w-full py-3 border-2 border-primary-500 text-primary-600
                             hover:bg-primary-50 font-semibold rounded-xl transition-colors"
                >
                  + Create New Profile
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="bg-gray-50 px-6 py-4 text-center text-sm text-gray-500">
          Learn math with fun themed problems!
        </div>
      </div>
    </div>
  );
}
