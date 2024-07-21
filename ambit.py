import json
import os
import threading

is_running = True

variables = {}

# this finds anything with a .json extenuating in the current directory

def get_json_files() -> list['str']:
    current = os.getcwd()
    all_files = [f for f in os.listdir(current) if os.path.isfile(os.path.join(current, f))]
    json_files = [j for j in all_files if j.split(".")[-1] == "json"]

    return json_files


# this specifically finds a script.json file to work with
def get_json_script() -> tuple:
    try:
        script: str = [s for s in get_json_files() if s == "script.json"][0]
        with open(script, 'r') as fp:
            return json.load(fp), True

    except IndexError as e:
        return "Unable to find a script.json file in this directory.", False

    except json.JSONDecodeError as e:
        return "Invalid JSON format!", False


class Standard():
    def __init__(self, script: dict):
        self.script = script 

    def display_outputs(self):
        try:
            outputs = self.script["output"]
            for out in outputs:
                if str(out).startswith("$"):
                    variable = out.removeprefix("$")
                    if variable in variables:
                        print(variables[variable])

                else:
                    print(out)
        except Exception:
            pass


    def check_for_variables(self):
        global variables
        try:
            variables = self.script["variables"]
        except:
            pass

    


    def execute_on_stack(self):
        self.check_for_variables()
        self.display_outputs()

# this manages all the changes and should be called in a loop
def check_for_changes():
    response = get_json_script()
    if response[1]:
        json_code = response[0]
        standard = Standard(json_code)
        standard.execute_on_stack()
        
    else:
        print(f"An error occurred, error: {response[0]}")
