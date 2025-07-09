import json


def extract_exercise_names():

    with open("free-exercise-db/dist/exercises.json", "r") as f:
        exercises = json.load(f)

    exercise_names = [e["name"] for e in exercises]
    output = f"""--- START OF exercise_name_index ---
This document contains the complete and official list of all available exercise names. This is the primary and ONLY source for validating an exercise name before using any tool or searching for details.

{"\n".join(exercise_names)}

--- END OF exercise_name_index ---"""

    with open("data/exercise_names.txt", "w") as f:
        f.write(output)

def extract_exercise_names_json():
    with open("data/json/exercises.json", "r") as f:
        exercises = json.load(f)

    with open("data/json/exercise_names.json", "w") as f:
        f.write("[\n")
        for e in exercises[:-1]:
            f.write(f"""\t{{"exercise_name": "{e["name"]}"}},\n""")
        f.write(f"""\t{{"exercise_name": "{e["name"]}"}}\n]""")


extract_exercise_names_json()