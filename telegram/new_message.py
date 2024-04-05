from telethon import events, client

from consts import WELCOME_MESSAGE
from spotify.album import Album
from spotify.artist import Artist
from spotify.playlist import Playlist
from spotify.song import Song
from telegram import CLIENT
from telegram.utils import handle_search_message


@CLIENT.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond(WELCOME_MESSAGE)


async def handle_track(event: events.NewMessage.Event, msg_link):
    print(f'[TELEGRAM] song callback query: {msg_link}')
    message = await Song(msg_link).song_telethon_template()
    await event.respond(message[0], thumb=message[1], buttons=message[2])


async def handle_album(event: events.NewMessage.Event, msg_link):
    print(f'[TELEGRAM] album callback query: {msg_link}')
    message = await Album(msg_link).album_telegram_template()
    await event.respond(message[0], thumb=message[1], buttons=message[2])


async def handle_artist(event: events.NewMessage.Event, msg_link):
    print(f'[TELEGRAM] artist callback query: {msg_link}')
    message = await Artist(msg_link).artist_telethon_template()
    await event.respond(message[0], buttons=message[1])


async def handle_playlist(event: events.NewMessage.Event, msg_link):
    print(f'[TELEGRAM] playlist callback query: {msg_link}')
    message = await Playlist(msg_link).playlist_template()
    await event.respond(message[0], buttons=message[1])


@CLIENT.on(events.NewMessage)
async def download(event: events.NewMessage.Event):
    # message is private
    if event.is_private:
        msg = event.raw_text
        print(f'[TELEGRAM] New message: {msg}')
        msg_link = text_finder(msg)
        if msg_link.startswith('https://open.spotify.com/'):
            # Process different types of Spotify links
            if 'album' in msg_link:
                await handle_album(event, msg_link)
            elif 'track' in msg_link:
                await handle_track(event, msg_link)
            elif 'playlist' in msg_link:
                await handle_playlist(event, msg_link)
            elif 'artist' in msg_link:
                await handle_artist(event, msg_link)
            else:
                await handle_search_message(event)
        else:
            await handle_search_message(event)


def text_finder(txt):
    index = txt.find("https://open.spotify.com")
    if index != -1:
        return txt[index:]
    return ''
