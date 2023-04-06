import ffmpeg
import pytube as pyt
from pytube import YouTube as YT
from pytube import Channel as CH
import os
import setmetadata
import get_thumbnail
import crop_image

tagging = True

def download(url):
    yt=pyt.YouTube(url)
    song=yt.streams.filter(only_audio=True)[-1].download(output_path=os.getcwd() + '/tmp')
    return song

def convert(song):
    # set the new filename with the mp3 extension
    filename=song.split('.')[0]+'.mp3'

    # add the parameters to the ffmpeg command
    stream = ffmpeg.output(ffmpeg.input(song), filename, loglevel="quiet")

    # perform the conversion
    ffmpeg.run(stream)

    # return the new filename so we can work with it later
    return filename

def cleanup(song):
    os.remove(song)
    
def set_tagging(enable_tagging):
    global tagging
    tagging = enable_tagging

def main(url, tags, song_nr, playlist_title):
    # download the song in the highest quality available
    downloaded_song = download(url)
    
    # convert the song to mp3 and remove the webm file
    converted_song = convert(downloaded_song)
    cleanup(downloaded_song)

    # get the url to the thumbnail image
    thumbnail_url = pyt.YouTube(url).thumbnail_url

    # add the song number to the tags dictionary
    tags['song_nr'] = song_nr
    tags['album'] = playlist_title

    if tags['artist'] == None:
        tags['artist'] = get_artist(url)
    if tags['title'] == None:
        tags['title'] = pyt.YouTube(url).title

    # fetch the thumbnail url and apply it to the song if tagging is enabled
    if tagging:
        # fetch and download the thumbnail image
        img = get_thumbnail.main(thumbnail_url)

        # crop cover
        crop_image.crop(img)

        # set the cover
        setmetadata.set_cover(converted_song, img)
        # set the tags
        setmetadata.main(converted_song, tags)
        
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