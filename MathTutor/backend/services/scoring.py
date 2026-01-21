from typing import Dict, Any

class ScoringService:
    """Service for calculating points and bonuses."""

    # Base points by difficulty
    BASE_POINTS = {
        "easy": 5,
        "medium": 10,
        "hard": 15
    }

    # Bonus points
    FIRST_TRY_BONUS = 2
    STREAK_BONUS = 5
    STREAK_THRESHOLD = 3  # Streak bonus kicks in at 3 correct in a row

    def __init__(self):
        self.current_streak = 0

    def calculate_points(self, difficulty: str, correct: bool, first_try: bool) -> Dict[str, Any]:
        """Calculate points for a problem attempt.

        Returns:
            Dict containing:
                - base_points: Points from difficulty
                - first_try_bonus: Bonus for getting it right first try
                - streak_bonus: Bonus for streak
                - total_points: Sum of all points
                - new_streak: Updated streak count
        """
        if not correct:
            self.current_streak = 0
            return {
                "base_points": 0,
                "first_try_bonus": 0,
                "streak_bonus": 0,
                "total_points": 0,
                "new_streak": 0
            }

        # Base points
        base = self.BASE_POINTS.get(difficulty, self.BASE_POINTS["easy"])

        # First try bonus
        first_bonus = self.FIRST_TRY_BONUS if first_try else 0

        # Update streak
        self.current_streak += 1

        # Streak bonus (only awarded when hitting threshold or multiples)
        streak_bonus = 0
        if self.current_streak >= self.STREAK_THRESHOLD and self.current_streak % self.STREAK_THRESHOLD == 0:
            streak_bonus = self.STREAK_BONUS

        total = base + first_bonus + streak_bonus

        return {
            "base_points": base,
            "first_try_bonus": first_bonus,
            "streak_bonus": streak_bonus,
            "total_points": total,
            "new_streak": self.current_streak
        }

    def get_streak(self) -> int:
        """Get current streak count."""
        return self.current_streak

    def reset_streak(self):
        """Reset the streak (called on incorrect answer)."""
        self.current_streak = 0

    @staticmethod
    def get_difficulty_points(difficulty: str) -> int:
        """Get base points for a difficulty level."""
        return ScoringService.BASE_POINTS.get(difficulty, ScoringService.BASE_POINTS["easy"])
