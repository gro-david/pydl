import download_convert
from pytube import Playlist
"""
url = str(input('Enter the url:   '))

while True:
    global playlist
    playlist_input = input('Do you want to download the complete playlist (Y/n):   ')

    if(playlist_input.lower() == 'y' or playlist_input == ''):
        playlist = True
        break
    elif(playlist_input.lower() == 'n'):
        playlist = False
        break
    else:
        print('Invalid input')
""" 


def main(url, playlist, tags):
    # if the url contains '&list=' then its a playlist and if the playlist bool is true we want to loop over the playlist and download each song
    if 'list=' in url and playlist:
        # create a playlist object
        playlist = Playlist(url)
        # loop over the playlist
        for i in range(len(playlist.video_urls)):
            # download the video
            download_convert.main(playlist.video_urls[i], tags, i + 1, playlist.title)
    else:
        # if its not a playlist then just download the video
        url = url.split('&list=')[0]
        download_convert.main(url, tags, None, None)

#main(url, True)