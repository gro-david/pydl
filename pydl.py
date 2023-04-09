import os
import click

# Rich modules for console styling
from rich.console import Console
from rich.prompt import Prompt

# Custom modules
import manage_playlist
import download_convert
import read_conf
import generate_conf
import write_conf

# the config file is read and the values are stored in the conf dictionary
conf = read_conf.main()

# different sections are seperated to make it easier to work withs
flags = conf['Flags']
general = conf['General']

# the empty tags dictionary will be filled with the metadata of the song if manual tagging is enabled
tags_in = {
    'artist': None,
    'album': None,
    'title': None,
    'genre': None,
    'song_nr': None,
}

# create a console object to use for styling
console = Console()

# when running the script one function needs to be specified which gets run, when making a group of the commands you can have multiple commands in one script
@click.group()
def main():
    pass

# this command comes from the main group to run it you need to type the following: "python main.py command_one"
@main.command()
def generate_config():
    conf = generate_conf.main()
    write_conf.main(conf)

# this is the download command it gets the required inputs from the user and passes those on to the playlist management
# which calls the main function of the download_convert script. That downloads the song and converts it to mp3.
# if the config file is wrong the script would throw an error. To avoid this we deliver our own error message and exit the script
try:
    @main.command()
    @click.argument('input')
    @click.option('-p', '--path', help='The path where you want to save the song/songs', default='')
    @click.option('--playlist/--no-playlist', help='Use this flag if you want to download the complete playlist', default=flags['playlist'])
    @click.option('--tag/--no-tag', help='Use this flag if you want to disable automatic metadata fetching', default=flags['tag'])
    @click.option('--experimental/--no-experimental', help='Use this flag if you want to enable experimental tagging', default=flags['experimental'])
    @click.option('-m', '--manual-tag', help='Set this to True if you want to manually set the metadata', default=flags['manual-tag'], is_flag=True)
    @click.option('-l', '--limit', help='The amount of songs you want to download from the playlist', default=general['dl-limit'])
    def download(input, path, playlist, tag, experimental, manual_tag, limit):
        # this was added so there is a free line between the command and the status
        click.echo('\n')
        
        # we want the relative path, path out is the output path after modifications
        path_out = os.path.join(os.getcwd(), path)

        # we need to check if the path is valid
        if not os.path.isdir(path_out):
            console.print('[bold red]Invalid path![/bold red] Please enter a valid path to a directory!')
            quit()
        else:
            # if the path is valid, set the path in the download_convert script
            download_convert.set_path(path_out)

        # run the manual tagging function if the manual tag flag is set to true we extracted this code to make it more readabledis
        if manual_tag:
            manual_tagging()

        # if tagging and experimental tagging are both enabled, set the tagging to experimental
        if tag and experimental:
            download_convert.set_tagging('experimental')
        # if only tagging is enabled, set the tagging to normal
        elif tag:
            download_convert.set_tagging('normal')
        # if only experimental tagging is enabled, set the tagging to experimental
        elif experimental:
            download_convert.set_tagging('experimental')
        # if neither tagging nor experimental tagging are enabled, set the tagging to off
        else:
            download_convert.set_tagging('off')


        # run the playlist management script which then downloads the song/songs
        manage_playlist.main(input, playlist, tags_in, limit)
except KeyError:
    console.print('[bold red]Invalid config file![/bold red] Please generate a new config file!')

def manual_tagging():
    global tags_in

    tags_in['artist'] = Prompt.ask("Enter the [bold cyan]ARTIST[/bold cyan] name. [italic][Leave empty to skip][/italic]")
    tags_in['album'] =  Prompt.ask("Enter the [bold cyan]ALBUM[/bold cyan] name. [italic][Leave empty to skip][/italic]")
    tags_in['title'] = Prompt.ask("Enter the [bold cyan]TITLE[/bold cyan] of the song. [italic][Leave empty to skip][/italic]")
    tags_in['genre'] = Prompt.ask("Enter the [bold cyan]GENRE[/bold cyan] of the song. [italic][Leave empty to skip][/italic]")
    

    # loop over each value in the dictionary and add it to the topop list if empty
    topop=[]
    for key in tags_in.keys():
        if tags_in[key] == '':
            topop.append(key)

    # we only want to prompt the user if there is something to complete
    if len(topop) > 0:
        # ask the user until they deliver a valid input if that is the case we break out of the loop
        while True:
            complete = Prompt.ask('Should the empty fields be automatically filled in? [italic][Y/n][italic]')

            if complete.lower() == 'y' or complete == '':
                for key in topop:
                    tags_in[key] = None
                break
            
            elif complete.lower() == 'n':
                # pop empty items
                for key in topop:
                    tags_in.pop(key)
                break  
            
            else:
                console.print('Invalid input', style='bold red')

# this gets run every time we want to do something with the script
if(__name__ == "__main__"):
    main()