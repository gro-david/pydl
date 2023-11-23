import asyncio
from shazamio import Shazam

from pytube import YouTube as YT
from pytube import Channel as CH
from pytube.exceptions import PytubeError


async def recognize(song):
    # intialize the shazam object
    shazam = Shazam()

    # recognize the song and all of the infos
    out = await shazam.recognize_song(song)

    # find the results we are looking for and return them
    genre = out["track"]["genres"]["primary"]
    title = out["track"]["title"]
    artist = out["track"]["subtitle"]
    cover_url = out["track"]["sections"][0]["metapages"][0]["image"]
    return {"title": title, "artist": artist, "genre": genre, "cover": cover_url}


def main(song):
    return asyncio.run(recognize(song))


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
            title = YT(url).title
            error = False
        except PytubeError:
            pass

    return title
