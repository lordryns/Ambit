import os
import click
import pyautogui as pg 
from stashdb import DB 
import json


class Compiler:
    def __init__(self, script_path) -> None:
        self.script_path = script_path
        self.format_script()
        self.run_script()
    
    def read_script(self) -> list | None:
        try:
            with open(self.script_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            click.secho(f"Error: Could not read script, [invalid syntax]. err: {str(e)}", fg="red")
            return None
        
    
    def format_script(self) -> None:
        script = self.read_script()
        if script is not None:
            with open(self.script_path, 'w') as f:
                json.dump(script, f, indent=4, sort_keys=True)

    
    def run_script(self) -> bool:
        script = self.read_script()
        if script is not None:
            for i in range(len(script)):
                block = script[i]
                if self.check_for_command(block):
                    self.check_for_move_command(block)
                else:
                   click.secho(f"Error: Each block must contain a command parameter, missing at block {i + 1}", fg="red")


    def check_for_move_command(self, block):
        if block["command"] == "move":
            if "params" in block:
                pass
            else:
                click.secho("Error: A params key is required.", fg="red")
    
    def check_for_command(self, block):
        if "command" in block:
            return True 
        else:
            return False
        
    



@click.command()
@click.argument("path", type=str)
def run(path):
    if path.split('.')[-1] == "json":
        if os.path.exists(path):
            compiler = Compiler(path)
        else:
            click.secho(f"Error: Path -> '{path}' does not exist.", fg="red")
    else:
        click.secho("Error: File must be of type json", fg='red')


@click.group()
def cli():
    """Ambit."""


cli.add_command(run)

if __name__ == "__main__":
    cli()