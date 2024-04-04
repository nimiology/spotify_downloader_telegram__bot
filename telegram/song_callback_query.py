from telethon import events, types
from telethon.tl.types import PeerUser

from consts import NOT_IN_DB, PROCESSING, DOWNLOADING, UPLOADING, ALREADY_IN_DB, NO_LYRICS_FOUND
from models import session, SongRequest
from spotify.album import Album
from spotify.song import Song
from telegram import CLIENT, DB_CHANNEL_ID, BOT_ID


@CLIENT.on(events.CallbackQuery(pattern='song'))
async def song_callback_query(event: events.CallbackQuery.Event):
    data = event.data.decode('utf-8')
    print(f'[TELEGRAM] song callback query: {data}')
    message = await Song(data[5:]).song_telethon_template()
    await event.respond(message[0], thumb=message[1], buttons=message[2])


@CLIENT.on(events.CallbackQuery(pattern='download_song'))
async def send_song_callback_query(event: events.CallbackQuery.Event):
    data = event.data.decode('utf-8')
    song_id = data[14:]
    print(f'[TELEGRAM] download song callback query: {song_id}')
    await Song.upload_on_telegram(event, song_id)


@CLIENT.on(events.CallbackQuery(pattern='track_lyrics'))
async def track_lyrics_callback_query(event: events.CallbackQuery.Event):
    data = event.data.decode('utf-8')
    song_id = data[13:]
    print(f'[TELEGRAM] track lyrics callback query: {data}')
    print(song_id)
    print(f'[TELEGRAM] track lyrics callback query: {song_id}')
    lyrics = Song(song_id).lyrics()
    if lyrics is None:
        await event.respond(NO_LYRICS_FOUND)
    else:
        await event.respond(f'{lyrics}\n\n{BOT_ID}')


@CLIENT.on(events.CallbackQuery(pattern='download_song_image'))
async def download_image_callback_query(event: events.CallbackQuery.Event):
    data = event.data.decode('utf-8')
    song_id = data[20:]
    print(f'[TELEGRAM] download song image callback query: {song_id}')
    await event.respond(BOT_ID, file=Song(song_id).album_cover)


@CLIENT.on(events.CallbackQuery(pattern='track_artist'))
async def track_artist_callback_query(event: events.CallbackQuery.Event):
    data = event.data.decode('utf-8')
    song_id = data[13:]
    song = Song(song_id)
    print(f'[TELEGRAM] track artists callback query: {song_id}')
    message = await song.artist_buttons_telethon_templates()
    await event.respond(message=message[0], buttons=message[1])


@CLIENT.on(events.CallbackQuery(pattern='album'))
async def album_callback_query(event: events.CallbackQuery.Event):
    data = event.data.decode('utf-8')
    album_id = data[6:]
    print(f'[TELEGRAM] album callback query: {album_id}')
    message = await Album(album_id).album_telegram_template()
    await event.respond(message[0], thumb=message[1], buttons=message[2])
