import eyed3.id3
import eyed3
from detail import Detail
import requests
import lyricsgenius


genius = lyricsgenius.Genius('your genius token')

def tag(lenk,name):
    DETAIL = Detail(lenk)
    results = DETAIL.results


    response = requests.get(results['album']['images'][0]['url'])
    DIRCOVER = "songpicts//" + results['name'] + DETAIL.fetures + ".png"
    file = open(DIRCOVER, "wb")
    file.write(response.content)
    file.close()

    aud = eyed3.load(f"song//{DETAIL.song_name_folder}.mp3")
    aud.tag.artist = results['artists'][0]['name']
    aud.tag.album = results['album']['name']
    aud.tag.album_artist = results['artists'][0]['name']
    aud.tag.title = results['name'] + DETAIL.fetures
    aud.tag.track_num = results['track_number']
    aud.tag.year = int(results['album']['release_date'][:4])
    try:
        songok = genius.search_song(results['name'], results['artists'][0]['name'])
        aud.tag.lyrics.set(songok.lyrics)
    except:
        pass
    aud.tag.images.set(3, open(DIRCOVER, 'rb').read(), 'image/png')
    aud.tag.save()

def lyrics(lenk):
    try:
        DETAIL = Detail(lenk)
        results = DETAIL.results
        songok = genius.search_song(results['name'], results['artists'][0]['name'])
        return songok.lyrics
    except:
        pass
