import download_convert
from pytube import Playlist
import read_conf

# we only need the general values but we left the option for other parameters open in case we want to add more later
conf = read_conf.main()
general = conf['General']

def main(url, playlist, tags):
    # if the url contains '&list=' then its a playlist and if the playlist bool is true we want to loop over the playlist and download each song
    if 'list=' in url and playlist:
        # create a playlist object
        playlist = Playlist(url)

        # if the limit is greater than the amount of songs in the playlist then just download all the songs
        if general['dl-limit'] > len(playlist.video_urls):
            # loop over the playlist
            for i in range(len(playlist.video_urls)):
                # download the video
                download_convert.main(playlist.video_urls[i], tags, i + 1, playlist.title)

        # otherwise just download the amount of songs specified in the limit
        else:
            for i in range(general['dl-limit']):
                # download the video
                download_convert.main(playlist.video_urls[i], tags, i + 1, playlist.title)    
    else:
        # if its not a playlist then just download the video
        url = url.split('&list=')[0]
        download_convert.main(url, tags, None, None)

#main(url, True)