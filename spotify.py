import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import valuetotxt
import requests

spotifyy = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(client_id='client id',
                                                        client_secret='client secret'))




class Detail:
    def __init__(self, link):
        self.results = spotifyy.track(link)
        self.song = self.results['name']
        self.artist = self.results['artists'][0]['name']
        self.song_name = str(self.song + " " + self.artist)
        self.song_name_folder = str(self.song + " - " + self.artist)
        self.artistfinder = self.results['artists']
        self.tracknum = self.results['track_number']
        self.album = self.results['album']['name']
        self.realese_date = int(self.results['album']['release_date'][:4])
        if len(self.artistfinder) > 1:
            self.fetures = "( Ft."
            for lomi in range(0, len(self.artistfinder)):
                try:
                    if lomi < len(self.artistfinder) - 2:
                        artistft = self.artistfinder[lomi + 1]['name'] + ", "
                        self.fetures += artistft
                    else:
                        artistft = self.artistfinder[lomi + 1]['name'] + ")"
                        self.fetures += artistft
                except:
                    pass
        else:
            self.fetures = ""

        self.time_duration = ""
        self.time_duration1 = ""
        self.time_duration2 = ""
        self.time_duration3 = ""
        millis = self.results['duration_ms']
        millis = int(millis)
        seconds = (millis / 1000) % 60
        minutes = (millis / (1000 * 60)) % 60
        self.seconds = int(seconds)
        self.minutes = int(minutes)
        if seconds >= 10:
            if seconds < 59:
                self.time_duration = "{0}:{1}".format(self.minutes, self.seconds)
                self.time_duration1 = "{0}:{1}".format(self.minutes, self.seconds + 1)
                self.time_duration2 = "{0}:{1}".format(self.minutes, self.seconds - 1)
                if seconds == 10:
                    self.time_duration2 = "{0}:0{1}".format(self.minutes, self.seconds - 1)
                    self.time_duration3 = "{0}:{1}".format(self.minutes, self.seconds + 2)
                elif seconds < 58:
                    self.time_duration3 = "{0}:{1}".format(self.minutes, self.seconds + 2)
                    self.time_duration2 = "{0}:{1}".format(self.minutes, self.seconds - 1)
                elif seconds == 58:
                    self.time_duration3 = "{0}:0{1}".format(self.minutes + 1, self.seconds - 58)
                    self.time_duration2 = "{0}:{1}".format(self.minutes, self.seconds - 1)
                else:
                    self.time_duration2 = "{0}:{1}".format(self.minutes, self.seconds - 1)
            else:
                self.time_duration1 = "{0}:0{1}".format(self.minutes + 1, self.seconds - 59)
                if seconds == 59:
                    self.time_duration3 = "{0}:0{1}".format(self.minutes + 1, self.seconds - 58)
        else:
            self.time_duration = "{0}:0{1}".format(self.minutes, self.seconds)
            self.time_duration1 = "{0}:0{1}".format(self.minutes, self.seconds + 1)

            if seconds < 8:
                self.time_duration3 = "{0}:0{1}".format(self.minutes, self.seconds + 2)
                self.time_duration2 = "{0}:0{1}".format(self.minutes, self.seconds - 1)
            elif seconds == 9 or seconds == 8:
                self.time_duration3 = "{0}:{1}".format(self.minutes, self.seconds + 2)

            elif seconds == 0:
                self.time_duration2 = "{0}:{1}".format(self.minutes - 1, self.seconds + 59)
                self.time_duration3 = "{0}:0{1}".format(self.minutes, self.seconds + 2)
            else:
                self.time_duration2 = "{0}:0{1}".format(self.minutes, self.seconds - 1)
                self.time_duration3 = "{0}:0{1}".format(self.minutes, self.seconds + 2)

        self.trackname = self.song + self.fetures

        response = requests.get(self.results['album']['images'][0]['url'])
        DIRCOVER = "songpicts//" + self.trackname + ".png"
        file = open(DIRCOVER, "wb")
        file.write(response.content)
        file.close()

        txt = f'{self.song}\n{self.artist}\n{self.song_name}\n{self.song_name_folder}\n' \
              f'{self.trackname}\n{self.time_duration}\n{self.time_duration1}\n' \
              f'{self.realese_date}\n{self.tracknum}\n{self.album}\n{self.time_duration2}\n' \
              f'{self.time_duration3}\n'

        valuetotxt.savetxt(txt)


def album(link):
    results = spotifyy.album_tracks(link)
    albums = results['items']
    while results['next']:
        results = spotifyy.next(results)
        albums.extend(results['items'])
    return albums


def artist(link):
    results = spotifyy.artist_top_tracks(link)
    albums = results['tracks']
    return albums


def searchalbum(track):
    results = spotifyy.search(track)
    return results['tracks']['items'][0]['album']['external_urls']['spotify']


def searchsingle(track):
    results = spotifyy.search(track)
    return results['tracks']['items'][0]['href']


def searchartist(searchstr):
    results = spotifyy.search(searchstr)
    return results['tracks']['items'][0]['artists'][0]["external_urls"]['spotify']




