from telethon import events

from spotify.artist import Artist
from telegram import CLIENT, BOT_ID


@CLIENT.on(events.CallbackQuery(pattern='download_artist_image'))
async def download_album_image_callback_query(event: events.CallbackQuery.Event):
    data = event.data.decode('utf-8')
    artist_id = data[22:]
    print(f'[TELEGRAM] download artist image callback query: {artist_id}')
    await event.respond(BOT_ID, file=Artist(artist_id).artist_profile)


@CLIENT.on(events.CallbackQuery(pattern='artist_top_tracks'))
async def artist_top_tracks_callback_query(event: events.CallbackQuery.Event):
    data = event.data.decode('utf-8')
    artist_id = data[18:]
    artist = Artist(artist_id)
    print(f'[TELEGRAM] artist top tracks callback query: {artist.id}')
    message = await artist.artist_top_tracks_template()
    await event.respond(message[0], buttons=message[1])


@CLIENT.on(events.CallbackQuery(pattern='artist_albums'))
async def artist_albums_callback_query(event: events.CallbackQuery.Event):
    data = event.data.decode('utf-8')
    artist_id = data[14:]
    artist = Artist(artist_id)
    print(f'[TELEGRAM] artist albums callback query: {artist.id}')
    message = await artist.artist_albums_template()
    await event.respond(message[0], buttons=message[1])


@CLIENT.on(events.CallbackQuery(pattern='artist:'))
async def album_callback_query(event: events.CallbackQuery.Event):
    data = event.data.decode('utf-8')
    print(data)
    artist_id = data[7:]
    print(f'[TELEGRAM] artist callback query: {artist_id}')
    artist = Artist(artist_id)
    message = await artist.artist_telethon_template()
    await event.respond(message=message[0], buttons=message[1], )
