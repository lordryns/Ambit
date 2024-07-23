import json
import os
import threading

is_running = True

json_code = {}
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
            return json.load(fp), True, 0

    except IndexError as e:
        return "Unable to find a script.json file in this directory.", False, 1

    except json.JSONDecodeError as e:
        return "Invalid JSON format!", False, 2



def run_script():
    response = get_json_script()

    if response[1]:
        json_code = response[0]




def main():
    print('-'*15, end="")
    print("Ambit v 1.0", end="")
    print('-'*15)
    while True:
        command = input(">>").lower()
        if command == 'exists':
            if get_json_script()[2] in (0, 2):
                print("True\n")
            else: print("False\n")
        
        if command == 'run':
            run_script()


if __name__ == '__main__':
    main()
