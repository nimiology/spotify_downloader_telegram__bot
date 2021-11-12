from __future__ import unicode_literals
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from youtube_search import YoutubeSearch
import youtube_dl
import eyed3.id3
import eyed3
import lyricsgenius
import telepot

spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(client_id='a145db3dcd564b9592dacf10649e4ed5',
                                                        client_secret='389614e1ec874f17b8c99511c7baa2f6'))
genius = lyricsgenius.Genius('biZZReO7F98mji5oz3cE0FiIG73Hh07qoXSIzYSGNN3GBsnY-eUrPAVSdJk_0_de')

token = 'token bot'
bot = telepot.Bot(token)


class Song:
    def __init__(self, link, chat_id):
        self.chat_id = chat_id
        self.link = link
        self.song = spotify.track(link)
        self.trackName = self.song['name']
        self.artist = self.song['artists'][0]['name']
        self.artists = self.song['artists']
        self.trackNumber = self.song['track_number']
        self.album = self.song['album']['name']
        self.releaseDate = int(self.song['album']['release_date'][:4])
        self.duration = int(self.song['duration_ms'])

    # find features
    def Features(self):
        if len(self.artists) > 1:
            features = "(Ft."
            for artistPlace in range(0, len(self.artists)):
                try:
                    if artistPlace < len(self.artists) - 2:
                        artistft = self.artists[artistPlace + 1]['name'] + ", "
                    else:
                        artistft = self.artists[artistPlace + 1]['name'] + ")"
                    features += artistft
                except:
                    pass
        else:
            features = ""
        return features

    # convert time duration
    def ConvertTimeDuration(self):
        seconds = (self.duration / 1000) % 60
        minutes = (self.duration / (1000 * 60)) % 60
        seconds = int(seconds)
        minutes = int(minutes)

        if seconds >= 10:
            time_duration1 = "{0}:{1}".format(minutes, seconds)
            time_duration2 = "{0}:{1}".format(minutes, seconds + 1)
            time_duration3 = "{0}:{1}".format(minutes, seconds - 1)
            time_duration4 = "{0}:{1}".format(minutes, seconds + 2)

            if seconds == 10:
                time_duration3 = "{0}:0{1}".format(minutes, seconds - 1)
            elif seconds == 58 or seconds == 59:
                time_duration4 = "{0}:0{1}".format(minutes + 1, seconds - 58)
                if seconds == 59:
                    time_duration2 = "{0}:0{1}".format(minutes + 1, seconds - 59)

        else:
            time_duration1 = "{0}:0{1}".format(minutes, seconds)
            time_duration2 = "{0}:0{1}".format(minutes, seconds + 1)
            time_duration3 = "{0}:0{1}".format(minutes, seconds - 1)
            time_duration4 = "{0}:0{1}".format(minutes, seconds + 2)
            if seconds == 9 or seconds == 8:
                time_duration4 = "{0}:{1}".format(minutes, seconds + 2)
                if seconds == 9:
                    time_duration2 = "{0}:{1}".format(minutes, seconds + 1)

            elif seconds == 0:
                time_duration3 = "{0}:{1}".format(minutes - 1, seconds + 59)
        return time_duration1, time_duration2, time_duration3, time_duration4

    # download song cover
    def DownloadSongCover(self):
        response = requests.get(self.song['album']['images'][0]['url'])
        imageFileName = "songpicts/" + self.trackName + ".png"
        image = open(imageFileName, "wb")
        image.write(response.content)
        image.close()
        return imageFileName

    # search for youtube link
    def YTLink(self):
        results = list(YoutubeSearch(str(self.trackName + " " + self.artist)).to_dict())
        time_duration1, time_duration2, time_duration3, time_duration4 = self.ConvertTimeDuration()
        YTSlug = ''
        for URLSSS in results:
            timeyt = URLSSS["duration"]
            if timeyt == time_duration1 or timeyt == time_duration2 \
                    or timeyt == time_duration3 or timeyt == time_duration4:
                YTSlug = URLSSS['url_suffix']
                break

        YTLink = str("https://www.youtube.com/" + YTSlug)
        return YTLink

    # download song
    def YTDownload(self):
        options = {
            # PERMANENT options
            'format': 'bestaudio/best',
            'keepvideo': False,
            'outtmpl': f'song/{self.trackName}.*',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320'
            }],
        }

        with youtube_dl.YoutubeDL(options) as mp3:
            mp3.download([self.YTLink()])

    # merge song metadata to song
    def SongMetaData(self):
        mp3 = eyed3.load(f"song/{self.trackName}.mp3")
        mp3.tag.artist = self.artist
        mp3.tag.album = self.album
        mp3.tag.album_artist = self.artist
        mp3.tag.title = self.trackName + self.Features()
        mp3.tag.track_num = self.trackNumber
        mp3.tag.year = self.trackNumber
        try:
            songGenius = genius.search_song(self.trackName, self.artist)
            mp3.tag.lyrics.set(songGenius.lyrics)
        except:
            pass
        mp3.tag.images.set(3, open(self.DownloadSongCover(), 'rb').read(), 'image/png')
        mp3.tag.save()

    def Telegram(self):
        if self.YTLink() != 'https://www.youtube.com/':
            self.YTDownload()
            self.SongMetaData()
            caption = f'Track: {self.trackName}\nAlbum: {self.album}\nArtist: {self.artist}'
            bot.sendAudio(self.chat_id, open(f'song//{self.trackName}.mp3', 'rb'), title=self.trackName,
                          caption=caption)
        else:
            bot.sendSticker(self.chat_id, 'CAACAgQAAxkBAAIFSWBF_m3GHUtZJxQzobvD_iWxYVClAAJuAgACh4hSOhXuVi2-7-xQHgQ')
            bot.sendMessage(self.chat_id, f'404\n"{self.trackName}" Not Found')


def album(link):
    results = spotify.album_tracks(link)
    albums = results['items']
    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])
    return albums


def artist(link):
    results = spotify.artist_top_tracks(link)
    albums = results['tracks']
    return albums


def searchalbum(track):
    results = spotify.search(track)
    return results['tracks']['items'][0]['album']['external_urls']['spotify']


def playlist(link):
    results = spotify.playlist_tracks(link)
    return results['items'][:50]


def searchsingle(track):
    results = spotify.search(track)
    return results['tracks']['items'][0]['href']


def searchartist(searchstr):
    results = spotify.search(searchstr)
    return results['tracks']['items'][0]['artists'][0]["external_urls"]['spotify']
