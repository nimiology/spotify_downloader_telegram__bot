import lyricsgenius
import spotipy
from decouple import config

SPOTIFY = spotipy.Spotify(
    client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials(client_id=config("SPOTIPY_CLIENT_ID"),
                                                                       client_secret=config("SPOTIPY_CLIENT_SECRET")))

GENIUS = lyricsgenius.Genius(config("GENIUS_ACCESS_TOKEN"))
