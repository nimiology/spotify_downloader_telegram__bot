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


async def progress_callback(processing, sent_bytes, total):
    percentage = sent_bytes / total * 100
    await processing.edit(f"Uploading: {percentage:.2f}%")


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

        upload_file = await CLIENT.upload_file(file_path,
                                               progress_callback=lambda sent_bytes, total: progress_callback(processing,
                                                                                                             sent_bytes,
                                                                                                             total))
        new_message = await CLIENT.send_file(
            DB_CHANNEL_ID,
            caption=BOT_ID,
            file=upload_file,
            supports_streaming=True,
            attributes=(
                types.DocumentAttributeAudio(title=song.track_name, duration=song.duration_to_seconds,
                                             performer=song.artist_name),),

        )
        await processing.delete()
        song.save_db(event.sender_id, new_message.id)
        message_id = new_message.id

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
