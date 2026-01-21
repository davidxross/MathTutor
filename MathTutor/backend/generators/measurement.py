import random
from typing import Dict, Any
from .base import BaseProblemGenerator

class MeasurementGenerator(BaseProblemGenerator):
    """Generator for measurement problems."""

    topic = "measurement"
    display_name = "Measurement"
    problem_types = ["perimeter", "area", "volume", "conversions", "time"]

    def __init__(self):
        super().__init__()
        self.difficulty_ranges = {
            "easy": {"min": 2, "max": 10},
            "medium": {"min": 5, "max": 25},
            "hard": {"min": 10, "max": 50}
        }

    def _generate_problem(self, difficulty: str, problem_type: str) -> Dict[str, Any]:
        generators = {
            "perimeter": self._gen_perimeter,
            "area": self._gen_area,
            "volume": self._gen_volume,
            "conversions": self._gen_conversions,
            "time": self._gen_time
        }
        return generators.get(problem_type, self._gen_perimeter)(difficulty)

    def _gen_perimeter(self, difficulty: str) -> Dict[str, Any]:
        min_val, max_val = self.get_range(difficulty)
        shape = random.choice(["rectangle", "square"])

        if shape == "square":
            side = random.randint(min_val, max_val)
            answer = 4 * side

            question = f"A square {'{location}'} has sides of {side} metres. What is its perimeter?"

            return {
                "question": question.format(location="garden"),
                "answer": answer,
                "solution": [
                    f"A square has 4 equal sides",
                    f"Perimeter = 4 × side length",
                    f"Perimeter = 4 × {side} = {answer} metres",
                    f"The perimeter is {answer} metres"
                ],
                "theme_data": {"location": "garden", "side": side, "shape": "square"}
            }
        else:
            length = random.randint(min_val, max_val)
            width = random.randint(min_val, max_val)
            answer = 2 * (length + width)

            question = f"A rectangular {'{location}'} is {length} metres long and {width} metres wide. What is its perimeter?"

            return {
                "question": question.format(location="playground"),
                "answer": answer,
                "solution": [
                    f"A rectangle has 2 pairs of equal sides",
                    f"Perimeter = 2 × (length + width)",
                    f"Perimeter = 2 × ({length} + {width})",
                    f"Perimeter = 2 × {length + width} = {answer} metres",
                    f"The perimeter is {answer} metres"
                ],
                "theme_data": {"location": "playground", "length": length, "width": width, "shape": "rectangle"}
            }

    def _gen_area(self, difficulty: str) -> Dict[str, Any]:
        min_val, max_val = self.get_range(difficulty)
        shape = random.choice(["rectangle", "square", "triangle"])

        if shape == "square":
            side = random.randint(min_val, max_val)
            answer = side * side

            return {
                "question": f"What is the area of a square with sides of {side} cm?",
                "answer": answer,
                "solution": [
                    f"Area of a square = side × side",
                    f"Area = {side} × {side}",
                    f"Area = {answer} cm²",
                    f"The area is {answer} square centimetres"
                ],
                "theme_data": {"side": side, "shape": "square"}
            }
        elif shape == "rectangle":
            length = random.randint(min_val, max_val)
            width = random.randint(min_val, max_val)
            answer = length * width

            return {
                "question": f"A rectangle is {length} cm long and {width} cm wide. What is its area?",
                "answer": answer,
                "solution": [
                    f"Area of a rectangle = length × width",
                    f"Area = {length} × {width}",
                    f"Area = {answer} cm²",
                    f"The area is {answer} square centimetres"
                ],
                "theme_data": {"length": length, "width": width, "shape": "rectangle"}
            }
        else:  # triangle
            base = random.randint(min_val, max_val) * 2  # Ensure even for clean division
            height = random.randint(min_val, max_val)
            answer = (base * height) // 2

            return {
                "question": f"A triangle has a base of {base} cm and a height of {height} cm. What is its area?",
                "answer": answer,
                "solution": [
                    f"Area of a triangle = (base × height) ÷ 2",
                    f"Area = ({base} × {height}) ÷ 2",
                    f"Area = {base * height} ÷ 2",
                    f"Area = {answer} cm²",
                    f"The area is {answer} square centimetres"
                ],
                "theme_data": {"base": base, "height": height, "shape": "triangle"}
            }

    def _gen_volume(self, difficulty: str) -> Dict[str, Any]:
        min_val, max_val = self.get_range(difficulty)

        # Simpler values for volume
        if difficulty == "easy":
            values = [2, 3, 4, 5]
        elif difficulty == "medium":
            values = [2, 3, 4, 5, 6, 8, 10]
        else:
            values = list(range(2, 15))

        shape = random.choice(["cube", "rectangular_prism"])

        if shape == "cube":
            side = random.choice(values)
            answer = side ** 3

            return {
                "question": f"What is the volume of a cube with sides of {side} cm?",
                "answer": answer,
                "solution": [
                    f"Volume of a cube = side × side × side",
                    f"Volume = {side} × {side} × {side}",
                    f"Volume = {side * side} × {side}",
                    f"Volume = {answer} cm³",
                    f"The volume is {answer} cubic centimetres"
                ],
                "theme_data": {"side": side, "shape": "cube"}
            }
        else:
            length = random.choice(values)
            width = random.choice(values)
            height = random.choice(values)
            answer = length * width * height

            return {
                "question": f"A box is {length} cm long, {width} cm wide, and {height} cm tall. What is its volume?",
                "answer": answer,
                "solution": [
                    f"Volume of a rectangular prism = length × width × height",
                    f"Volume = {length} × {width} × {height}",
                    f"Volume = {length * width} × {height}",
                    f"Volume = {answer} cm³",
                    f"The volume is {answer} cubic centimetres"
                ],
                "theme_data": {"length": length, "width": width, "height": height, "shape": "rectangular_prism"}
            }

    def _gen_conversions(self, difficulty: str) -> Dict[str, Any]:
        conversions = {
            "easy": [
                ("m", "cm", 100, [1, 2, 3, 4, 5]),
                ("km", "m", 1000, [1, 2, 3, 5]),
                ("kg", "g", 1000, [1, 2, 3, 5]),
                ("L", "mL", 1000, [1, 2, 3, 5])
            ],
            "medium": [
                ("m", "cm", 100, [2, 3, 5, 7, 10]),
                ("km", "m", 1000, [2, 4, 5, 10]),
                ("kg", "g", 1000, [2, 4, 5, 10]),
                ("L", "mL", 1000, [2, 4, 5]),
                ("cm", "m", 0.01, [100, 200, 500])
            ],
            "hard": [
                ("m", "cm", 100, [1.5, 2.5, 3.25]),
                ("km", "m", 1000, [1.5, 2.25]),
                ("kg", "g", 1000, [1.5, 2.5, 0.5]),
                ("cm", "m", 0.01, [150, 250, 375])
            ]
        }

        options = conversions.get(difficulty, conversions["easy"])
        from_unit, to_unit, factor, values = random.choice(options)
        value = random.choice(values)

        answer = value * factor if factor >= 1 else value * factor

        if isinstance(answer, float) and answer == int(answer):
            answer = int(answer)

        unit_names = {
            "m": "metres", "cm": "centimetres", "km": "kilometres",
            "kg": "kilograms", "g": "grams", "L": "litres", "mL": "millilitres"
        }

        return {
            "question": f"Convert {value} {from_unit} to {to_unit}.",
            "answer": answer,
            "solution": [
                f"1 {from_unit} = {factor if factor >= 1 else int(1/factor)} {to_unit}" if factor >= 1 else f"1 {from_unit} = {factor} {to_unit}",
                f"Multiply: {value} × {factor if factor >= 1 else factor}",
                f"{value} {from_unit} = {answer} {to_unit}"
            ],
            "theme_data": {"value": value, "from_unit": from_unit, "to_unit": to_unit}
        }

    def _gen_time(self, difficulty: str) -> Dict[str, Any]:
        problem_type = random.choice(["elapsed", "conversion"])

        if problem_type == "elapsed":
            if difficulty == "easy":
                start_hour = random.randint(8, 14)
                duration_minutes = random.choice([30, 60, 90, 120])
            elif difficulty == "medium":
                start_hour = random.randint(8, 14)
                duration_minutes = random.choice([45, 75, 95, 105])
            else:
                start_hour = random.randint(8, 12)
                duration_minutes = random.choice([115, 135, 165, 195])

            end_minutes = (0 + duration_minutes) % 60
            end_hour = start_hour + duration_minutes // 60

            end_time = f"{end_hour}:{end_minutes:02d}"
            start_time = f"{start_hour}:00"

            return {
                "question": f"A movie starts at {start_time} and lasts {duration_minutes} minutes. What time does it end? (Write in format like 2:30)",
                "answer": end_time,
                "solution": [
                    f"Start time: {start_time}",
                    f"Duration: {duration_minutes} minutes = {duration_minutes // 60} hour(s) and {duration_minutes % 60} minutes",
                    f"Add {duration_minutes // 60} hour(s) to {start_hour}:00 → {start_hour + duration_minutes // 60}:00",
                    f"Add {duration_minutes % 60} minutes → {end_time}",
                    f"The movie ends at {end_time}"
                ],
                "theme_data": {"start_time": start_time, "duration": duration_minutes}
            }
        else:  # conversion
            if difficulty == "easy":
                hours = random.randint(1, 5)
                answer = hours * 60
                question = f"How many minutes are in {hours} hour(s)?"
                solution = [f"1 hour = 60 minutes", f"{hours} hours = {hours} × 60 = {answer} minutes"]
            else:
                minutes = random.choice([60, 120, 180, 240, 300, 90, 150])
                answer = minutes // 60 if minutes % 60 == 0 else f"{minutes // 60} hours {minutes % 60} minutes"
                question = f"Convert {minutes} minutes to hours (and minutes if needed)."
                solution = [f"Divide by 60: {minutes} ÷ 60", f"= {minutes // 60} remainder {minutes % 60}", f"= {answer}"]

            return {
                "question": question,
                "answer": answer,
                "solution": solution,
                "theme_data": {}
            }
