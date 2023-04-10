import ffmpeg
import os

# rich
from rich.prompt import Confirm
from rich.console import Console

# pytube
import pytube as pyt
from pytube import YouTube as YT
from pytube import Channel as CH
from pytube.exceptions import PytubeError

# Custom modules
import setmetadata
import get_thumbnail
import crop_image
import get_metadata
import notifier

tn_as_cover = None

# create a console object to use for styling
console = Console()

# 3 options for tagging: normal, experimental, off
tagging = 'normal'

# the path where the songs are downloaded to
dl_path = os.getcwd()

def download(url):
    yt=pyt.YouTube(url)
    stream=yt.streams.filter(only_audio=True)
    song=yt.streams.filter(only_audio=True)[-1].download(output_path=dl_path)
    return song

def convert(song, title):
    # set the new filename with the mp3 extension
    filename=song.split('.')[0]+'.mp3'

    # if we would not check this ffmpeg would hast ot itself. That would mess up the status
    if os.path.isfile(filename):
        # send a notification to the user that input is required
        notifier.error(title)
        if Confirm.ask(f"[bold red]File {filename} already exists, overwrite?[/bold red]"):
            os.remove(filename)
            with console.status(f"[bold green]Converting {title}...[/bold green]", spinner="dots"):
                # add the parameters to the ffmpeg command
                stream = ffmpeg.output(ffmpeg.input(song), filename, loglevel="quiet")

                # perform the conversion
                ffmpeg.run(stream)
        else:
            console.print(f"[bold red]Skipping {title}...[/bold red]")
    else:
        with console.status(f"[bold green]Converting {title}...[/bold green]", spinner="dots"):
                # add the parameters to the ffmpeg command
                stream = ffmpeg.output(ffmpeg.input(song), filename, loglevel="quiet")

                # perform the conversion
                ffmpeg.run(stream)
                
    # return the new filename so we can work with it later
    return filename

def cleanup(song):
    os.remove(song)

# these functions get called by the main script. only needed to make the code easier to understand
def set_tagging(tagging_mode):
    global tagging
    tagging = tagging_mode

def set_path(path):
    global dl_path
    dl_path = path

def main(url, tags_in, song_nr, playlist_title):
    tags_out = {
        'artist': None,
        'album': None,
        'title': None,
        'genre': None,
        'song_nr': None,
    }

    # we only need the inputs when we are tagging manually
    if tagging == 'manual':
        tags_out = tags_in

    # get the title of the song, this is done in a seperate function beacuse pytube throws random errors sometimes.
    # to avoid this we use a try except block and a loop. so we just try again if the fetch fails
    title = get_title(url)

    # download the song in the highest quality available
    with console.status(f"[bold green]Downloading {title}...[/bold green]", spinner="dots"):
        downloaded_song = download(url)
    
    # convert the song to mp3
    converted_song = convert(downloaded_song, title)
    
    # remove the webm file
    cleanup(downloaded_song)

    if tagging != 'off':
        # add the song number to the tags dictionary
        tags_out['song_nr'] = song_nr
        tags_out['album'] = playlist_title

    # use the appropriate tagging method
    with console.status(f"[bold green]Fetching tags for {title}...[/bold green]", spinner="dots"):
        if tagging == 'normal':
            # set the different tags if they are not overwritten by the user
            if tags_out['artist'] == None:
                tags_out['artist'] = get_artist(url)
            if tags_out['title'] == None:
                tags_out['title'] = title
            
            # get the url to the thumbnail image
            thumbnail_url = pyt.YouTube(url).thumbnail_url

        elif tagging == 'experimental':
            # tags which we get from the get_metadata script
            got_tags = get_metadata.main(converted_song)

            # set the different tags if they are not overwritten by the user
            if tags_out['artist'] == None:
                tags_out['artist'] = got_tags['artist']
            if tags_out['title'] == None:
                tags_out['title'] = got_tags['title']
            if tags_out['genre'] == None:
                tags_out['genre'] = got_tags['genre']
            
            # decide which cover to use
            if tn_as_cover == True:
                # get the url to the thumbnail image
                thumbnail_url = pyt.YouTube(url).thumbnail_url
            else:
                # get the cover url
                thumbnail_url = got_tags['cover']
    
        # if we are downloading songs from an artist channel we want to set the album name to the artist name + songs
        if tagging != 'off' and tags_out['album'] == 'Songs':
            tags_out['album'] = tags_out['artist'] + ' Songs'

    # fetch the thumbnail url and apply it to the song if tagging is enabled
    with console.status(f"[bold green]Applying tags to {title}...[/bold green]", spinner="dots"):
        if tagging != 'off':
            # fetch and download the thumbnail image
            img = get_thumbnail.main(thumbnail_url)

            # crop cover
            crop_image.crop(img)

            # set the cover
            setmetadata.set_cover(converted_song, img)
            # set the tags
            setmetadata.main(converted_song, tags_out)
            
            # delete the cover image
            cleanup(img)

# get the uploader of the video and set as artist additionally remove any unnecessary text
def get_artist(url):
    if "Topic" in str(CH(YT(url).channel_url).channel_name):
        _artist = str(CH(YT(url).channel_url).channel_name).removesuffix(" - Topic")
    elif "VEVO" in str(CH(YT(url).channel_url).channel_name):
        _artist = str(CH(YT(url).channel_url).channel_name).removesuffix("VEVO")
    else:
        _artist = str(CH(YT(url).channel_url).channel_name)
    
    return _artist

def get_title(url):
    error = True
    while error == True:
        # get the title of the song
        try:
            title = pyt.YouTube(url).title
            error = False
        except PytubeError:
            pass

    return title