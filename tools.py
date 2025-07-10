import json
import difflib
from pathlib import Path
from agno.tools import tool


with open("data/json/exercise_names.json") as f:
    exercises_data = json.load(f)

EXERCISE_NAMES = [e["exercise_name"] for e in exercises_data]


@tool(show_result=True)
def get_exercise_image(exercise_name: str) -> dict:
    """
    Searches for and retrieves image file paths for a given exercise name.

    The tool first attempts to find an exact match for the provided exercise
    name. If a corresponding directory with images is found, it returns the
    paths to those images.

    If no exact match is found, the tool performs a fuzzy search to identify
    up to 10 exercises with similar names. If any are found, it returns a
    list of these similarly named exercises along with their respective image paths.

    Args:
        exercise_name (str): The name of the exercise to search for, e.g., "Barbell Curl".

    Returns:
        A dictionary describing the outcome of the search. The structure of the
        dictionary varies based on the search result.

        - Case 1: An exact match is found.
          The 'exact_match' key is True, and 'images' contains the file paths.
          {
              "images": ["path/to/image1.jpg", "path/to/image2.jpg"],
              "exact_match": True,
              "similar_exercises": None
          }

        - Case 2: No exact match is found, but similar exercises are available.
          The 'exact_match' key is False, and 'similar_exercises' contains a
          list of potential matches.
          {
              "images": None,
              "exact_match": False,
              "similar_exercises": [
                  {"exercise_name": "Dumbbell Bicep Curl", "images": ["path/to/img_a.jpg"]},
                  {"exercise_name": "Preacher Curl", "images": ["path/to/img_b.jpg"]}
              ]
          }

        - Case 3: No exact or similar matches are found.
          The 'exact_match' key is False, and 'similar_exercises' is an empty list.
          {
              "images": None,
              "exact_match": False,
              "similar_exercises": []
          }
    """
    dir_path = Path(f"free-exercise-db/exercises/{exercise_name.replace(' ', '_')}")

    if dir_path.exists():
        images = [str(file) for file in dir_path.iterdir() if file.is_file()]
        print("Exists")
        return {"images": images, "exact_match": True, "similar_exercises": None}

    similar_names = difflib.get_close_matches(exercise_name, EXERCISE_NAMES, n=10, cutoff=0.6)

    similar_exercises = []
    for name in similar_names:
        alt_dir_path = Path(f"free-exercise-db/exercises/{name.replace(' ', '_')}")
        if alt_dir_path.exists():
            images = [str(file) for file in alt_dir_path.iterdir() if file.is_file()]
            similar_exercises.append({"exercise_name": name, "images": images})

    print("Similar" if similar_exercises else "Nop")
    return {"images": None, "exact_match": False, "similar_exercises": similar_exercises}


@tool(show_result=True)
def get_exercise_image___OLD(exercise_name: str) -> list:
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


