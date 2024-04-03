from decouple import config
from telethon import events
from telethon.tl.functions.messages import GetMessagesRequest
from telethon.tl.types import PeerUser

from spotify.song import Song
from telegram import CLIENT
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
    processing = await event.respond('processing...')
    song = Song(song_id)
    # update processing message
    await processing.edit('downloading...')
    file_path = song.download()
    await processing.edit('uploading...')
    new_message = await CLIENT.send_message(
        int(config('DB_CHANNEL_ID')),
        f'forward {song_id}',
        file=file_path
    )
    await CLIENT.forward_messages(
        entity=event.chat_id,  # Destination chat ID
        messages=new_message.id,  # Message ID to forward
        from_peer=PeerUser(int(config('DB_CHANNEL_ID')))  # ID of the chat/channel where the message is from
    )


@CLIENT.on(events.CallbackQuery(pattern='track_lyrics'))
async def track_lyrics_callback_query(event: events.CallbackQuery.Event):
    data = event.data.decode('utf-8')
    song_id = data[13:]
    print(f'[TELEGRAM] track lyrics callback query: {data}')
    print(song_id)
    print(f'[TELEGRAM] track lyrics callback query: {song_id}')
    await event.respond(Song(song_id).lyrics())


@CLIENT.on(events.CallbackQuery(pattern='download_image'))
async def download_image_callback_query(event: events.CallbackQuery.Event):
    data = event.data.decode('utf-8')
    song_id = data[15:]
    print(song_id)
    print(f'[TELEGRAM] download image callback query: {song_id}')
    await event.respond(config('BOT_ID'), file=Song(song_id).album_cover)
