from telethon import events, client

from consts import SINGLE_MESSAGE, ARTISTS_MESSAGE, ALBUM_MESSAGE, WELCOME_MESSAGE
from telegram import CLIENT
from telegram.utils import handle_search_message


@CLIENT.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond(WELCOME_MESSAGE)


@CLIENT.on(events.NewMessage(pattern='/album'))
async def album(event):
    await event.respond(ALBUM_MESSAGE)


@CLIENT.on(events.NewMessage(pattern='/artist'))
async def artist(event):
    await event.respond(ARTISTS_MESSAGE)


@CLIENT.on(events.NewMessage(pattern='/single'))
async def single(event):
    await event.respond(SINGLE_MESSAGE)


@CLIENT.on(events.NewMessage)
async def download(event: events.NewMessage.Event):
    msg = event.raw_text
    print(f'[TELEGRAM] New message: {msg}')
    # msg_link = text_finder(msg)
    # if msg_link.startswith('https://open.spotify.com/album'):
    #     await downloader(event, msg, 'AL')
    # elif msg_link.startswith('https://open.spotify.com/track'):
    #     await download_song(event, msg_link)
    # elif msg.startswith('https://open.spotify.com/playlist'):
    #     await downloader(event, msg, 'PL')
    # elif msg_link.startswith('https://open.spotify.com/artist'):
    #     await downloader(event, msg, 'AR')
    # else:
    await handle_search_message(event)

# def text_finder(txt):
#     index = txt.find("https://open.spotify.com")
#     if index != -1:
#         return txt[index:]
#     return ''
#
# async def downloader(event, link, type):
#     if type == 'AL':
#         items = spotify.album(link)
#     elif type == 'AR':
#         items = spotify.artist(link)
#     elif type == 'PL':
#         items = spotify.playlist(link)
#     else:
#         items = []
#
#     message = ""
#     count = 0
#     for song in items:
#         if type == 'PL':
#             song = song['track']
#         count += 1
#         message += f"{count}. {song['name']}\n"
#     await event.respond(message)
#
#     for song in items:
#         if type == 'PL':
#             song = song['track']
#         await download_song(event, song['href'])
#
#
# async def download_song(event, link):
#     song = spotify.Song(link)
#     song.yt_link()
#     try:
#         song.yt_download()
#         song.song_meta_data()
#         caption = f'Track: {song.trackName}\nAlbum: {song.album}\nArtist: {song.artist}'
#         await event.respond(file=open(f'{song.trackName}.mp3', 'rb'), caption=caption)
#     except:
#         await event.respond(f'404\n"{song.trackName}" Not Found')
