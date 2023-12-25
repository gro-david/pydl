# pydl - YouTube Downloader Project
## by Dávid Gro.
\
### Description
\
This is version 2 of my python YouTube Downloader. I didn't make v1 available because the code looked awful, the quality was low, and the download speed was slow.

This project currently only has a CLI (Command Line Interface), but a GUI (Graphical User Interface) is already in the works.

Functions: \
    - Download playlists easily with setting the tag `--playlist` or disable downloading playlists (and only download the current song) with the `--no-playlist` tag \
    - Fetch and apply metadata (mp3 tags) automatically with the `--tag` flag, or disable metadata fetching with the `--no-tag` flag. \
    - You can also manually set the metadata tags using the `-m` or `--manual-tag` flags.
    - You can enable experimental tagging (more advanced but sometimes slow) using the `--experimental` flag. The `--no-experimental` disables it. \
    - Save the files to a specific **relative** path using the `-p` or `--path` flag. \
    - Limit the amount of songs downloaded using the `-l` or `--limit` flag. \
    - Notification when download finishes

Commands: \
    - `download` downloads song/playlist \
    - `generate-config` generates the pydl.conf file

Automatic fetching is supported for following tags: \
    - Artist (Channel name formatted) \
    - Album (Name of the Playlist) \
    - Title (Name of the video/song) \
    - Song Number (Only when downloading a playlist) \
    - Album Cover (Thumbnail cropped to the middle square)

Experimental tagging supports following tags: \
    - Artist \
    - Album \
    - Title \
    - Genre

Manual Setting is supported for following tags: \
    - Artist \
    - Album \
    - Title \
    - Genre

This project was written entirely in python using following libraries: \
    - Click (CLI Library) \
    - Rich (Formatting CLI) \
    - pytube (Video downloading) \
    - ffmpeg-python (Converting audio track to mp3) \
    - Pillow (Cover Cropping) \
    - urllib (Downloading the Thumbnail) \
    - shazamio (Experimental tagging) \
    - mutagen (Setting the mp3 tags) \
    - os (File management) \
    - pyinstaller (File compilation)


Example command could look like this: `pydl download {url} --tag --playlist -m`

Feel free to fork this project and modify it to make it work just the way you like it.

Downloading top songs from any channel is currently not possible due to a glitch in the pytube library. I will add this function as soon as the problem is resolved from by the pytube developers.

Future functions: \
    - GUI \
    - Downloading top songs from a channel


### Installation Instructions:

Linux:
    - Download the latest Linux release from the releases page \
    - Extract the archive \
    - Open a terminal in the extracted folder \
    - Run the following command: `sudo ./linux-install.sh` \
    - You can now use the pydl command in your terminal \
\
Windows:
    - Download the latest Windows release from the releases page \
    - Extract the archive \
    - Open the command prompt as administrator \
    - Navigate to the extracted archive \ 
    - run the `./win-install.bat` command \
    - You can now use the pydl command in your terminal \

 Docs: \
    - `download`: Downloads a song or a playlist \
    - `generate-config`: Generates the pydl.conf file \
    - `pydl` (no arguments): Opens the pydl shell

###### DISCLAIMER: This project is for demonstration purposes only.
