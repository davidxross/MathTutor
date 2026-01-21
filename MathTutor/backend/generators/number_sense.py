import random
from fractions import Fraction
from typing import Dict, Any
from .base import BaseProblemGenerator

class NumberSenseGenerator(BaseProblemGenerator):
    """Generator for number sense and numeration problems."""

    topic = "number_sense"
    display_name = "Number Sense & Numeration"
    problem_types = ["multiplication", "division", "fractions", "decimals", "percentages"]

    def __init__(self):
        super().__init__()
        self.difficulty_ranges = {
            "easy": {"min": 2, "max": 12},
            "medium": {"min": 10, "max": 50},
            "hard": {"min": 25, "max": 100}
        }

    def _generate_problem(self, difficulty: str, problem_type: str) -> Dict[str, Any]:
        generators = {
            "multiplication": self._gen_multiplication,
            "division": self._gen_division,
            "fractions": self._gen_fractions,
            "decimals": self._gen_decimals,
            "percentages": self._gen_percentages
        }
        return generators.get(problem_type, self._gen_multiplication)(difficulty)

    def _gen_multiplication(self, difficulty: str) -> Dict[str, Any]:
        min_val, max_val = self.get_range(difficulty)
        a = random.randint(min_val, max_val)
        b = random.randint(min_val, max_val)
        answer = a * b

        # Theme-friendly template
        templates = [
            {
                "question": "{name} has {a} {container_plural} with {b} {item_plural} in each. How many {item_plural} are there in total?",
                "theme_data": {
                    "name": "Alex",
                    "container": "box",
                    "container_plural": "boxes",
                    "item": "marble",
                    "item_plural": "marbles"
                }
            },
            {
                "question": "If there are {a} {group_plural} and each {group} has {b} {item_plural}, what is the total number of {item_plural}?",
                "theme_data": {
                    "group": "team",
                    "group_plural": "teams",
                    "item": "player",
                    "item_plural": "players"
                }
            }
        ]

        template = random.choice(templates)
        question = template["question"].format(a=a, b=b, **template["theme_data"])

        return {
            "question": question,
            "answer": answer,
            "solution": [
                f"We need to multiply {a} × {b}",
                f"{a} × {b} = {answer}",
                f"The answer is {answer}"
            ],
            "theme_data": {**template["theme_data"], "a": a, "b": b}
        }

    def _gen_division(self, difficulty: str) -> Dict[str, Any]:
        min_val, max_val = self.get_range(difficulty)
        divisor = random.randint(min_val, max_val)
        quotient = random.randint(min_val, max_val)
        dividend = divisor * quotient  # Ensure clean division

        templates = [
            {
                "question": "{name} has {dividend} {item_plural} to share equally among {divisor} {recipient_plural}. How many {item_plural} does each {recipient} get?",
                "theme_data": {
                    "name": "Sam",
                    "item": "cookie",
                    "item_plural": "cookies",
                    "recipient": "friend",
                    "recipient_plural": "friends"
                }
            },
            {
                "question": "There are {dividend} {item_plural} that need to be packed into {divisor} {container_plural}. If each {container} holds the same amount, how many {item_plural} go in each?",
                "theme_data": {
                    "item": "book",
                    "item_plural": "books",
                    "container": "box",
                    "container_plural": "boxes"
                }
            }
        ]

        template = random.choice(templates)
        question = template["question"].format(dividend=dividend, divisor=divisor, **template["theme_data"])

        return {
            "question": question,
            "answer": quotient,
            "solution": [
                f"We need to divide {dividend} by {divisor}",
                f"{dividend} ÷ {divisor} = {quotient}",
                f"Each one gets {quotient}"
            ],
            "theme_data": {**template["theme_data"], "dividend": dividend, "divisor": divisor}
        }

    def _gen_fractions(self, difficulty: str) -> Dict[str, Any]:
        # Generate fraction addition/comparison problems
        if difficulty == "easy":
            denominators = [2, 4]
        elif difficulty == "medium":
            denominators = [2, 3, 4, 5, 6]
        else:
            denominators = [2, 3, 4, 5, 6, 8, 10, 12]

        denom = random.choice(denominators)
        num1 = random.randint(1, denom - 1)
        num2 = random.randint(1, denom - num1)  # Ensure sum <= 1

        answer_num = num1 + num2

        if answer_num == denom:
            answer_str = "1"
            answer = 1
        elif answer_num % 2 == 0 and denom % 2 == 0:
            # Simplify
            simplified = Fraction(answer_num, denom)
            answer_str = f"{simplified.numerator}/{simplified.denominator}"
            answer = answer_str
        else:
            answer_str = f"{answer_num}/{denom}"
            answer = answer_str

        question = f"{num1}/{denom} + {num2}/{denom} = ?"

        return {
            "question": f"What is {num1}/{denom} + {num2}/{denom}? (Write your answer as a fraction like 3/4 or as a whole number)",
            "answer": answer_str,
            "solution": [
                f"Both fractions have the same denominator ({denom})",
                f"Add the numerators: {num1} + {num2} = {answer_num}",
                f"Keep the denominator: {answer_num}/{denom}",
                f"The answer is {answer_str}"
            ],
            "theme_data": {"num1": num1, "num2": num2, "denom": denom}
        }

    def _gen_decimals(self, difficulty: str) -> Dict[str, Any]:
        if difficulty == "easy":
            a = round(random.uniform(0.1, 5.0), 1)
            b = round(random.uniform(0.1, 5.0), 1)
        elif difficulty == "medium":
            a = round(random.uniform(1.0, 20.0), 2)
            b = round(random.uniform(1.0, 20.0), 2)
        else:
            a = round(random.uniform(10.0, 100.0), 2)
            b = round(random.uniform(10.0, 100.0), 2)

        operation = random.choice(["+", "-"])
        if operation == "-" and b > a:
            a, b = b, a

        answer = round(a + b, 2) if operation == "+" else round(a - b, 2)
        op_word = "add" if operation == "+" else "subtract"

        question = f"What is {a} {operation} {b}?"

        return {
            "question": question,
            "answer": answer,
            "solution": [
                f"Line up the decimal points",
                f"  {a:>8}",
                f"{operation} {b:>8}",
                f"= {answer:>8}",
                f"The answer is {answer}"
            ],
            "theme_data": {"a": a, "b": b, "operation": operation}
        }

    def _gen_percentages(self, difficulty: str) -> Dict[str, Any]:
        percentages = {
            "easy": [10, 25, 50],
            "medium": [10, 20, 25, 50, 75],
            "hard": [5, 10, 15, 20, 25, 30, 40, 50, 60, 75]
        }

        percent = random.choice(percentages.get(difficulty, percentages["easy"]))

        # Choose a number that gives a clean answer
        if percent == 10:
            total = random.choice([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        elif percent == 25:
            total = random.choice([4, 8, 12, 16, 20, 40, 80, 100])
        elif percent == 50:
            total = random.choice([2, 4, 6, 8, 10, 20, 40, 60, 80, 100])
        else:
            total = random.choice([20, 40, 60, 80, 100])

        answer = int(total * percent / 100)

        question = f"What is {percent}% of {total}?"

        return {
            "question": question,
            "answer": answer,
            "solution": [
                f"To find {percent}% of {total}:",
                f"Convert {percent}% to a decimal: {percent}/100 = {percent/100}",
                f"Multiply: {total} × {percent/100} = {answer}",
                f"The answer is {answer}"
            ],
            "theme_data": {"percent": percent, "total": total}
        }
