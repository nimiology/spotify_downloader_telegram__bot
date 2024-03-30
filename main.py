import spotify
from consts import WELCOME_MESSAGE, ALBUM_MESSAGE, ARTISTS_MESSAGE, SINGLE_MESSAGE, NOT_FOUND_STICKER



async def start(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=WELCOME_MESSAGE)


async def album(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=ALBUM_MESSAGE)


async def artist(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=ARTISTS_MESSAGE)


async def single(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=SINGLE_MESSAGE)


async def download(update: Update, context: CallbackContext):
    msg = update.message.text
    msg_link = text_finder(msg)
    if msg_link.startswith('https://open.spotify.com/album'):
        await downloader(update, context, msg, 'AL')
    elif msg_link.startswith('https://open.spotify.com/track'):
        await download_song(update, context, msg_link)
    elif msg.startswith('https://open.spotify.com/playlist'):
        await downloader(update, context, msg, 'PL')
    elif msg_link.startswith('https://open.spotify.com/artist'):
        await downloader(update, context, msg, 'AR')
    else:
        await handle_search_message(update, context, msg)


def text_finder(txt):
    index = txt.find("https://open.spotify.com")
    if index != -1:
        return txt[index:]
    return ''


async def handle_search_message(update: Update, context: CallbackContext, msg: str):
    chat_id = update.effective_chat.id
    if chat_id in sort:
        sort_type = sort.pop(chat_id)
        if sort_type == 'artist':
            await downloader(update, context, spotify.search_artist(msg), 'AR')
        elif sort_type == 'album':
            await downloader(update, context, spotify.search_album(msg), 'AL')
        elif sort_type == 'single':
            await download_song(update, context, spotify.search_single(msg))
    else:
        await send_help_message(update, context)


async def send_help_message(update: Update, context: CallbackContext):
    await context.bot.send_sticker(chat_id=update.effective_chat.id,
                                   sticker=NOT_FOUND_STICKER)
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Send me a link or use the commands!')


async def downloader(update: Update, context: CallbackContext, link: str, type: str):
    if type == 'AL':
        items = spotify.album(link)
    elif type == 'AR':
        items = spotify.artist(link)
    elif type == 'PL':
        items = spotify.playlist(link)
    else:
        items = []

    message = ""
    count = 0
    for song in items:
        if type == 'PL':
            song = song['track']
        count += 1
        message += f"{count}. {song['name']}\n"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    for song in items:
        if type == 'PL':
            song = song['track']
        await download_song(update, context, song['href'])


async def download_song(update: Update, context: CallbackContext, link: str):
    song = spotify.Song(link)
    song.yt_link()
    try:
        song.yt_download()
        song.song_meta_data()
        caption = f'Track: {song.trackName}\nAlbum: {song.album}\nArtist: {song.artist}'
        await context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(f'{song.trackName}.mp3', 'rb'),
                                     caption=caption, title=song.trackName)
    except:
        await context.bot.send_sticker(chat_id=update.effective_chat.id,
                                       sticker=NOT_FOUND_STICKER)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'404\n"{song.trackName}" Not Found')


sort = {}


def run():
    application = ApplicationBuilder().token(telegram_token).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('album', album))
    application.add_handler(CommandHandler('single', single))
    application.add_handler(CommandHandler('artist', artist))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download))
    print('[TELEGRAM BOT] Listening...')
    application.run_polling()


if __name__ == '__main__':
    run()
