import json
from database.db import get_db, close_db, dict_from_row

class User:
    """User model for managing student profiles."""

    def __init__(self, id=None, name=None, created_at=None, settings=None):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.settings = settings or {
            "theme": "classic",
            "difficulty": "easy",
            "daily_goal": 10,
            "sound_enabled": True
        }

    @staticmethod
    def create(name, settings=None):
        """Create a new user."""
        conn = get_db()
        cursor = conn.cursor()

        default_settings = {
            "theme": "classic",
            "difficulty": "easy",
            "daily_goal": 10,
            "sound_enabled": True
        }
        if settings:
            default_settings.update(settings)

        cursor.execute(
            "INSERT INTO users (name, settings) VALUES (?, ?)",
            (name, json.dumps(default_settings))
        )
        user_id = cursor.lastrowid
        conn.commit()
        close_db(conn)

        return User.get_by_id(user_id)

    @staticmethod
    def get_by_id(user_id):
        """Get user by ID."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        close_db(conn)

        if row:
            data = dict_from_row(row)
            data['settings'] = json.loads(data['settings']) if data['settings'] else {}
            return User(**data)
        return None

    @staticmethod
    def get_all():
        """Get all users."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
        rows = cursor.fetchall()
        close_db(conn)

        users = []
        for row in rows:
            data = dict_from_row(row)
            data['settings'] = json.loads(data['settings']) if data['settings'] else {}
            users.append(User(**data))
        return users

    def update_settings(self, new_settings):
        """Update user settings."""
        self.settings.update(new_settings)
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET settings = ? WHERE id = ?",
            (json.dumps(self.settings), self.id)
        )
        conn.commit()
        close_db(conn)

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "settings": self.settings
        }
