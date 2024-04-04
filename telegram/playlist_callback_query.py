from telethon import events

from consts import PROCESSING, ALBUM_HAS_SENT_SUCCESSFULLY, PLAYLIST_HAS_SENT_SUCCESSFULLY
from spotify.playlist import Playlist
from spotify.song import Song
from telegram import CLIENT, BOT_ID


@CLIENT.on(events.CallbackQuery(pattern='download_playlist_songs'))
async def download_album_songs_callback_query(event: events.CallbackQuery.Event):
    data = event.data.decode('utf-8')
    playlist_id = data[24:]
    print(f'[TELEGRAM] download playlist songs callback query: {playlist_id}')
    processing = await event.respond(PROCESSING)
    for song_id in Playlist.get_playlist_tracks(playlist_id):
        print(song_id)
        await Song.upload_on_telegram(event=event, song_id=song_id['track']['id'])
    await processing.delete()
    await event.respond(PLAYLIST_HAS_SENT_SUCCESSFULLY)


@CLIENT.on(events.CallbackQuery(pattern='download_playlist_image'))
async def download_album_image_callback_query(event: events.CallbackQuery.Event):
    data = event.data.decode('utf-8')
    playlist_id = data[24:]
    print(f'[TELEGRAM] download playlist image callback query: {playlist_id}')
    await event.respond(BOT_ID, file=Playlist(playlist_id).playlist_image)


@CLIENT.on(events.CallbackQuery(pattern='playlist:'))
async def album_artist_callback_query(event: events.CallbackQuery.Event):
    data = event.data.decode('utf-8')
    playlist_id = data[9:]
    playlist = Playlist(playlist_id)
    print(f'[TELEGRAM] playlist callback query: {playlist_id}')
    message = await playlist.playlist_template()
    await event.respond(message=message[0], buttons=message[1])
