from __future__ import unicode_literals
import os
from youtube_search import YoutubeSearch
import youtube_dl
import subprocess
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import eyed3.id3
import eyed3
import lyricsgenius
import requests
import telepot
import time

token = 'telegram token'
bot = telepot.Bot(token)

genius = lyricsgenius.Genius('genius api token')
spotifyy = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(client_id='client id spotify',
                                                        client_secret='client server spotify'))


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        def download(lenk, chat_id = chat_id):
            results = spotifyy.track(lenk)
            song = results['name']
            artist = results['artists'][0]['name']
            song_name = str(song + " " + artist)
            song_name_folder = str(song + " - " + artist)
            artistfinder = results['artists']
            if len(artistfinder) > 1:
                fetures = "( Ft."
                for lomi in range(0, len(artistfinder)):
                    try:
                        if lomi < len(artistfinder) - 2:
                            artistft = artistfinder[lomi + 1]['name'] + ", "
                            fetures += artistft
                        else:
                            artistft = artistfinder[lomi + 1]['name'] + ")"
                            fetures += artistft
                    except:
                        pass
            else:
                fetures = ""

            millis = results['duration_ms']
            millis = int(millis)
            seconds = (millis / 1000) % 60
            seconds = int(seconds + 1)
            minutes = (millis / (1000 * 60)) % 60
            minutes = int(minutes)
            time_duration = "%d:%d" % (minutes, seconds)

            trackname = results['name'] + fetures
            albumartist = results['artists'][0]['name']
            tracknumber = results['track_number']
            albumname = results['album']['name']
            releasedate = results['album']['release_date']

            bot.sendMessage(chat_id, "Song Found : " + song_name +
                            '\ntrack : ' + trackname +
                            '\nalbum artist : ' + albumartist +
                            "\ntrack num : {0}".format(tracknumber) +
                            "\nAlbum name : " + albumname +
                            '\nrealese date : ' + releasedate +
                            '\nduration : {0}'.format(time_duration))
            try:
                bot.sendMessage(chat_id, "Searching...")
                aud = eyed3.load(f"song//{song_name_folder}.mp3")
                results = spotifyy.track(lenk)
                try:
                    songbook = genius.search_song(results['name'], results['artists'][0]['name'])
                    try:
                        bot.sendMessage(chat_id, songbook.lyrics)
                    except:
                        pass
                except:
                    pass

                response = requests.get(results['album']['images'][0]['url'])
                DIRCOVER = "songpicts//" + trackname + ".png"
                file = open(DIRCOVER, "wb")
                file.write(response.content)
                file.close()

                aud.tag.artist = artist
                aud.tag.album = albumname
                aud.tag.album_artist = albumartist
                aud.tag.title = trackname
                aud.tag.track_num = tracknumber
                aud.tag.year = int(releasedate[:4])
                try:
                    aud.tag.lyrics.set(songbook.lyrics)
                except:
                    pass
                aud.tag.images.set(3, open(DIRCOVER, 'rb').read(), 'image/png')
                aud.tag.save()
                bot.sendMessage(chat_id, "Sending...")
                print("Sending")
                bot.sendAudio(chat_id, open(f'song//{song_name_folder}.mp3', 'rb'), title=trackname)
                print("Finished!")
            except:
                song_name_final = song_name.replace(" ", "+")
                pre_url = "https://www.youtube.com/results?search_query="
                yt_search = pre_url + song_name_final
                print(yt_search)

                results = list(YoutubeSearch(str(song_name)).to_dict())
                for URLSSS in range(0, len(results)):
                    if results[URLSSS]["duration"] == time_duration:
                        LINKASLI = results[URLSSS]['url_suffix']
                try:
                    print(LINKASLI)
                except:
                    bot.sendMessage(chat_id, "404 \n NOT FOUND")

                print("Song Found")
                yt_pre = str("https://www.youtube.com/" + LINKASLI)
                print(yt_pre)
                bot.sendMessage(chat_id, "Downloading... ")

                def check():
                    import importlib
                    try:
                        importlib.import_module('youtube_dl')

                    except ModuleNotFoundError:
                        print('youtube-dl NOT FOUND in this Computer !')
                        print('The SCRIPT will install youtube-dl python package . . .')
                        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'youtube-dl'])

                    finally:
                        globals()['youtube_dl'] = importlib.import_module('youtube_dl')
                        run()

                ffmpeg_path = os.getcwd()

                def tag():
                    results = spotifyy.track(lenk)
                    try:
                        songbook = genius.search_song(results['name'], results['artists'][0]['name'])
                        try:
                            bot.sendMessage(chat_id, songbook.lyrics)
                        except:
                            pass
                    except:
                        pass

                    response = requests.get(results['album']['images'][0]['url'])
                    DIRCOVER = "songpicts//" + trackname + ".png"
                    file = open(DIRCOVER, "wb")
                    file.write(response.content)
                    file.close()

                    aud = eyed3.load(f"song//{song_name_folder}.mp3")
                    aud.tag.artist = artist
                    aud.tag.album = albumname
                    aud.tag.album_artist = albumartist
                    aud.tag.title = trackname
                    aud.tag.track_num = tracknumber
                    aud.tag.year = int(releasedate[:4])
                    try:
                        aud.tag.lyrics.set(songbook.lyrics)
                    except:
                        pass
                    aud.tag.images.set(3, open(DIRCOVER, 'rb').read(), 'image/png')
                    aud.tag.save()
                    bot.sendMessage(chat_id, "Sending...")
                    print("Sending")
                    bot.sendAudio(chat_id, open(f'song//{song_name_folder}.mp3', 'rb'), title=trackname)

                def run():
                    options = {
                        # PERMANENT options
                        'format': 'bestaudio/best',
                        'ffmpeg_location': f'{ffmpeg_path}/ffmpeg.exe',
                        'keepvideo': False,
                        'outtmpl': f'song//{song_name_folder}.*',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '320'
                        }],

                        # (OPTIONAL options)
                        'noplaylist': True
                    }

                    with youtube_dl.YoutubeDL(options) as mp3:
                        mp3.download([yt_pre])
                        bot.sendMessage(chat_id, "Downloaded.")
                        tag()
                        print("Download Completed!")

                if __name__ == '__main__':
                    check()

        leenk = msg['text']




        if leenk[:30]==('https://open.spotify.com/album') :

            results = spotifyy.album_tracks(leenk)
            albums = results['items']
            while results['next']:
                results = spotifyy.next(results)
                albums.extend(results['items'])

            for album in albums:
                download(album['id'])
        elif leenk[:30]== ('https://open.spotify.com/track')  :

            download(leenk)

        else:
            bot.sendMessage(chat_id,"Link invalid")
bot.message_loop(handle)

print('Listening ...')

while 1:
    time.sleep(10)
