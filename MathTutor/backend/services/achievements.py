from typing import Dict, Any, List, Optional
from database.db import get_db, close_db

# Achievement definitions
ACHIEVEMENTS = {
    "quick_learner": {
        "id": "quick_learner",
        "name": "Quick Learner",
        "description": "Get 5 problems correct in a row",
        "icon": "⚡",
        "requirement": {"type": "streak", "value": 5}
    },
    "master_number_sense": {
        "id": "master_number_sense",
        "name": "Number Ninja",
        "description": "Answer 10 Number Sense problems correctly",
        "icon": "🔢",
        "requirement": {"type": "topic_correct", "topic": "number_sense", "value": 10}
    },
    "master_measurement": {
        "id": "master_measurement",
        "name": "Measurement Master",
        "description": "Answer 10 Measurement problems correctly",
        "icon": "📏",
        "requirement": {"type": "topic_correct", "topic": "measurement", "value": 10}
    },
    "master_geometry": {
        "id": "master_geometry",
        "name": "Geometry Genius",
        "description": "Answer 10 Geometry problems correctly",
        "icon": "📐",
        "requirement": {"type": "topic_correct", "topic": "geometry", "value": 10}
    },
    "master_patterning": {
        "id": "master_patterning",
        "name": "Pattern Pro",
        "description": "Answer 10 Patterning & Algebra problems correctly",
        "icon": "🔄",
        "requirement": {"type": "topic_correct", "topic": "patterning", "value": 10}
    },
    "master_data": {
        "id": "master_data",
        "name": "Data Detective",
        "description": "Answer 10 Data Management problems correctly",
        "icon": "📊",
        "requirement": {"type": "topic_correct", "topic": "data_management", "value": 10}
    },
    "week_warrior": {
        "id": "week_warrior",
        "name": "Week Warrior",
        "description": "Complete your daily goal for 7 days in a row",
        "icon": "🏆",
        "requirement": {"type": "goal_streak", "value": 7}
    },
    "perfect_day": {
        "id": "perfect_day",
        "name": "Perfect Day",
        "description": "Get 100% first-try accuracy in a session (min 5 problems)",
        "icon": "⭐",
        "requirement": {"type": "perfect_session", "min_problems": 5}
    },
    "hundred_club": {
        "id": "hundred_club",
        "name": "Hundred Club",
        "description": "Earn 100+ points in a single session",
        "icon": "💯",
        "requirement": {"type": "session_points", "value": 100}
    },
    "math_explorer": {
        "id": "math_explorer",
        "name": "Math Explorer",
        "description": "Try problems from all 5 topics",
        "icon": "🧭",
        "requirement": {"type": "topics_tried", "value": 5}
    },
    "theme_explorer": {
        "id": "theme_explorer",
        "name": "Theme Explorer",
        "description": "Try all 3 different themes",
        "icon": "🎭",
        "requirement": {"type": "themes_tried", "value": 3}
    },
    "persistence": {
        "id": "persistence",
        "name": "Persistent Learner",
        "description": "Attempt 50 problems total",
        "icon": "💪",
        "requirement": {"type": "total_attempted", "value": 50}
    },
    "century": {
        "id": "century",
        "name": "Century Solver",
        "description": "Solve 100 problems correctly",
        "icon": "🎯",
        "requirement": {"type": "total_correct", "value": 100}
    }
}


class AchievementService:
    """Service for tracking and awarding achievements."""

    def __init__(self, user_id: int):
        self.user_id = user_id

    def get_user_achievements(self) -> List[Dict[str, Any]]:
        """Get all achievements earned by the user."""
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            """SELECT achievement_id, earned_at FROM user_achievements
               WHERE user_id = ?
               ORDER BY earned_at DESC""",
            (self.user_id,)
        )
        rows = cursor.fetchall()
        close_db(conn)

        earned = []
        for row in rows:
            achievement_id = row['achievement_id']
            if achievement_id in ACHIEVEMENTS:
                achievement = ACHIEVEMENTS[achievement_id].copy()
                achievement['earned_at'] = row['earned_at']
                earned.append(achievement)

        return earned

    def get_all_achievements_with_status(self) -> List[Dict[str, Any]]:
        """Get all achievements with earned status."""
        earned_ids = {a['id'] for a in self.get_user_achievements()}

        result = []
        for achievement_id, achievement in ACHIEVEMENTS.items():
            item = achievement.copy()
            item['earned'] = achievement_id in earned_ids
            result.append(item)

        return result

    def award_achievement(self, achievement_id: str) -> bool:
        """Award an achievement to the user. Returns True if newly awarded."""
        if achievement_id not in ACHIEVEMENTS:
            return False

        conn = get_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO user_achievements (user_id, achievement_id) VALUES (?, ?)",
                (self.user_id, achievement_id)
            )
            conn.commit()
            close_db(conn)
            return True
        except Exception:  # Already exists
            close_db(conn)
            return False

    def check_and_award(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check if any achievements should be awarded based on context.

        Context should contain:
            - current_streak: int
            - session_points: int
            - session_problems: int
            - session_correct: int
            - session_first_try: int
            - topics_practiced: List[str]
            - themes_used: List[str]
            - total_attempted: int
            - total_correct: int
            - topic_correct: Dict[str, int]  # topic -> correct count
            - goal_streak: int  # consecutive days meeting goal
        """
        new_achievements = []
        earned_ids = {a['id'] for a in self.get_user_achievements()}

        for achievement_id, achievement in ACHIEVEMENTS.items():
            if achievement_id in earned_ids:
                continue

            req = achievement['requirement']
            earned = False

            if req['type'] == 'streak':
                earned = context.get('current_streak', 0) >= req['value']

            elif req['type'] == 'topic_correct':
                topic_counts = context.get('topic_correct', {})
                earned = topic_counts.get(req['topic'], 0) >= req['value']

            elif req['type'] == 'goal_streak':
                earned = context.get('goal_streak', 0) >= req['value']

            elif req['type'] == 'perfect_session':
                problems = context.get('session_problems', 0)
                first_try = context.get('session_first_try', 0)
                correct = context.get('session_correct', 0)
                min_problems = req.get('min_problems', 5)
                earned = (problems >= min_problems and first_try == correct == problems)

            elif req['type'] == 'session_points':
                earned = context.get('session_points', 0) >= req['value']

            elif req['type'] == 'topics_tried':
                topics = context.get('topics_practiced', [])
                earned = len(set(topics)) >= req['value']

            elif req['type'] == 'themes_tried':
                themes = context.get('themes_used', [])
                earned = len(set(themes)) >= req['value']

            elif req['type'] == 'total_attempted':
                earned = context.get('total_attempted', 0) >= req['value']

            elif req['type'] == 'total_correct':
                earned = context.get('total_correct', 0) >= req['value']

            if earned:
                if self.award_achievement(achievement_id):
                    new_achievements.append(achievement)

        return new_achievements

    @staticmethod
    def get_achievement_by_id(achievement_id: str) -> Optional[Dict[str, Any]]:
        """Get achievement definition by ID."""
        return ACHIEVEMENTS.get(achievement_id)
