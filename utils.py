import json


def extract_exercise_names_json():
    """
    For generating the json file that contains all exercise names.
    """

    with open("data/json/exercises.json", "r") as f:
        exercises = json.load(f)

    with open("data/json/exercise_names.json", "w") as f:
        f.write("[\n")
        for e in exercises[:-1]:
            f.write(f"""\t{{"exercise_name": "{e["name"]}"}},\n""")
        f.write(f"""\t{{"exercise_name": "{e["name"]}"}}\n]""")


extract_exercise_names_json()