from telethon import Button

from spotify import SPOTIFY


class Playlist:
    def __init__(self, link):
        self.spotify = SPOTIFY.playlist(link)
        self.id = self.spotify['id']
        self.spotify_link = self.spotify['external_urls']['spotify']
        self.playlist_name = self.spotify['name']
        self.description = self.spotify['description']
        self.owner_name = self.spotify['owner']['display_name']
        self.followers_count = self.spotify['followers']['total']
        self.track_count = len(self.spotify['tracks']['items'])
        self.playlist_image = self.spotify['images'][0]['url']
        self.uri = self.spotify['uri']

    async def playlist_template(self):
        message = f'''
▶️Playlist: {self.playlist_name}
📝Description: {self.description}
👤Owner: {self.owner_name}
🩷Followers: {self.followers_count}
🔢Total Track: {self.track_count}

[IMAGE]({self.playlist_image})
{self.uri}  
'''

        buttons = [[Button.inline(f'📩Download Playlist Tracks!', data=f"download_playlist_songs:{self.id}")],
                   [Button.inline(f'🖼️Download Playlist Image!', data=f"download_playlist_image:{self.id}")],
                   [Button.url(f'🎵Listen on Spotify', self.spotify_link)],
                   ]
        return message, buttons

    @staticmethod
    def get_playlist_tracks(link):
        return SPOTIFY.playlist_tracks(link, limit=50)['items']
