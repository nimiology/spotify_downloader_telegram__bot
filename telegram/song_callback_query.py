from telethon import events
from telethon.tl.types import PeerUser

from consts import NOT_IN_DB, PROCESSING, DOWNLOADING, UPLOADING, ALREADY_IN_DB
from models import session, SongRequest, User
from spotify.song import Song
from telegram import CLIENT, DB_CHANNEL_ID, BOT_ID
from telegram.templates import song_template


@CLIENT.on(events.CallbackQuery(pattern='song'))
async def song_callback_query(event: events.CallbackQuery.Event):
    data = event.data.decode('utf-8')
    print(f'[TELEGRAM] song callback query: {data}')
    message = await song_template(Song(data[5:]))
    await event.respond(message[0], thumb=message[1], buttons=message[2])


@CLIENT.on(events.CallbackQuery(pattern='download_song'))
async def send_song_callback_query(event: events.CallbackQuery.Event):
    data = event.data.decode('utf-8')
    song_id = data[14:]
    print(f'[TELEGRAM] download song callback query: {song_id}')
    processing = await event.respond(PROCESSING)

    # first check if the song is already in the database
    song_db = session.query(SongRequest).filter_by(spotify_id=song_id).first()
    if song_db:
        await processing.edit(ALREADY_IN_DB)
        message_id = song_db.song_id_in_group
    else:
        # if not, create a new message in the database
        await processing.delete()
        song = Song(song_id)
        await event.respond(NOT_IN_DB)
        # update processing message
        processing = await event.respond(DOWNLOADING)
        file_path = song.download()
        await processing.edit(UPLOADING)
        new_message = await CLIENT.send_message(
            DB_CHANNEL_ID,
            BOT_ID,
            file=file_path
        )
        song.save_db(event.sender_id, new_message.id)
        message_id = new_message.id

    await processing.delete()
    # forward the message
    await CLIENT.forward_messages(
        entity=event.chat_id,  # Destination chat ID
        messages=message_id,  # Message ID to forward
        from_peer=PeerUser(int(DB_CHANNEL_ID))  # ID of the chat/channel where the message is from
    )


@CLIENT.on(events.CallbackQuery(pattern='track_lyrics'))
async def track_lyrics_callback_query(event: events.CallbackQuery.Event):
    data = event.data.decode('utf-8')
    song_id = data[13:]
    print(f'[TELEGRAM] track lyrics callback query: {data}')
    print(song_id)
    print(f'[TELEGRAM] track lyrics callback query: {song_id}')
    await event.respond(f'{Song(song_id).lyrics()}\n\n{BOT_ID}')


@CLIENT.on(events.CallbackQuery(pattern='download_image'))
async def download_image_callback_query(event: events.CallbackQuery.Event):
    data = event.data.decode('utf-8')
    song_id = data[15:]
    print(song_id)
    print(f'[TELEGRAM] download image callback query: {song_id}')
    await event.respond(BOT_ID, file=Song(song_id).album_cover)
