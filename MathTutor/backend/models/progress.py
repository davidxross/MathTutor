import json
from datetime import date, datetime, timedelta
from database.db import get_db, close_db, dict_from_row

class Progress:
    """Progress tracking model for user performance."""

    def __init__(self, id=None, user_id=None, date=None, points_earned=0,
                 problems_attempted=0, problems_correct=0, topics_practiced=None,
                 achievements_earned=None):
        self.id = id
        self.user_id = user_id
        self.date = date
        self.points_earned = points_earned
        self.problems_attempted = problems_attempted
        self.problems_correct = problems_correct
        self.topics_practiced = topics_practiced or []
        self.achievements_earned = achievements_earned or []

    @staticmethod
    def get_or_create_today(user_id):
        """Get today's progress or create if doesn't exist."""
        conn = get_db()
        cursor = conn.cursor()
        today = date.today().isoformat()

        cursor.execute(
            "SELECT * FROM progress WHERE user_id = ? AND date = ?",
            (user_id, today)
        )
        row = cursor.fetchone()

        if not row:
            cursor.execute(
                "INSERT INTO progress (user_id, date) VALUES (?, ?)",
                (user_id, today)
            )
            conn.commit()
            cursor.execute(
                "SELECT * FROM progress WHERE user_id = ? AND date = ?",
                (user_id, today)
            )
            row = cursor.fetchone()

        close_db(conn)

        data = dict_from_row(row)
        data['topics_practiced'] = json.loads(data['topics_practiced']) if data['topics_practiced'] else []
        data['achievements_earned'] = json.loads(data['achievements_earned']) if data['achievements_earned'] else []
        return Progress(**data)

    @staticmethod
    def get_user_history(user_id, days=30):
        """Get progress history for a user over the last N days."""
        conn = get_db()
        cursor = conn.cursor()
        start_date = (date.today() - timedelta(days=days)).isoformat()

        cursor.execute(
            """SELECT * FROM progress
               WHERE user_id = ? AND date >= ?
               ORDER BY date DESC""",
            (user_id, start_date)
        )
        rows = cursor.fetchall()
        close_db(conn)

        history = []
        for row in rows:
            data = dict_from_row(row)
            data['topics_practiced'] = json.loads(data['topics_practiced']) if data['topics_practiced'] else []
            data['achievements_earned'] = json.loads(data['achievements_earned']) if data['achievements_earned'] else []
            history.append(Progress(**data))
        return history

    @staticmethod
    def get_streak(user_id, daily_goal=10):
        """Calculate current streak (consecutive days meeting goal)."""
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            """SELECT date, problems_correct FROM progress
               WHERE user_id = ?
               ORDER BY date DESC""",
            (user_id,)
        )
        rows = cursor.fetchall()
        close_db(conn)

        if not rows:
            return 0

        streak = 0
        expected_date = date.today()

        for row in rows:
            row_date = date.fromisoformat(row['date'])
            if row_date != expected_date:
                # Allow for yesterday if today hasn't started
                if streak == 0 and row_date == expected_date - timedelta(days=1):
                    expected_date = row_date
                else:
                    break

            if row['problems_correct'] >= daily_goal:
                streak += 1
                expected_date = row_date - timedelta(days=1)
            else:
                break

        return streak

    def update(self, points=0, attempted=0, correct=0, topic=None, achievement=None):
        """Update progress for today."""
        self.points_earned += points
        self.problems_attempted += attempted
        self.problems_correct += correct

        if topic and topic not in self.topics_practiced:
            self.topics_practiced.append(topic)

        if achievement and achievement not in self.achievements_earned:
            self.achievements_earned.append(achievement)

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE progress SET
               points_earned = ?, problems_attempted = ?, problems_correct = ?,
               topics_practiced = ?, achievements_earned = ?
               WHERE id = ?""",
            (self.points_earned, self.problems_attempted, self.problems_correct,
             json.dumps(self.topics_practiced), json.dumps(self.achievements_earned), self.id)
        )
        conn.commit()
        close_db(conn)

    @staticmethod
    def record_problem(user_id, problem_type, topic, difficulty, correct, first_try, points):
        """Record a problem attempt in history."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO problem_history
               (user_id, problem_type, topic, difficulty, correct, first_try, points_earned)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (user_id, problem_type, topic, difficulty, correct, first_try, points)
        )
        conn.commit()
        close_db(conn)

    @staticmethod
    def get_total_stats(user_id):
        """Get total stats for a user across all time."""
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            """SELECT
               COALESCE(SUM(points_earned), 0) as total_points,
               COALESCE(SUM(problems_attempted), 0) as total_attempted,
               COALESCE(SUM(problems_correct), 0) as total_correct
               FROM progress WHERE user_id = ?""",
            (user_id,)
        )
        row = cursor.fetchone()
        close_db(conn)

        return dict_from_row(row) if row else {"total_points": 0, "total_attempted": 0, "total_correct": 0}

    @staticmethod
    def get_topic_stats(user_id):
        """Get performance breakdown by topic."""
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            """SELECT topic,
               COUNT(*) as attempts,
               SUM(CASE WHEN correct THEN 1 ELSE 0 END) as correct_count,
               SUM(points_earned) as points
               FROM problem_history
               WHERE user_id = ?
               GROUP BY topic""",
            (user_id,)
        )
        rows = cursor.fetchall()
        close_db(conn)

        return [dict_from_row(row) for row in rows]

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "date": self.date,
            "points_earned": self.points_earned,
            "problems_attempted": self.problems_attempted,
            "problems_correct": self.problems_correct,
            "topics_practiced": self.topics_practiced,
            "achievements_earned": self.achievements_earned
        }
