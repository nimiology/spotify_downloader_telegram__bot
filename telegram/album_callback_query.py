from telethon import events

from consts import PROCESSING, ALBUM_HAS_SENT_SUCCESSFULLY
from spotify.album import Album
from spotify.song import Song
from telegram import CLIENT, BOT_ID


@CLIENT.on(events.CallbackQuery(pattern='download_album_songs'))
async def download_album_songs_callback_query(event: events.CallbackQuery.Event):
    data = event.data.decode('utf-8')
    album_id = data[21:]
    print(f'[TELEGRAM] download album songs callback query: {album_id}')
    album = Album(album_id)
    processing = await event.respond(PROCESSING)
    for song_id in album.track_list:
        await Song.upload_on_telegram(event=event, song_id=song_id)
    await processing.delete()
    await event.respond(ALBUM_HAS_SENT_SUCCESSFULLY)


@CLIENT.on(events.CallbackQuery(pattern='download_album_image'))
async def download_album_image_callback_query(event: events.CallbackQuery.Event):
    data = event.data.decode('utf-8')
    song_id = data[21:]
    print(f'[TELEGRAM] download album image callback query: {song_id}')
    await event.respond(BOT_ID, file=Album(song_id).album_cover)


@CLIENT.on(events.CallbackQuery(pattern='album_artist'))
async def album_artist_callback_query(event: events.CallbackQuery.Event):
    data = event.data.decode('utf-8')
    album_id = data[13:]
    song = Album(album_id)
    print(f'[TELEGRAM] album artists callback query: {album_id}')
    message = await song.artist_buttons_telethon_templates()
    await event.respond(message=message[0], buttons=message[1])
