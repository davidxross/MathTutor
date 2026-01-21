import random
from typing import Dict, Any, List
from .base import BaseProblemGenerator

class DataManagementGenerator(BaseProblemGenerator):
    """Generator for data management and probability problems."""

    topic = "data_management"
    display_name = "Data Management & Probability"
    problem_types = ["mean", "median", "mode", "range", "probability", "graphs"]

    def __init__(self):
        super().__init__()

    def _generate_problem(self, difficulty: str, problem_type: str) -> Dict[str, Any]:
        generators = {
            "mean": self._gen_mean,
            "median": self._gen_median,
            "mode": self._gen_mode,
            "range": self._gen_range,
            "probability": self._gen_probability,
            "graphs": self._gen_graphs
        }
        return generators.get(problem_type, self._gen_mean)(difficulty)

    def _gen_mean(self, difficulty: str) -> Dict[str, Any]:
        if difficulty == "easy":
            count = 3
            numbers = [random.randint(2, 10) for _ in range(count)]
            # Adjust last number to get clean mean
            target_sum = random.choice([9, 12, 15, 18, 21, 24]) # Divisible by 3
            numbers[-1] = target_sum - sum(numbers[:-1])
            if numbers[-1] < 1:
                numbers = [4, 5, 6]
        elif difficulty == "medium":
            count = 4
            numbers = [random.randint(5, 20) for _ in range(count)]
            target_sum = round(sum(numbers) / 4) * 4  # Make divisible by 4
            numbers[-1] += target_sum - sum(numbers)
        else:
            count = 5
            numbers = [random.randint(10, 50) for _ in range(count)]
            target_sum = round(sum(numbers) / 5) * 5
            numbers[-1] += target_sum - sum(numbers)

        answer = sum(numbers) // count
        numbers_str = ", ".join(map(str, sorted(numbers)))

        return {
            "question": f"Find the mean (average) of these numbers: {numbers_str}",
            "answer": answer,
            "solution": [
                f"The mean is the sum divided by the count",
                f"Sum: {' + '.join(map(str, numbers))} = {sum(numbers)}",
                f"Count: {count} numbers",
                f"Mean: {sum(numbers)} ÷ {count} = {answer}"
            ],
            "theme_data": {"numbers": numbers}
        }

    def _gen_median(self, difficulty: str) -> Dict[str, Any]:
        if difficulty == "easy":
            count = 5  # Odd number for easy median
            numbers = sorted([random.randint(1, 20) for _ in range(count)])
        elif difficulty == "medium":
            count = 7
            numbers = sorted([random.randint(5, 30) for _ in range(count)])
        else:
            count = 6  # Even number - need to average two middle values
            numbers = sorted([random.randint(10, 50) for _ in range(count)])
            # Adjust for clean median
            mid1, mid2 = count // 2 - 1, count // 2
            numbers[mid1] = random.randint(20, 30)
            numbers[mid2] = numbers[mid1] + random.choice([0, 2, 4, 6])
            numbers = sorted(numbers)

        if count % 2 == 1:
            answer = numbers[count // 2]
            median_explanation = f"The middle number is {answer}"
        else:
            mid1, mid2 = numbers[count // 2 - 1], numbers[count // 2]
            answer = (mid1 + mid2) / 2
            if answer == int(answer):
                answer = int(answer)
            median_explanation = f"Average of two middle numbers: ({mid1} + {mid2}) ÷ 2 = {answer}"

        numbers_str = ", ".join(map(str, numbers))

        return {
            "question": f"Find the median of these numbers: {numbers_str}",
            "answer": answer,
            "solution": [
                f"The median is the middle value when numbers are in order",
                f"Numbers in order: {numbers_str}",
                median_explanation,
                f"Median = {answer}"
            ],
            "theme_data": {"numbers": numbers}
        }

    def _gen_mode(self, difficulty: str) -> Dict[str, Any]:
        if difficulty == "easy":
            mode = random.randint(3, 10)
            count = random.randint(3, 4)
            numbers = [mode] * count
            # Add some other unique numbers
            for _ in range(2):
                n = random.randint(1, 15)
                if n != mode:
                    numbers.append(n)
        else:
            mode = random.randint(5, 20)
            count = random.randint(3, 5)
            numbers = [mode] * count
            for _ in range(4):
                n = random.randint(1, 25)
                if n != mode:
                    numbers.append(n)

        random.shuffle(numbers)
        numbers_str = ", ".join(map(str, numbers))

        return {
            "question": f"Find the mode of these numbers: {numbers_str}",
            "answer": mode,
            "solution": [
                f"The mode is the number that appears most often",
                f"Count each number:",
                f"  {mode} appears {count} times",
                f"  Other numbers appear less often",
                f"Mode = {mode}"
            ],
            "theme_data": {"numbers": numbers, "mode": mode}
        }

    def _gen_range(self, difficulty: str) -> Dict[str, Any]:
        if difficulty == "easy":
            min_val = random.randint(2, 10)
            max_val = min_val + random.randint(5, 15)
            numbers = [min_val, max_val] + [random.randint(min_val, max_val) for _ in range(3)]
        else:
            min_val = random.randint(10, 30)
            max_val = min_val + random.randint(15, 40)
            numbers = [min_val, max_val] + [random.randint(min_val, max_val) for _ in range(5)]

        random.shuffle(numbers)
        answer = max_val - min_val
        numbers_str = ", ".join(map(str, numbers))

        return {
            "question": f"Find the range of these numbers: {numbers_str}",
            "answer": answer,
            "solution": [
                f"The range is the difference between the largest and smallest values",
                f"Smallest: {min_val}",
                f"Largest: {max_val}",
                f"Range = {max_val} - {min_val} = {answer}"
            ],
            "theme_data": {"numbers": numbers}
        }

    def _gen_probability(self, difficulty: str) -> Dict[str, Any]:
        scenario_type = random.choice(["dice", "cards", "marbles", "spinner"])

        if scenario_type == "dice":
            # Probability with a standard die
            event_type = random.choice(["specific", "even", "greater"])
            if event_type == "specific":
                target = random.randint(1, 6)
                answer = "1/6"
                question = f"What is the probability of rolling a {target} on a standard die?"
                solution = [
                    f"A standard die has 6 faces numbered 1-6",
                    f"There is 1 way to roll a {target}",
                    f"Probability = favorable outcomes ÷ total outcomes",
                    f"Probability = 1/6"
                ]
            elif event_type == "even":
                answer = "1/2"
                question = "What is the probability of rolling an even number on a standard die?"
                solution = [
                    "A standard die has 6 faces",
                    "Even numbers are: 2, 4, 6 (3 numbers)",
                    "Probability = 3/6 = 1/2"
                ]
            else:  # greater than
                target = random.choice([2, 3, 4])
                favorable = 6 - target
                answer = f"{favorable}/6"
                question = f"What is the probability of rolling greater than {target} on a standard die?"
                solution = [
                    f"Numbers greater than {target}: {list(range(target+1, 7))}",
                    f"That's {favorable} numbers out of 6",
                    f"Probability = {favorable}/6"
                ]

        elif scenario_type == "marbles":
            if difficulty == "easy":
                total = random.choice([5, 10])
                red = random.choice([1, 2, 3])
            else:
                total = random.choice([8, 10, 12])
                red = random.randint(2, total // 2)

            # Simplify if possible
            from math import gcd
            g = gcd(red, total)
            simplified = f"{red//g}/{total//g}" if g > 1 else f"{red}/{total}"
            answer = simplified

            question = f"A bag contains {total} marbles: {red} red and {total - red} blue. What is the probability of picking a red marble?"
            solution = [
                f"Total marbles: {total}",
                f"Red marbles: {red}",
                f"Probability = {red}/{total}" + (f" = {simplified}" if g > 1 else "")
            ]

        elif scenario_type == "spinner":
            sections = random.choice([4, 6, 8])
            target_count = random.randint(1, sections // 2)

            from math import gcd
            g = gcd(target_count, sections)
            simplified = f"{target_count//g}/{sections//g}" if g > 1 else f"{target_count}/{sections}"
            answer = simplified

            question = f"A spinner has {sections} equal sections. {target_count} section(s) are colored green. What is the probability of landing on green?"
            solution = [
                f"Total sections: {sections}",
                f"Green sections: {target_count}",
                f"Probability = {target_count}/{sections}" + (f" = {simplified}" if g > 1 else "")
            ]

        else:  # cards
            question = "What is the probability of drawing a heart from a standard deck of 52 cards?"
            answer = "1/4"
            solution = [
                "A standard deck has 52 cards",
                "There are 13 hearts in a deck",
                "Probability = 13/52 = 1/4"
            ]

        return {
            "question": question,
            "answer": answer,
            "solution": solution,
            "theme_data": {"scenario": scenario_type}
        }

    def _gen_graphs(self, difficulty: str) -> Dict[str, Any]:
        # Bar graph / pictograph interpretation
        categories = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        context = random.choice(["books read", "goals scored", "apples picked", "laps run"])

        if difficulty == "easy":
            values = [random.randint(2, 10) for _ in range(5)]
        else:
            values = [random.randint(5, 25) for _ in range(5)]

        question_type = random.choice(["total", "difference", "most", "average"])

        if question_type == "total":
            answer = sum(values)
            question_text = f"What is the total number of {context} for the whole week?"
            solution = [
                f"Add all values:",
                f"{' + '.join(map(str, values))} = {answer}"
            ]
        elif question_type == "difference":
            max_day = categories[values.index(max(values))]
            min_day = categories[values.index(min(values))]
            answer = max(values) - min(values)
            question_text = f"What is the difference between the highest and lowest days?"
            solution = [
                f"Highest: {max_day} with {max(values)}",
                f"Lowest: {min_day} with {min(values)}",
                f"Difference: {max(values)} - {min(values)} = {answer}"
            ]
        elif question_type == "most":
            max_val = max(values)
            answer = categories[values.index(max_val)]
            question_text = f"On which day were the most {context}?"
            solution = [
                f"Looking at each day:",
                *[f"  {cat}: {val}" for cat, val in zip(categories, values)],
                f"The highest is {answer} with {max_val}"
            ]
        else:  # average
            avg = sum(values) // 5
            values = [v for v in values]  # Adjust for clean average
            values[-1] = (avg * 5) - sum(values[:-1])
            answer = avg
            question_text = f"What is the average number of {context} per day?"
            solution = [
                f"Total: {sum(values)}",
                f"Number of days: 5",
                f"Average: {sum(values)} ÷ 5 = {answer}"
            ]

        # Create text representation of bar graph
        graph_data = "\n".join([f"  {cat}: {val}" for cat, val in zip(categories, values)])
        full_question = f"Use the data showing {context} for each day:\n{graph_data}\n\n{question_text}"

        return {
            "question": full_question,
            "answer": answer,
            "solution": solution,
            "theme_data": {"categories": categories, "values": values, "context": context}
        }
