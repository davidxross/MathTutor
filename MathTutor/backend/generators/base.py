import random
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class BaseProblemGenerator(ABC):
    """Base class for all problem generators."""

    # Topic identifier
    topic = "base"

    # Display name
    display_name = "Base"

    # Problem types available for this generator
    problem_types = []

    def __init__(self):
        self.difficulty_ranges = {
            "easy": {"min": 1, "max": 10},
            "medium": {"min": 10, "max": 100},
            "hard": {"min": 100, "max": 1000}
        }

    def generate(self, difficulty: str = "easy", problem_type: Optional[str] = None) -> Dict[str, Any]:
        """Generate a problem with the given difficulty and optional type.

        Returns:
            Dict containing:
                - question: The problem text (with placeholders for theming)
                - answer: The correct answer
                - solution: List of step-by-step solution strings
                - difficulty: The difficulty level
                - topic: The topic category
                - problem_type: Specific type of problem
                - theme_data: Data for theme substitution
        """
        if problem_type is None:
            problem_type = random.choice(self.problem_types) if self.problem_types else "default"

        problem = self._generate_problem(difficulty, problem_type)

        # Ensure all required fields are present
        problem.setdefault("difficulty", difficulty)
        problem.setdefault("topic", self.topic)
        problem.setdefault("problem_type", problem_type)
        problem.setdefault("theme_data", {})

        return problem

    @abstractmethod
    def _generate_problem(self, difficulty: str, problem_type: str) -> Dict[str, Any]:
        """Generate a specific problem. Must be implemented by subclasses."""
        pass

    def get_range(self, difficulty: str) -> tuple:
        """Get the number range for a difficulty level."""
        r = self.difficulty_ranges.get(difficulty, self.difficulty_ranges["easy"])
        return r["min"], r["max"]

    def random_in_range(self, difficulty: str) -> int:
        """Get a random number in the difficulty range."""
        min_val, max_val = self.get_range(difficulty)
        return random.randint(min_val, max_val)

    @staticmethod
    def format_answer(answer: Any) -> str:
        """Format an answer for comparison (handles floats, fractions, etc.)."""
        if isinstance(answer, float):
            # Round to 2 decimal places
            return str(round(answer, 2))
        return str(answer)

    @staticmethod
    def check_answer(user_answer: str, correct_answer: Any, tolerance: float = 0.01) -> bool:
        """Check if user's answer is correct."""
        try:
            user_val = float(user_answer.strip())
            correct_val = float(correct_answer)
            return abs(user_val - correct_val) <= tolerance
        except (ValueError, TypeError):
            # String comparison for non-numeric answers
            return user_answer.strip().lower() == str(correct_answer).lower()
