import click
from rich.console import Console

console = Console()
# when running the script one function needs to be specified which gets run, when making a group of the commands you can have multiple commands in one script
@click.group()
def main():
    pass

# you can also have commands on the second level with the help of a sceond level group
@main.group()
def secondary():
    pass

# this command comes from the main group to run it you need to type the following: "python main.py command_one"
@main.command()
def command_one():
    console.print("command one", style="bold red")

# this command comes from the secondary group to run it you need to type the following: "python main.py secondary command_two"
@secondary.command()
def command_two():
    console.print("command two", style="bold green")

# this gets run every time we want to do something with the script
if(__name__ == "__main__"):
    main()