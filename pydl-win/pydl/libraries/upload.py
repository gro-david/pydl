from ytmusicapi import YTMusic
import ytmusicapi
import platformdirs
import os
from libraries import read_conf, write_conf, generate_conf
import pydl
import sys
from rich.prompt import Prompt

# the directory where the oauth file should be saved
config_dir = platformdirs.user_config_dir(
    appname="pydl", appauthor="gro-david", ensure_exists=True
)
browser_path = os.path.join(config_dir, "browser.json")

try:
    ytmusic = YTMusic(browser_path) if read_conf.main()["Flags"]["upload"] else YTMusic()
except KeyError:
    pydl.console.print("[bold red]Invalid config file![bold red] Please generate a new one...")
    conf = generate_conf.main()
    write_conf.main(conf)
    sys.exit()
except FileNotFoundError:
    pydl.console.print("[bold red]The config file was not found![bold red] Please generate a new one...")
    conf = generate_conf.main()
    write_conf.main(conf)
    sys.exit()

def auth():
    headers = Prompt.ask(
        "[bold green]Please enter headers copied from the browser (Press Ctrl+D/Ctrl+Z to save):[/bold green] \n"
    )
    headers = ""
    try:
        while True:
            header = input()
            headers += "\n" + header
    except EOFError:
        pass
    ytmusicapi.setup(filepath=browser_path, headers_raw=headers)


def upload_dir(dirpath, recursive=True):
    # authentificate if it is not yet authentificated
    # if ytmusic.get_authorization(oauth_path) == None or authentificate:
    #    ytmusicapi.setup_oauth(oauth_path, open_browser=True)

    directories = [dirpath]
    for directory in directories:
        for file in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, file)):
                if recursive:
                    directories.append(os.path.join(directory, file))
                continue
            if not file.split(".")[-1] == "mp3":
                continue
            ytmusic = YTMusic(browser_path)
            ytmusic.upload_song(filepath=os.path.join(dirpath, file))


def upload_song(filepath):
    ytmusic.upload_song(filepath=filepath)


if __name__ == "__main__":
    upload_dir(
        "/mnt/docs/6 - David/python-projects/pydl-repo/pydl-linux/test",
    )
