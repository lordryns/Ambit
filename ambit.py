import json
import os
import threading, socket

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



class Standard:
    def __init__(self, script: dict) -> None:
        self.script = script 

        self.handle_processes()
    def get_user_ip(self, command: str, _return: str):
        host_name = socket.gethostname()
        ip = socket.gethostbyname(host_name)

        try:
            
            if command == "get_ip":
                if _return  == "std":
                    print(ip)
                elif _return == "file":
                    with open("ip.txt", 'w') as fp:
                        fp.write(str(ip))
                        
                else:
                    print("Return type must either be STD or FILE.")

        except Exception as e:
            print(e)


    def get_device_name(self, command: str, _return: str):
        host_name = socket.gethostname()

        try:
            if command == "get_device_name":
                if _return  == "std":
                    print(host_name)
                elif _return == "file":
                    with open("ip.txt", 'w') as fp:
                        fp.write(str(host_name))
                        
                else:
                    print("Return type must either be STD or FILE.")

        except Exception as e:   
            print(e)

        
    def handle_processes(self):
        for script in self.script:
            command = script["$command"].lower()
            _return = script["return"].lower()

            
            self.get_device_name(command=command, _return=_return)
            self.get_user_ip(command=command, _return=_return)
    


def run_script():
    response = get_json_script()

    if response[1]:
        json_code = response[0]
        Standard(json_code)




def main():
    print('-'*15, end="")
    print("Ambit v 1.0", end="")
    print('-'*15)
    while True:
        command = input("~ ").lower().replace(" ", "")
        if command == 'exists':
            if get_json_script()[2] in (0, 2):
                print("True\n")
            else: print("False\n")
        
        elif command == 'run':
            run_script()
            print("\n")

        else: 
            print(f"{command} is not a valid command, use [help] to see the list of commands!")
            


if __name__ == '__main__':
    main()
