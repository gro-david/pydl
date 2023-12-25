# from: https://stackoverflow.com/questions/7391945/how-do-i-read-image-data-from-a-url-in-python
import os
import urllib.request

def main(url):
    path = os.path.join(os.getcwd(), 'album_art.png')
    urllib.request.urlretrieve(url, path)
    return path