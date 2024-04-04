from telethon import events

from consts import PROCESSING, ALBUM_HAS_SENT_SUCCESSFULLY
from spotify.album import Album
from spotify.song import Song
from telegram import CLIENT


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
