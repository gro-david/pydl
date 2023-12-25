from mutagen import *
from mutagen.mp3 import EasyMP3 as MP3
from mutagen.id3 import ID3, APIC

# tags is a dictionary with the following keys:
    # artist
    # album
    # title
    # genre
    # year
    # tracknumber

def main(file, tags):
    # create a mutagen mp3 object
    mp3 = MP3(file)

    # enable tagging if not already enabled
    try: 
        mp3.add_tags()
    except MutagenError:
        pass

    # set the tags based on the inbput values if they exist
    if tags['artist'] != None:
        mp3['artist'] = tags['artist']

    if tags['album'] != None:
        mp3['album'] = tags['album']
        
    if tags['title'] != None:
        mp3['title'] = tags['title']
        
    if tags['genre'] != None:
        mp3['genre'] = tags['title']

    if tags['song_nr'] != None:
        mp3['tracknumber'] = str(tags['song_nr'])
    
    if tags['genre'] != None:
        mp3['genre'] = tags['genre']

    # write the changes
    mp3.save()

def set_cover(file, img):
    # create a mutagen id3 object
    id3 = ID3(file)

    # set the cover using the APIC attribute
    with open(img, 'rb') as albumart:
        id3['APIC'] = APIC(encoding=3, mime='image/jpeg', type=3, desc=u'Cover', data=albumart.read())

    # write the changes
    id3.save()