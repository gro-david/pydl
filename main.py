import click
from rich.console import Console
from rich.prompt import Prompt
import manage_playlist
import download_convert

tags = {
    'artist': None,
    'album': None,
    'title': None,
    'genre': None,
    'song_nr': None,
}

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

# this is the download command it gets the required inputs from the user and passes those on to the playlist management
# which calls the main function of the download_convert script. That downloads the song and converts it to mp3. 
@main.command()
@click.argument('input')
@click.option('--playlist/--no-playlist', help='Use this flag if you want to download the complete playlist', default=True)
@click.option('--tag/--no-tag', help='Use this flag if you want to disable automatic metadata fetching', default=True)
@click.option('-m', '--manual-tag', help='Set this to True if you want to manually set the metadata', default=False, is_flag=True)
def download(input, playlist, tag, manual_tag):
    # enable or disable metadata fetching
    download_convert.set_tagging(tag)
    if manual_tag:
        global tags

        tags['artist'] = Prompt.ask("Enter the [bold cyan]ARTIST[/bold cyan] name. [italic][Leave empty to skip][/italic]")
        tags['album'] =  Prompt.ask("Enter the [bold cyan]ALBUM[/bold cyan] name. [italic][Leave empty to skip][/italic]")
        tags['title'] = Prompt.ask("Enter the [bold cyan]TITLE[/bold cyan] of the song. [italic][Leave empty to skip][/italic]")
        tags['genre'] = Prompt.ask("Enter the [bold cyan]GENRE[/bold cyan] of the song. [italic][Leave empty to skip][/italic]")
        

        # loop over each value in the dictionary and add it to the topop list if empty
        topop=[]
        for key in tags.keys():
            if tags[key] == '':
                topop.append(key)

        # we only want to prompt the user if there is something to complete
        if len(topop) > 0:
            # ask the user until they deliver a valid input if that is the case we break out of the loop
            while True:
                complete = Prompt.ask('Should the empty fields be automatically filled in? [italic][Y/n][italic]')

                if complete.lower() == 'y' or complete == '':
                    for key in topop:
                        tags[key] = None
                    break
                
                elif complete.lower() == 'n':
                    # pop empty items
                    for key in topop:
                        tags.pop(key)
                    break  
                
                else:
                    console.print('Invalid input', style='bold red')

    # run the playlist management script which then downloads the song/songs
    manage_playlist.main(input, playlist, tags)
    
# this gets run every time we want to do something with the script
if(__name__ == "__main__"):
    main()


# todo: generate pydl.conf command
# todo: create a bash script that can be used to run the script from anywhere
# todo: enable path changing