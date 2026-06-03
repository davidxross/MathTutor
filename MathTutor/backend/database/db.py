import sqlite3
import json
import secrets
from pathlib import Path

DATABASE_PATH = Path(__file__).parent / "math_tutor.db"

def get_db():
    """Get database connection with row factory for dict-like access."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def close_db(conn):
    """Close database connection."""
    if conn:
        conn.close()

def init_db():
    """Initialize the database with required tables."""
    conn = get_db()
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            settings TEXT DEFAULT '{}',
            secret_token TEXT NOT NULL DEFAULT ''
        )
    ''')

    # Daily progress table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER REFERENCES users(id),
            date DATE DEFAULT (date('now')),
            points_earned INTEGER DEFAULT 0,
            problems_attempted INTEGER DEFAULT 0,
            problems_correct INTEGER DEFAULT 0,
            topics_practiced TEXT DEFAULT '[]',
            achievements_earned TEXT DEFAULT '[]',
            UNIQUE(user_id, date)
        )
    ''')

    # Problem history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS problem_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER REFERENCES users(id),
            problem_type TEXT,
            topic TEXT,
            difficulty TEXT,
            correct BOOLEAN,
            first_try BOOLEAN,
            points_earned INTEGER DEFAULT 0,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Achievements table (tracks which badges each user has earned)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER REFERENCES users(id),
            achievement_id TEXT NOT NULL,
            earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, achievement_id)
        )
    ''')

    conn.commit()

    # Migration: add secret_token to existing databases that predate this column
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN secret_token TEXT NOT NULL DEFAULT ''")
        conn.commit()
    except Exception:
        pass  # Column already exists

    # Backfill tokens for any users that don't have one yet
    cursor.execute("SELECT id FROM users WHERE secret_token = ''")
    rows = cursor.fetchall()
    for row in rows:
        cursor.execute("UPDATE users SET secret_token = ? WHERE id = ?",
                       (secrets.token_hex(32), row['id']))
    if rows:
        conn.commit()

    close_db(conn)
    print(f"Database initialized at {DATABASE_PATH}")

def dict_from_row(row):
    """Convert sqlite3.Row to dictionary."""
    if row is None:
        return None
    return dict(row)
