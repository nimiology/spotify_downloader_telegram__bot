import eyed3.id3
import eyed3
import lyricsgenius
from valuetotxt import read

genius = lyricsgenius.Genius('your genius token')

def tag():

    song = read(0)
    artist = read(1)
    song_name_folder = read(3)
    trackname = read(4)
    realese_date = read(7)
    tracknum = read(8)
    album = read(9)

    aud = eyed3.load(f"song//{song_name_folder}.mp3")
    aud.tag.artist = artist
    aud.tag.album = album
    aud.tag.album_artist = artist
    aud.tag.title = trackname
    aud.tag.track_num = tracknum
    aud.tag.year = realese_date
    try:
        songok = genius.search_song(song, artist)
        aud.tag.lyrics.set(songok.lyrics)
    except:
        pass
    aud.tag.images.set(3, open("songpicts//" + trackname + ".png", 'rb').read(), 'image/png')
    aud.tag.save()
