from telethon import Button

from spotify import SPOTIFY


class Album:
    def __init__(self, link):
        self.id = link
        self.spotify = SPOTIFY.album(self.id)
        self.album_name = self.spotify['name']
        self.artists_list = self.spotify['artists']
        self.artist_name = self.artists_list[0]['name']
        self.spotify_link = self.spotify['external_urls']['spotify']
        self.album_cover = self.spotify['images'][0]['url']
        self.release_date = self.spotify['release_date']
        self.total_tracks = self.spotify['total_tracks']
        self.track_list = [x['id'] for x in self.spotify['tracks']['items']]
        self.uri = self.spotify['uri']

    async def album_telegram_template(self):
        message = f'''
💿 Album : `{self.album_name}`
🎤 Artist : `{self.artist_name}`
🎧 Total tracks : `{self.total_tracks}`
📅 Release Date : `{self.release_date}`

[IMAGE]({self.album_cover})
{self.uri}   
        '''

        buttons = [[Button.inline(f'📩Download Album Tracks!', data=f"download_album_songs:{self.id}")],
                   [Button.inline(f'🖼️Download Album Image!', data=f"download_album_image:{self.id}")],
                   [Button.inline(f'🧑‍🎨View Album Artists!', data=f"album_artist:{self.id}")],
                   [Button.url(f'🎵Listen on Spotify', self.spotify_link)],
                   ]

        return message, self.album_cover, buttons

    async def artist_buttons_telethon_templates(self):
        message = f"{self.album_name} album Artist's"
        buttons = [[Button.inline(artist['name'], data=f"artist:{artist['id']}")]
                   for artist in self.artists_list]
        return message, buttons
