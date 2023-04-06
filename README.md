# ydl - YouTube Downloader Project
### by Dávid Gro.
\
This is version 2 of my python YouTube Downloader. I didn't make v1 available because the code looked awful, the quality was low, and the download speed was slow.

This project currently only has a CLI (Command Line Interface), but a GUI (Graphical User Interface) is already in the works.

Functions: \
    - Download playlists easily with setting the tag `--playlist` or disable downloading playlists (and only download the current song) with the `--no-playlist` tag \
    - Fetch and apply metadata (mp3 tags) automatically with the `--tag` flag, or disable metadata fetching with the `--no-tag` flag. \
    - You can also manually set the metadata tags using the `-m` or `--manual-tag` flags.

Automatic fething is supported for following tags: \
    - Artist (Channel name formatted) \
    - Album (Name of the Playlist) \
    - Title (Name of the video/song) \
    - Song Number (Only when downloading a playlist) \
    - Album Cover (Thumbnail cropped to the middle square)

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
    - urllib (Downloadign the Thumbnail) \
    - mutagen (Setting the mp3 tags)
    - os (File management)


Example command could look like this: `ydl download {url} --tag --playlist -m`

Feel free to fork this project and modify it to make it work just the way you like it.

###### DISCLAIMER: This project is for entertainment purposes only.