from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
import spotify


def text_finder(txt):
    a = txt.find("https://open.spotify.com")
    txt = txt[a:]
    return txt


def downloader(update, context, link, type):
    if type == 'AL':
        ITEMS = spotify.album(link)
    elif type == 'AR':
        ITEMS = spotify.artist(link)
    elif type == 'PL':
        ITEMS = spotify.playlist(link)
    else:
        ITEMS = []

    MESSAGE = ""
    COUNT = 0
    for song in ITEMS:
        if type == 'PL':
            song = song['track']
        COUNT += 1
        MESSAGE += f"{COUNT}. {song['name']}\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=MESSAGE)

    for song in ITEMS:
        if type == 'PL':
            song = song['track']
        download_song(update, context, song['href'])


def download_song(update, context, link):
    song = spotify.Song(link)
    song.YTLink()
    try:
        song.YTDownload()
        song.SongMetaData()
        caption = f'Track: {song.trackName}\nAlbum: {song.album}\nArtist: {song.artist}'
        context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(f'{song.trackName}.mp3', 'rb'),
                               caption=caption, title=song.trackName)
    except:
        context.bot.send_sticker(chat_id=update.effective_chat.id,
                                 sticker='CAACAgQAAxkBAAIFSWBF_m3GHUtZJxQzobvD_iWxYVClAAJuAgACh4hSOhXuVi2-7-xQHgQ')
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'404\n"{song.trackName}" Not Found')


WELCOME = '''Hi
This is Spotify Downloader!
You can use the command.'''
ARTISTS_MESSAGE = '''send name and name of artist like this: Name artist'''
SINGLE_MESSAGE = '''send name and name of artist like this:
Name song
or for better search use this:
Name song - Name artist
'''
ALBUM_MESSAGE = '''send name and name of artist like this: 
Name album
or for better search use this:
Name album - Name artist
'''

sort = {}
telegram_token = 'token'

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=WELCOME)


def album(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=SINGLE_MESSAGE)
    sort[update.effective_chat.id] = 'album'


def artist(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=ARTISTS_MESSAGE)
    sort[update.effective_chat.id] = 'artist'


def single(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=SINGLE_MESSAGE)
    sort[update.effective_chat.id] = 'single'


def download(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    msg = update.message.text
    msglink = text_finder(msg)
    if msglink[:30] == ('https://open.spotify.com/album'):
        downloader(update, context, msg, 'AL')

    elif msglink[:30] == ('https://open.spotify.com/track'):
        download_song(update, context, msglink)

    elif msg[:33] == 'https://open.spotify.com/playlist':
        downloader(update, context, msg, 'PL')

    elif msglink[:31] == ('https://open.spotify.com/artist'):
        downloader(update, context, msg, 'AR')
    else:
        if chat_id in sort:
            if sort[chat_id] == 'artist':
                downloader(update, context, spotify.searchartist(msg), 'AR')
            elif sort[chat_id] == 'album':
                downloader(update, context, spotify.searchalbum(msg), 'AL')
            elif sort[chat_id] == 'single':
                download_song(update, context, spotify.searchsingle(msg))
            del sort[chat_id]
        else:
            context.bot.send_sticker(chat_id=update.effective_chat.id,
                                     sticker='CAACAgQAAxkBAAIBFGBLNcpfFcTLxnn5lR20ZbE2EJbrAAJRAQACEqdqA2XZDc7OSUrIHgQ')
            context.bot.send_message(chat_id=update.effective_chat.id, text='send me a link or use the commands!')


def run():
    updater = Updater(token=telegram_token, use_context=True)
    updater.start_polling()
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    album_handler = CommandHandler('album', album)
    single_handler = CommandHandler('single', single)
    artist_handler = CommandHandler('artist', artist)
    download1_handler = MessageHandler(Filters.text & (~Filters.command), download)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(album_handler)
    dispatcher.add_handler(single_handler)
    dispatcher.add_handler(artist_handler)
    dispatcher.add_handler(download1_handler)
    print('[TELEGRAM BOT] Listening...')


if __name__ == '__main__':
    run()
