import random
from typing import Dict, Any, List
from .base import BaseProblemGenerator

class PatterningGenerator(BaseProblemGenerator):
    """Generator for patterning and algebra problems."""

    topic = "patterning"
    display_name = "Patterning & Algebra"
    problem_types = ["number_patterns", "equations", "variables", "growing_patterns", "input_output"]

    def __init__(self):
        super().__init__()

    def _generate_problem(self, difficulty: str, problem_type: str) -> Dict[str, Any]:
        generators = {
            "number_patterns": self._gen_number_patterns,
            "equations": self._gen_equations,
            "variables": self._gen_variables,
            "growing_patterns": self._gen_growing_patterns,
            "input_output": self._gen_input_output
        }
        return generators.get(problem_type, self._gen_number_patterns)(difficulty)

    def _gen_number_patterns(self, difficulty: str) -> Dict[str, Any]:
        pattern_type = random.choice(["arithmetic", "multiply", "square"])

        if pattern_type == "arithmetic":
            if difficulty == "easy":
                start = random.randint(1, 10)
                step = random.choice([2, 3, 5, 10])
            elif difficulty == "medium":
                start = random.randint(1, 20)
                step = random.choice([3, 4, 6, 7, 9, 11])
            else:
                start = random.randint(10, 50)
                step = random.choice([7, 8, 9, 11, 12, 13, 15])

            sequence = [start + step * i for i in range(5)]
            answer = sequence[4]
            displayed = sequence[:4]

            return {
                "question": f"What is the next number in the pattern: {', '.join(map(str, displayed))}, ?",
                "answer": answer,
                "solution": [
                    f"Find the difference between consecutive numbers:",
                    f"{displayed[1]} - {displayed[0]} = {step}",
                    f"The pattern increases by {step} each time",
                    f"Next number: {displayed[3]} + {step} = {answer}"
                ],
                "theme_data": {"sequence": displayed, "step": step}
            }

        elif pattern_type == "multiply":
            start = random.choice([2, 3])
            multiplier = random.choice([2, 3])
            sequence = [start * (multiplier ** i) for i in range(5)]
            answer = sequence[4]
            displayed = sequence[:4]

            return {
                "question": f"What is the next number in the pattern: {', '.join(map(str, displayed))}, ?",
                "answer": answer,
                "solution": [
                    f"Look at the relationship between consecutive numbers:",
                    f"{displayed[1]} ÷ {displayed[0]} = {multiplier}",
                    f"Each number is multiplied by {multiplier}",
                    f"Next number: {displayed[3]} × {multiplier} = {answer}"
                ],
                "theme_data": {"sequence": displayed, "multiplier": multiplier}
            }

        else:  # square numbers
            start = random.randint(1, 3)
            sequence = [(start + i) ** 2 for i in range(5)]
            answer = sequence[4]
            displayed = sequence[:4]

            return {
                "question": f"What is the next number in the pattern: {', '.join(map(str, displayed))}, ?",
                "answer": answer,
                "solution": [
                    f"These are square numbers:",
                    f"{displayed[0]} = {start}² = {start}×{start}",
                    f"{displayed[1]} = {start+1}² = {start+1}×{start+1}",
                    f"The pattern is consecutive square numbers",
                    f"Next: {start+4}² = {answer}"
                ],
                "theme_data": {"sequence": displayed, "start": start}
            }

    def _gen_equations(self, difficulty: str) -> Dict[str, Any]:
        if difficulty == "easy":
            # x + a = b
            a = random.randint(2, 10)
            answer = random.randint(1, 10)
            b = a + answer
            equation = f"x + {a} = {b}"
            solution_steps = [
                f"To find x, subtract {a} from both sides",
                f"x = {b} - {a}",
                f"x = {answer}"
            ]
        elif difficulty == "medium":
            op = random.choice(["add", "subtract", "multiply"])
            if op == "add":
                a = random.randint(5, 20)
                answer = random.randint(5, 20)
                b = a + answer
                equation = f"x + {a} = {b}"
                solution_steps = [
                    f"Subtract {a} from both sides",
                    f"x = {b} - {a}",
                    f"x = {answer}"
                ]
            elif op == "subtract":
                answer = random.randint(5, 20)
                a = random.randint(5, 15)
                b = answer - a
                equation = f"x - {a} = {b}"
                solution_steps = [
                    f"Add {a} to both sides",
                    f"x = {b} + {a}",
                    f"x = {answer}"
                ]
            else:  # multiply
                answer = random.randint(2, 10)
                a = random.choice([2, 3, 4, 5])
                b = a * answer
                equation = f"{a}x = {b}"
                solution_steps = [
                    f"Divide both sides by {a}",
                    f"x = {b} ÷ {a}",
                    f"x = {answer}"
                ]
        else:  # hard
            # Two-step equations: ax + b = c
            a = random.choice([2, 3, 4, 5])
            answer = random.randint(3, 10)
            b = random.randint(2, 10)
            c = a * answer + b
            equation = f"{a}x + {b} = {c}"
            solution_steps = [
                f"Step 1: Subtract {b} from both sides",
                f"{a}x = {c} - {b} = {c - b}",
                f"Step 2: Divide both sides by {a}",
                f"x = {c - b} ÷ {a}",
                f"x = {answer}"
            ]

        return {
            "question": f"Solve for x: {equation}",
            "answer": answer,
            "solution": solution_steps,
            "theme_data": {"equation": equation}
        }

    def _gen_variables(self, difficulty: str) -> Dict[str, Any]:
        """Evaluate expressions with given variable values."""
        if difficulty == "easy":
            n = random.randint(2, 10)
            a = random.choice([2, 3, 4, 5])
            answer = a * n
            return {
                "question": f"If n = {n}, what is the value of {a}n?",
                "answer": answer,
                "solution": [
                    f"{a}n means {a} × n",
                    f"{a} × {n} = {answer}"
                ],
                "theme_data": {"n": n, "a": a}
            }
        elif difficulty == "medium":
            x = random.randint(2, 8)
            a = random.choice([2, 3, 4])
            b = random.randint(1, 10)
            answer = a * x + b
            return {
                "question": f"If x = {x}, what is the value of {a}x + {b}?",
                "answer": answer,
                "solution": [
                    f"Substitute x = {x} into {a}x + {b}",
                    f"= {a} × {x} + {b}",
                    f"= {a * x} + {b}",
                    f"= {answer}"
                ],
                "theme_data": {"x": x, "a": a, "b": b}
            }
        else:
            x = random.randint(2, 5)
            y = random.randint(2, 5)
            a = random.choice([2, 3])
            b = random.choice([2, 3])
            answer = a * x + b * y
            return {
                "question": f"If x = {x} and y = {y}, what is the value of {a}x + {b}y?",
                "answer": answer,
                "solution": [
                    f"Substitute x = {x} and y = {y}",
                    f"= {a} × {x} + {b} × {y}",
                    f"= {a * x} + {b * y}",
                    f"= {answer}"
                ],
                "theme_data": {"x": x, "y": y, "a": a, "b": b}
            }

    def _gen_growing_patterns(self, difficulty: str) -> Dict[str, Any]:
        """Visual/numerical growing patterns."""
        if difficulty == "easy":
            start = random.randint(1, 5)
            growth = random.choice([1, 2, 3])
            term_number = random.randint(4, 6)
        elif difficulty == "medium":
            start = random.randint(2, 10)
            growth = random.choice([2, 3, 4, 5])
            term_number = random.randint(5, 8)
        else:
            start = random.randint(3, 10)
            growth = random.choice([3, 4, 5, 6])
            term_number = random.randint(8, 12)

        # Show first 3 terms
        terms = [start + growth * i for i in range(3)]
        answer = start + growth * (term_number - 1)

        ordinal = lambda n: str(n) + ("th" if 11 <= n <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))

        return {
            "question": f"In the pattern {terms[0]}, {terms[1]}, {terms[2]}, ..., what is the {ordinal(term_number)} term?",
            "answer": answer,
            "solution": [
                f"Find the pattern rule:",
                f"Starting value: {start}",
                f"Each term increases by: {growth}",
                f"Rule: Start at {start}, add {growth} each time",
                f"{ordinal(term_number)} term = {start} + ({term_number} - 1) × {growth}",
                f"= {start} + {term_number - 1} × {growth}",
                f"= {start} + {(term_number - 1) * growth}",
                f"= {answer}"
            ],
            "theme_data": {"start": start, "growth": growth, "terms": terms}
        }

    def _gen_input_output(self, difficulty: str) -> Dict[str, Any]:
        """Input/output machine problems."""
        if difficulty == "easy":
            # Simple operation: add or multiply
            operation = random.choice(["add", "multiply"])
            if operation == "add":
                constant = random.randint(2, 10)
                inputs = [random.randint(1, 10) for _ in range(3)]
                outputs = [i + constant for i in inputs]
                test_input = random.randint(1, 15)
                answer = test_input + constant
                rule = f"add {constant}"
            else:
                constant = random.choice([2, 3, 4, 5])
                inputs = [random.randint(1, 5) for _ in range(3)]
                outputs = [i * constant for i in inputs]
                test_input = random.randint(1, 10)
                answer = test_input * constant
                rule = f"multiply by {constant}"
        else:
            # Two operations: multiply then add
            multiplier = random.choice([2, 3])
            addend = random.randint(1, 5)
            inputs = [random.randint(1, 5) for _ in range(3)]
            outputs = [i * multiplier + addend for i in inputs]
            test_input = random.randint(1, 10)
            answer = test_input * multiplier + addend
            rule = f"multiply by {multiplier}, then add {addend}"

        table = "\n".join([f"  Input: {i} → Output: {o}" for i, o in zip(inputs, outputs)])

        return {
            "question": f"Study this input-output table:\n{table}\n\nWhat is the output when the input is {test_input}?",
            "answer": answer,
            "solution": [
                f"Find the rule by looking at the pattern:",
                f"The rule is: {rule}",
                f"For input {test_input}:",
                f"Output = {answer}"
            ],
            "theme_data": {"inputs": inputs, "outputs": outputs, "test_input": test_input}
        }
