from spotify import SPOTIFY
from spotify.song import Song


def album(link):
    results = SPOTIFY.album_tracks(link)
    albums = results['items']
    while results['next']:
        results = SPOTIFY.next(results)
        albums.extend(results['items'])
    return albums


def artist(link):
    results = SPOTIFY.artist_top_tracks(link)
    albums = results['tracks']
    return albums


def search_album(track):
    results = SPOTIFY.search(track)
    return results['tracks']['items'][0]['album']['external_urls']['spotify']


def playlist(link):
    results = SPOTIFY.playlist_items(link)
    return results['items'][:50]


def search_single(q) -> list[Song]:
    results = SPOTIFY.search(q)
    songs_list = []
    for item in results['tracks']['items']:
        songs_list.append(Song(item['id']))
    return songs_list


def search_artist(artist):
    results = SPOTIFY.search(artist)
    return results['tracks']['items'][0]['artists'][0]["external_urls"]['spotify']
