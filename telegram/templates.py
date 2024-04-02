from telethon import events, Button

from spotify.song import Song


async def song_template(song: Song):
    message = f'''
🎧 Title :`{song.track_name}`
🎤 Artist : `{song.artist}{song.features()}`
💿 Album : `{song.album}`
📅 Release Date : `{song.release_date}`

[IMAGE]({song.album_cover})
ID:Song:{song.id}    
    '''

    buttons = [[Button.inline(f'📩Download Track!', data=f"download_song:{song.id}")],
               [Button.inline(f'🖼️Download Track Image!', data=f"download_image:{song.id}")],
               [Button.inline(f'👀View Track Album!', data=f"album:{song.album}")],
               [Button.inline(f'🧑‍🎨View Track Artists!', data=f"tack_artist:{song.id}")],
               [Button.inline(f'📃View Track Lyrics!', data=f"track_lyrics:{song.id}")],
               [Button.url(f'🎵Listen on Spotify', f"https://open.spotify.com/track/{song.id}")],
               ]

    return message, song.album_cover, buttons

