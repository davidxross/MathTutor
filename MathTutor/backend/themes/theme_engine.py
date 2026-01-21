import random
import re
from typing import Dict, Any

# Theme definitions with word substitutions
THEMES = {
    "classic": {
        "id": "classic",
        "name": "Classic",
        "description": "Standard textbook-style problems",
        "names": ["Alex", "Sam", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Quinn"],
        "substitutions": {}  # No substitutions for classic
    },
    "stranger_things": {
        "id": "stranger_things",
        "name": "Stranger Things",
        "description": "Problems set in Hawkins with Eleven, the Upside Down, and more",
        "names": ["Eleven", "Mike", "Dustin", "Lucas", "Will", "Max", "Nancy", "Steve", "Hopper"],
        "substitutions": {
            # Items
            "marble": "Eggo waffle",
            "marbles": "Eggo waffles",
            "cookie": "waffle",
            "cookies": "waffles",
            "apple": "Eggo",
            "apples": "Eggos",
            "book": "walkie-talkie",
            "books": "walkie-talkies",
            "toy": "D&D figurine",
            "toys": "D&D figurines",
            "sticker": "Hawkins badge",
            "stickers": "Hawkins badges",
            "candy": "Nougat",
            "candies": "Nougats",
            "pencil": "flashlight",
            "pencils": "flashlights",
            "ball": "Christmas light",
            "balls": "Christmas lights",
            "card": "alphabet letter",
            "cards": "alphabet letters",

            # Containers
            "box": "portal",
            "boxes": "portals",
            "basket": "Upside Down rift",
            "baskets": "Upside Down rifts",
            "bag": "backpack",
            "bags": "backpacks",
            "container": "secret hideout",
            "containers": "secret hideouts",

            # Locations
            "garden": "Hawkins Lab",
            "playground": "Starcourt Mall",
            "school": "Hawkins Middle School",
            "store": "Palace Arcade",
            "park": "the forest",
            "library": "the Byers' house",
            "pool": "Hawkins Pool",
            "field": "the Upside Down",

            # Groups
            "friend": "party member",
            "friends": "party members",
            "team": "squad",
            "teams": "squads",
            "group": "crew",
            "groups": "crews",
            "class": "Hawkins crew",
            "classes": "Hawkins crews",
            "student": "adventurer",
            "students": "adventurers",

            # Activities
            "game": "D&D campaign",
            "games": "D&D campaigns",
            "race": "escape from the Demogorgon",
            "races": "escapes from Demogorgons",
            "party": "adventure",
            "parties": "adventures",

            # Units in context
            "goals scored": "Demogorgons defeated",
            "laps run": "portals closed",
            "books read": "clues discovered",
            "apples picked": "Eggos collected"
        }
    },
    "puppy": {
        "id": "puppy",
        "name": "Puppy Paradise",
        "description": "Problems featuring adorable puppies, treats, and fun activities",
        "names": ["Buddy", "Max", "Charlie", "Cooper", "Rocky", "Bear", "Duke", "Tucker", "Luna", "Bella"],
        "substitutions": {
            # Items
            "marble": "dog treat",
            "marbles": "dog treats",
            "cookie": "biscuit",
            "cookies": "biscuits",
            "apple": "tennis ball",
            "apples": "tennis balls",
            "book": "chew toy",
            "books": "chew toys",
            "toy": "squeaky toy",
            "toys": "squeaky toys",
            "sticker": "paw print",
            "stickers": "paw prints",
            "candy": "treat",
            "candies": "treats",
            "pencil": "bone",
            "pencils": "bones",
            "ball": "tennis ball",
            "balls": "tennis balls",
            "card": "puppy photo",
            "cards": "puppy photos",

            # Containers
            "box": "dog bed",
            "boxes": "dog beds",
            "basket": "food bowl",
            "baskets": "food bowls",
            "bag": "treat bag",
            "bags": "treat bags",
            "container": "kennel",
            "containers": "kennels",

            # Locations
            "garden": "dog park",
            "playground": "puppy playground",
            "school": "obedience school",
            "store": "pet store",
            "park": "dog park",
            "library": "shelter",
            "pool": "splash pool",
            "field": "grassy yard",

            # Groups
            "friend": "puppy pal",
            "friends": "puppy pals",
            "team": "pack",
            "teams": "packs",
            "group": "litter",
            "groups": "litters",
            "class": "puppy class",
            "classes": "puppy classes",
            "student": "puppy trainee",
            "students": "puppy trainees",

            # Activities
            "game": "fetch session",
            "games": "fetch sessions",
            "race": "puppy race",
            "races": "puppy races",
            "party": "puppy playdate",
            "parties": "puppy playdates",

            # Units in context
            "goals scored": "treats earned",
            "laps run": "laps around the park",
            "books read": "tricks learned",
            "apples picked": "balls fetched"
        }
    }
}


class ThemeEngine:
    """Engine for applying themes to math problems."""

    def __init__(self, theme_id: str = "classic"):
        self.theme = THEMES.get(theme_id, THEMES["classic"])

    @staticmethod
    def get_all_themes():
        """Get list of all available themes."""
        return [
            {"id": t["id"], "name": t["name"], "description": t["description"]}
            for t in THEMES.values()
        ]

    def apply_theme(self, problem: Dict[str, Any]) -> Dict[str, Any]:
        """Apply the current theme to a problem."""
        themed_problem = problem.copy()

        # Apply name substitution
        question = themed_problem["question"]
        solution = themed_problem.get("solution", [])

        # Replace generic names with themed names
        name = random.choice(self.theme["names"])

        # Replace placeholder names or existing generic names
        generic_names = ["Alex", "Sam", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Quinn", "Sarah", "John"]
        for generic in generic_names:
            if generic in question:
                question = question.replace(generic, name, 1)
                break

        # Apply word substitutions
        for original, replacement in self.theme["substitutions"].items():
            # Case-insensitive replacement while preserving case
            pattern = re.compile(re.escape(original), re.IGNORECASE)
            question = pattern.sub(replacement, question)

            # Also apply to solution steps
            solution = [pattern.sub(replacement, step) for step in solution]

        themed_problem["question"] = question
        themed_problem["solution"] = solution
        themed_problem["theme"] = self.theme["id"]
        themed_problem["theme_name"] = self.theme["name"]

        return themed_problem

    def set_theme(self, theme_id: str):
        """Change the current theme."""
        self.theme = THEMES.get(theme_id, THEMES["classic"])
