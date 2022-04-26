import datetime
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from youtube_search import YoutubeSearch
import youtube_dl
import eyed3.id3
import eyed3
import lyricsgenius

spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(client_id='a145db3dcd564b9592dacf10649e4ed5',
                                                        client_secret='389614e1ec874f17b8c99511c7baa2f6'))
genius = lyricsgenius.Genius('biZZReO7F98mji5oz3cE0FiIG73Hh07qoXSIzYSGNN3GBsnY-eUrPAVSdJk_0_de')


class Song:
    def __init__(self, link):
        self.link = link
        self.song = spotify.track(link)
        self.trackName = self.song['name']
        self.artist = self.song['artists'][0]['name']
        self.artists = self.song['artists']
        self.trackNumber = self.song['track_number']
        self.album = self.song['album']['name']
        self.releaseDate = int(self.song['album']['release_date'][:4])
        self.duration = int(self.song['duration_ms'])

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

    def ConvertTimeDuration(self):
        target_datetime_ms = self.duration
        base_datetime = datetime.datetime(1900, 1, 1)
        delta = datetime.timedelta(0, 0, 0, target_datetime_ms)
        target_datetime1 = base_datetime + delta
        target_datetime1 = target_datetime1.replace(microsecond=0)
        target_datetime2 = target_datetime1 + datetime.timedelta(seconds=1)
        target_datetime3 = target_datetime1 + datetime.timedelta(seconds=2)
        target_datetime4 = target_datetime1 + datetime.timedelta(seconds=3)

        target_datetime5 = target_datetime1 - datetime.timedelta(seconds=1)
        target_datetime6 = target_datetime1 - datetime.timedelta(seconds=2)
        target_datetime7 = target_datetime1 - datetime.timedelta(seconds=3)

        return target_datetime1, \
               target_datetime2, \
               target_datetime3, \
               target_datetime4, \
               target_datetime5, \
               target_datetime6, \
               target_datetime7

    def DownloadSongCover(self):
        response = requests.get(self.song['album']['images'][0]['url'])
        imageFileName = self.trackName + ".png"
        image = open(imageFileName, "wb")
        image.write(response.content)
        image.close()
        return imageFileName

    def YTLink(self):
        results = list(YoutubeSearch(str(self.trackName + " " + self.artist)).to_dict())
        time_duration1, time_duration2, time_duration3, time_duration4,\
        time_duration5, time_duration6, time_duration7 = self.ConvertTimeDuration()
        YTSlug = ''

        for URLSSS in results:
            timeyt = URLSSS["duration"]
            timeyt = datetime.datetime.strptime(timeyt, '%M:%S')

            if timeyt == time_duration1 or timeyt == time_duration2 \
                    or timeyt == time_duration3 or timeyt == time_duration4 or \
                    timeyt == time_duration5 or timeyt == time_duration6 or \
                    timeyt == time_duration7:
                YTSlug = URLSSS['url_suffix']
                break

        YTLink = str("https://www.youtube.com/" + YTSlug)
        return YTLink

    def YTDownload(self):
        options = {
            # PERMANENT options
            'format': 'bestaudio/best',
            'keepvideo': True,
            'outtmpl': f'{self.trackName}.*',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320'
            }],
        }

        with youtube_dl.YoutubeDL(options) as mp3:
            mp3.download([self.YTLink()])

    def SongMetaData(self):
        mp3 = eyed3.load(f"{self.trackName}.mp3")
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
