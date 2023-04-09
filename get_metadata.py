import asyncio
from shazamio import Shazam


async def recognize(song):
    # intialize the shazam object
    shazam = Shazam()

    # recognize the song and all of the infos
    out = await shazam.recognize_song(song)

    # find the results we are looking for and return them
    genre = out['track']['genres']['primary']
    title = out['track']['title']
    artist = out['track']['subtitle']
    cover_url = out['track']['sections'][0]['metapages'][0]['image']
    return {'title': title, 'artist': artist, 'genre': genre, 'cover': cover_url}


def main(song):
    return asyncio.run(recognize(song))

if __name__ == '__main__':
    print(main('tmp/Hero.mp3'))