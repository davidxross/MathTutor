import random
from typing import Dict, Any
from .base import BaseProblemGenerator

class GeometryGenerator(BaseProblemGenerator):
    """Generator for geometry problems."""

    topic = "geometry"
    display_name = "Geometry"
    problem_types = ["angles", "shapes_2d", "shapes_3d", "symmetry", "coordinates"]

    def __init__(self):
        super().__init__()

    def _generate_problem(self, difficulty: str, problem_type: str) -> Dict[str, Any]:
        generators = {
            "angles": self._gen_angles,
            "shapes_2d": self._gen_shapes_2d,
            "shapes_3d": self._gen_shapes_3d,
            "symmetry": self._gen_symmetry,
            "coordinates": self._gen_coordinates
        }
        return generators.get(problem_type, self._gen_angles)(difficulty)

    def _gen_angles(self, difficulty: str) -> Dict[str, Any]:
        problem_type = random.choice(["triangle", "straight_line", "identify"])

        if problem_type == "triangle":
            if difficulty == "easy":
                angle1 = random.choice([60, 70, 80, 90])
                angle2 = random.choice([30, 40, 50, 60])
            elif difficulty == "medium":
                angle1 = random.randint(35, 85)
                angle2 = random.randint(35, 85)
            else:
                angle1 = random.randint(20, 100)
                angle2 = random.randint(20, 140 - angle1)

            angle3 = 180 - angle1 - angle2

            return {
                "question": f"A triangle has two angles measuring {angle1}° and {angle2}°. What is the third angle?",
                "answer": angle3,
                "solution": [
                    f"The sum of angles in a triangle is 180°",
                    f"Third angle = 180° - {angle1}° - {angle2}°",
                    f"Third angle = 180° - {angle1 + angle2}°",
                    f"Third angle = {angle3}°"
                ],
                "theme_data": {"angle1": angle1, "angle2": angle2}
            }

        elif problem_type == "straight_line":
            if difficulty == "easy":
                angle1 = random.choice([30, 45, 60, 90, 120, 135, 150])
            else:
                angle1 = random.randint(15, 165)

            angle2 = 180 - angle1

            return {
                "question": f"Two angles on a straight line are supplementary. If one angle is {angle1}°, what is the other?",
                "answer": angle2,
                "solution": [
                    f"Angles on a straight line add up to 180°",
                    f"Other angle = 180° - {angle1}°",
                    f"Other angle = {angle2}°"
                ],
                "theme_data": {"angle1": angle1}
            }

        else:  # identify
            angle = random.choice([30, 45, 60, 90, 120, 135, 150, 180])
            if angle < 90:
                answer = "acute"
                description = "less than 90°"
            elif angle == 90:
                answer = "right"
                description = "exactly 90°"
            elif angle < 180:
                answer = "obtuse"
                description = "greater than 90° but less than 180°"
            else:
                answer = "straight"
                description = "exactly 180°"

            return {
                "question": f"What type of angle is {angle}°? (acute, right, obtuse, or straight)",
                "answer": answer,
                "solution": [
                    f"An angle of {angle}° is {description}",
                    f"This is called a{'n' if answer in ['acute', 'obtuse'] else ''} {answer} angle"
                ],
                "theme_data": {"angle": angle}
            }

    def _gen_shapes_2d(self, difficulty: str) -> Dict[str, Any]:
        shapes = {
            "triangle": {"sides": 3, "angles": 3},
            "quadrilateral": {"sides": 4, "angles": 4},
            "pentagon": {"sides": 5, "angles": 5},
            "hexagon": {"sides": 6, "angles": 6},
            "octagon": {"sides": 8, "angles": 8}
        }

        if difficulty == "easy":
            available = ["triangle", "quadrilateral"]
        elif difficulty == "medium":
            available = ["triangle", "quadrilateral", "pentagon", "hexagon"]
        else:
            available = list(shapes.keys())

        question_type = random.choice(["sides", "name", "angles_sum"])

        if question_type == "sides":
            shape = random.choice(available)
            answer = shapes[shape]["sides"]
            return {
                "question": f"How many sides does a {shape} have?",
                "answer": answer,
                "solution": [
                    f"A {shape} has {answer} sides"
                ],
                "theme_data": {"shape": shape}
            }
        elif question_type == "name":
            num_sides = random.choice([3, 4, 5, 6, 8])
            names = {3: "triangle", 4: "quadrilateral", 5: "pentagon", 6: "hexagon", 8: "octagon"}
            answer = names[num_sides]
            return {
                "question": f"What is a polygon with {num_sides} sides called?",
                "answer": answer,
                "solution": [
                    f"A polygon with {num_sides} sides is called a {answer}"
                ],
                "theme_data": {"num_sides": num_sides}
            }
        else:  # angles_sum
            shape = random.choice(available)
            num_sides = shapes[shape]["sides"]
            answer = (num_sides - 2) * 180
            return {
                "question": f"What is the sum of the interior angles in a {shape}?",
                "answer": answer,
                "solution": [
                    f"A {shape} has {num_sides} sides",
                    f"Sum of interior angles = (n - 2) × 180°",
                    f"Sum = ({num_sides} - 2) × 180°",
                    f"Sum = {num_sides - 2} × 180° = {answer}°"
                ],
                "theme_data": {"shape": shape, "num_sides": num_sides}
            }

    def _gen_shapes_3d(self, difficulty: str) -> Dict[str, Any]:
        shapes = {
            "cube": {"faces": 6, "edges": 12, "vertices": 8},
            "rectangular prism": {"faces": 6, "edges": 12, "vertices": 8},
            "triangular prism": {"faces": 5, "edges": 9, "vertices": 6},
            "square pyramid": {"faces": 5, "edges": 8, "vertices": 5},
            "triangular pyramid": {"faces": 4, "edges": 6, "vertices": 4},
            "cylinder": {"faces": 3, "edges": 2, "vertices": 0},
            "cone": {"faces": 2, "edges": 1, "vertices": 1},
            "sphere": {"faces": 1, "edges": 0, "vertices": 0}
        }

        if difficulty == "easy":
            available = ["cube", "rectangular prism", "sphere"]
        elif difficulty == "medium":
            available = ["cube", "rectangular prism", "triangular prism", "square pyramid", "cylinder"]
        else:
            available = list(shapes.keys())

        shape = random.choice(available)
        prop = random.choice(["faces", "edges", "vertices"])
        answer = shapes[shape][prop]

        return {
            "question": f"How many {prop} does a {shape} have?",
            "answer": answer,
            "solution": [
                f"A {shape} has:",
                f"  - {shapes[shape]['faces']} face(s)",
                f"  - {shapes[shape]['edges']} edge(s)",
                f"  - {shapes[shape]['vertices']} vertices",
                f"So it has {answer} {prop}"
            ],
            "theme_data": {"shape": shape, "property": prop}
        }

    def _gen_symmetry(self, difficulty: str) -> Dict[str, Any]:
        shapes = {
            "equilateral triangle": 3,
            "isosceles triangle": 1,
            "square": 4,
            "rectangle": 2,
            "regular pentagon": 5,
            "regular hexagon": 6,
            "circle": "infinite"
        }

        if difficulty == "easy":
            available = {"square": 4, "rectangle": 2, "equilateral triangle": 3}
        elif difficulty == "medium":
            available = {"square": 4, "rectangle": 2, "equilateral triangle": 3, "isosceles triangle": 1, "regular hexagon": 6}
        else:
            available = shapes

        shape = random.choice(list(available.keys()))
        answer = available[shape]

        return {
            "question": f"How many lines of symmetry does a {shape} have?",
            "answer": answer,
            "solution": [
                f"A {shape} has {answer} line(s) of symmetry",
                f"These are lines where you could fold the shape and both halves match exactly"
            ],
            "theme_data": {"shape": shape}
        }

    def _gen_coordinates(self, difficulty: str) -> Dict[str, Any]:
        if difficulty == "easy":
            max_coord = 5
        elif difficulty == "medium":
            max_coord = 10
        else:
            max_coord = 10  # Can include negatives

        problem_type = random.choice(["identify", "distance", "midpoint"])

        if problem_type == "identify":
            x = random.randint(0, max_coord)
            y = random.randint(0, max_coord)

            question_type = random.choice(["x", "y"])
            if question_type == "x":
                answer = x
                return {
                    "question": f"What is the x-coordinate of the point ({x}, {y})?",
                    "answer": answer,
                    "solution": [
                        f"In coordinates (x, y), the first number is x",
                        f"For point ({x}, {y}), x = {x}"
                    ],
                    "theme_data": {"x": x, "y": y}
                }
            else:
                answer = y
                return {
                    "question": f"What is the y-coordinate of the point ({x}, {y})?",
                    "answer": answer,
                    "solution": [
                        f"In coordinates (x, y), the second number is y",
                        f"For point ({x}, {y}), y = {y}"
                    ],
                    "theme_data": {"x": x, "y": y}
                }

        elif problem_type == "distance":
            # Keep it simple - horizontal or vertical distance
            if random.choice([True, False]):
                # Horizontal line
                y = random.randint(0, max_coord)
                x1 = random.randint(0, max_coord // 2)
                x2 = random.randint(max_coord // 2 + 1, max_coord)
                answer = x2 - x1
                return {
                    "question": f"What is the distance between points ({x1}, {y}) and ({x2}, {y})?",
                    "answer": answer,
                    "solution": [
                        f"Both points have the same y-coordinate ({y})",
                        f"Distance = difference in x-coordinates",
                        f"Distance = {x2} - {x1} = {answer}"
                    ],
                    "theme_data": {"x1": x1, "y1": y, "x2": x2, "y2": y}
                }
            else:
                # Vertical line
                x = random.randint(0, max_coord)
                y1 = random.randint(0, max_coord // 2)
                y2 = random.randint(max_coord // 2 + 1, max_coord)
                answer = y2 - y1
                return {
                    "question": f"What is the distance between points ({x}, {y1}) and ({x}, {y2})?",
                    "answer": answer,
                    "solution": [
                        f"Both points have the same x-coordinate ({x})",
                        f"Distance = difference in y-coordinates",
                        f"Distance = {y2} - {y1} = {answer}"
                    ],
                    "theme_data": {"x1": x, "y1": y1, "x2": x, "y2": y2}
                }

        else:  # midpoint (harder)
            x1 = random.randint(0, max_coord) * 2  # Even numbers for clean midpoint
            y1 = random.randint(0, max_coord) * 2
            x2 = random.randint(0, max_coord) * 2
            y2 = random.randint(0, max_coord) * 2

            mid_x = (x1 + x2) // 2
            mid_y = (y1 + y2) // 2
            answer = f"({mid_x}, {mid_y})"

            return {
                "question": f"What is the midpoint between ({x1}, {y1}) and ({x2}, {y2})? (Answer as: x, y)",
                "answer": f"{mid_x}, {mid_y}",
                "solution": [
                    f"Midpoint x = (x₁ + x₂) ÷ 2 = ({x1} + {x2}) ÷ 2 = {mid_x}",
                    f"Midpoint y = (y₁ + y₂) ÷ 2 = ({y1} + {y2}) ÷ 2 = {mid_y}",
                    f"Midpoint = ({mid_x}, {mid_y})"
                ],
                "theme_data": {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
            }
