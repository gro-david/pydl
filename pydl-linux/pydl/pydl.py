# type: ignore
import os
import sys
import rich_click as rclick

# Rich modules for console styling
from rich.console import Console

# create a console object to use for styling
# this needs to be above the custom library imports, so taht they can reference this console object
console = Console()

# the module for the header
from pyfiglet import Figlet

# Custom modules
from libraries import manage_playlist
from libraries import download_convert
from libraries import read_conf
from libraries import generate_conf
from libraries import write_conf
from libraries import notifier
from libraries import manual_tagging
from libraries import queue_management
from libraries import rich_click_shell

# the config file is read and the values are stored in the conf dictionary
try:
    conf = read_conf.main()
except FileNotFoundError:
    console.print(
        "[bold red]Config file not found![/bold red] Starting config file generation..."
    )
    write_conf.main(generate_conf.main())
    sys.exit()
    
# different sections are seperated to make it easier to work withs
flags = conf["Flags"]
general = conf["General"]

# the empty tags dictionary will be filled with the metadata of the song if manual tagging is enabled
tags_in = {
    "artist": None,
    "album": None,
    "title": None,
    "genre": None,
    "song_nr": None,
}

# region configuring rich-click
# configuring the command sorting
rclick.rich_click.COMMAND_GROUPS = {
    "pydl.py": [
        {
            "name": "Universal Commands",
            "commands": ["download", "generate-config"],
        },
        {
            "name": "Shell Commands",
            "commands": [
                "queue-add",
                "queue-remove",
                "queue-start",
                "queue-clear",
                "queue-list",
                "clear",
            ],
        },
    ]
}
rclick.rich_click.STYLE_USAGE = "bold red"
rclick.rich_click.SHOW_ARGUMENTS = True
# for useage with rich attributes like [red]
rclick.rich_click.USE_RICH_MARKUP = True
# show the arguments in the help menu
rclick.rich_click.SHOW_ARGUMENTS = True
# endregion


# when running the script one function needs to be specified which gets run, when making a group of the commands you can have multiple commands in one script
@rclick.group(invoke_without_command=True)
@rclick.pass_context
def main(ctx):
    if ctx.invoked_subcommand is None:
        shell = rich_click_shell.make_click_shell(
            ctx,
            prompt="[bold cyan]pydl >> [/bold cyan]",
            intro=f"[bold red]{Figlet(font='doh').renderText('pydl')}[/bold red]",
        )
        shell.cmdloop()
    else:
        pass


# this command comes from the main group to run it you need to type the following: "python main.py command_one"
@main.command()
def generate_config():
    conf = generate_conf.main()
    write_conf.main(conf)


# region Download Command
# this is the download command it gets the required inputs from the user and passes those on to the playlist management
# which calls the main function of the download_convert script. That downloads the song and converts it to mp3.
# if the config file is wrong the script would throw an error. To avoid this we deliver our own error message and exit the script
try:

    @main.command()
    @rclick.argument("url")
    @rclick.option(
        "-p",
        "--path",
        help="The path where you want to save the song/songs",
        default="",
    )
    @rclick.option(
        "--playlist/--no-playlist",
        help="Use this flag if you want to download the complete playlist",
        default=flags["playlist"],
    )
    @rclick.option(
        "--tag/--no-tag",
        help="Use this flag if you want to disable automatic metadata fetching",
        default=flags["tag"],
    )
    @rclick.option(
        "--experimental/--no-experimental",
        help="Use this flag if you want to enable experimental tagging",
        default=flags["experimental"],
    )
    @rclick.option(
        "-m",
        "--manual-tag",
        help="Set this to True if you want to manually set the metadata",
        default=flags["manual-tag"],
        is_flag=True,
    )
    @rclick.option(
        "-l",
        "--limit",
        help="The amount of songs you want to download from the playlist",
        default=general["dl-limit"],
    )
    @rclick.option(
        "--tn/--no-tn",
        help="Use the thumbnail as the cover or not",
        default=flags["tn-as-cover"],
    )
    def download(url, path, playlist, tag, experimental, manual_tag, limit, tn):
        download_logic(url, path, playlist, tag, experimental, manual_tag, limit, tn)

except KeyError:
    console.print(
        "[bold red]Invalid config file![/bold red] Please generate a new config file!"
    )
# endregion


# this is the extracted download function
def download_logic(
    input,
    path="",
    playlist=flags["playlist"],
    tag=flags["tag"],
    experimental=flags["experimental"],
    manual_tag=flags["manual-tag"],
    limit=general["dl-limit"],
    tn=flags["tn-as-cover"],
    status=True,
):
    # we want the relative path, path out is the output path after modifications
    path_out = os.path.join(os.getcwd(), path)

    # we need to check if the path is valid
    if not os.path.isdir(path_out):
        console.print(
            "[bold red]Invalid path![/bold red] Please enter a valid path to a directory!"
        )
        quit()
    else:
        # if the path is valid, set the path in the download_convert script
        download_convert.set_path(path_out)

    # set the thumbnail as cover flag in the download_convert script
    download_convert.tn_as_cover = tn

    # run the manual tagging function if the manual tag flag is set to true we extracted this code to make it more readabledis
    if manual_tag:
        manual_tagging.main(tags_in)

    # if tagging and experimental tagging are both enabled, set the tagging to experimental
    if tag and experimental:
        download_convert.set_tagging("experimental")
    # if only tagging is enabled, set the tagging to normal
    elif tag:
        download_convert.set_tagging("normal")
    # if only experimental tagging is enabled, set the tagging to experimental
    elif experimental:
        download_convert.set_tagging("experimental")
    # if neither tagging nor experimental tagging are enabled, set the tagging to off
    else:
        download_convert.set_tagging("off")
    # set if we want a status message
    download_convert.set_status(status)
    # run the playlist management script which then downloads the song/songs. the title of the playlist will get saved
    pl_title = manage_playlist.main(input, playlist, tags_in, limit)

    # send a finished notification
    notifier.finished(pl_title)


@main.command(
    help="Queue only usable in the shell! Use 'pydl', without any arguments to enter the shell!"
)
@rclick.argument("url")
@rclick.option("-i", "--index")
@rclick.option("--playlist/--no-playlist", is_flag=True, default=flags["playlist"])
@rclick.option("-l", "--limit", default=general["dl-limit"])
@rclick.option("-p", "--path", default="")
def queue_add(url, index, playlist, limit, path):
    queue_management.add_to_queue(
        url=url, path=path, index=index, playlist=playlist, limit=limit
    )


@main.command(
    help="Queue only usable in the shell! Use 'pydl', without any arguments to enter the shell!"
)
def queue_list():
    queue_management.get_queue()


@main.command(
    help="Queue only usable in the shell! Use 'pydl', without any arguments to enter the shell!"
)
@rclick.argument("input")
def queue_remove(input):
    if input.isnumeric():
        index = int(input)
        queue_management.remove_from_queue(index)
    elif input.startswith("https://"):
        url = input
        queue_management.remove_from_queue(url=url)
    else:
        title = input
        queue_management.remove_from_queue(title=title)


@main.command(
    help="Queue only usable in the shell! Use 'pydl', without any arguments to enter the shell!"
)
def queue_start():
    queue_management.start_queue()


@main.command(
    help="Queue only usable in the shell! Use 'pydl', without any arguments to enter the shell!"
)
def queue_clear():
    queue_management.clear_queue()


@main.command(
    help="Clear the pydl shell. Use 'pydl', without any arguments to enter the shell!"
)
def clear():
    os.system("cls" if os.name == "nt" else "clear")


# this gets run every time we want to do something with the script
if __name__ == "__main__":
    main()
