# type: ignore
from libraries import download_convert
from ytmusicapi.ytmusic import YTMusic
import platformdirs
import os

# the directory where the oauth file should be saved
config_dir = platformdirs.user_config_dir(
    appname="pydl", appauthor="gro-david", ensure_exists=True
)
browser_path = os.path.join(config_dir, "browser.json")
url_stem = "music.youtube.com/watch?v="


def main(url, playlist, tags, limit):
    # if the url contains '&list=' then its a playlist and if the playlist bool is true we want to loop over the playlist and download songs
    if "&list=" in url or "?list=" in url and playlist == True:
        # create a playlist object
        ytmusic = YTMusic(browser_path)
        playlist = ytmusic.get_playlist(url.split("list=")[-1])
        songs = playlist.get("tracks")
        for i in range(min(limit, len(songs))):
            download_convert.main(
                url_stem + songs[i].get("videoId"), tags, i + 1, playlist.get("title")
            )

        return download_convert.album_name

    else:
        # if its not a playlist then just download the video
        url = url.split("&list=")[0]
        download_convert.main(url, tags, None, None)
        return download_convert.get_title(url)
