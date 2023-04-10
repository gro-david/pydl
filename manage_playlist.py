import download_convert
from pytube import Playlist


def main(url, playlist, tags, limit):
    # if the url contains '&list=' then its a playlist and if the playlist bool is true we want to loop over the playlist and download songs
    if '&list=' in url and playlist == True:
        # create a playlist object
        playlist_object = Playlist(url)

        # if the limit is greater than the amount of songs in the playlist then just download all the songs
        if limit > len(playlist_object.video_urls):
            # loop over the playlist
            for i in range(len(playlist_object.video_urls)):
                # download the video
                download_convert.main(playlist_object.video_urls[i], tags, i + 1, playlist_object.title)

        # otherwise just download the amount of songs specified in the limit
        else:
            for i in range(limit):
                # download the video
                download_convert.main(playlist_object.video_urls[i], tags, i + 1, playlist_object.title)
        
        # return the title so we can send a notification
        return download_convert.album_name

    else:
        # if its not a playlist then just download the video
        url = url.split('&list=')[0]
        download_convert.main(url, tags, None, None)
        return download_convert.get_title(url)