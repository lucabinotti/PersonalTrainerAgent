import json
import difflib
from pathlib import Path
from agno.tools import tool


with open("data/json/exercise_names.json") as f:
    exercises_data = json.load(f)

EXERCISE_NAMES = [e["exercise_name"] for e in exercises_data]


@tool(show_result=True)
def get_exercise_image_____NEW(exercise_name: str) -> dict:
    """
    Find images for an exercise. If no exact directory match is found, suggest the most similar exercise name.
    Returns a dictionary with:
        - images: list of image file paths
        - used_suggestion: True if a similar exercise name was used instead of the exact one
        - suggested_name: the name of the suggested exercise or None
    """
    dir_path = Path(f"free-exercise-db/exercises/{exercise_name.replace(' ', '_')}")

    if dir_path.exists():
        images = [str(file) for file in dir_path.iterdir() if file.is_file()]
        print("Exists")
        return {"images": images, "used_suggestion": False, "suggested_name": None}

    similar_names = difflib.get_close_matches(exercise_name, EXERCISE_NAMES, n=3, cutoff=0.6)

    for name in similar_names:
        alt_dir_path = Path(f"free-exercise-db/exercises/{name.replace(' ', '_')}")
        if alt_dir_path.exists():
            images = [str(file) for file in alt_dir_path.iterdir() if file.is_file()]
            print("Similar")
            return {"images": images, "used_suggestion": True, "suggested_name": name}

    print("Nop")
    return {"images": [], "used_suggestion": False, "suggested_name": None}


@tool(show_result=True)
def get_exercise_image(exercise_name: str) -> list:
    """
    Use this tool when there you think it is useful for the user to see pictures of
    particulars exercises. Call this tool passing as the exercise name the proper
    name specified in the JSON file that you can access as resource.
    """

    dir_path: Path = Path(rf"free-exercise-db/exercises/{exercise_name.replace(" ", "_")}")

    if dir_path.exists():
        print(f"Exists.")
        return [str(file) for file in dir_path.iterdir() if file.is_file()]
    print(f"Nop.")
    return []


