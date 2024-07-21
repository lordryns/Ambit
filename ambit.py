import json
import os

is_running = True


def get_json_files() -> list['str']:
    current = os.getcwd()
    all_files = [f for f in os.listdir(current) if os.path.isfile(os.path.join(current, f))]
    json_files = [j for j in all_files if j.split(".")[-1] == "json"]

    return json_files


def get_json_script() -> tuple:
    try:
        script: str = [s for s in get_json_files() if s == "script.json"][0]
        with open(script, 'r') as fp:
            return json.load(fp), True

    except IndexError as e:
        return "Unable to find a script.json file in this directory.", False

    except json.JSONDecodeError as e:
        return "Invalid JSON format!", False


def display_outputs(script: dict):
    try:
        output = script["output"]
        for out in output:
            print(out)
    except:
        pass


def check_for_changes():
    response = get_json_script()
    if response[1]:
        json_code = response[0]
        display_outputs(json_code)

    else:
        print(f"An error occurred, error: {response[0]}")
