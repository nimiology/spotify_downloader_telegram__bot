from spotify import DOWNLOADMP3 as SONGDOWNLOADER
import telepot
import spotify
import requests
import threading
import os

token = os.environ.get('BOT_TOKEN')
bot = telepot.Bot(token)

sort = {}


def txtfinder(txt):
    a = txt.find("https://open.spotify.com")
    txt = txt[a:]
    return txt

def cantfind(chat_id):
    bot.sendSticker(chat_id, 'CAACAgQAAxkBAAIBE2BLNclvKLFHC-grzNdOEXKGl6cLAALzAAMSp2oDSBk1Yo7wCGUeBA')
    bot.sendMessage(chat_id, "can't find it")

def cantfindone(chat_id):
    bot.sendSticker(chat_id, 'CAACAgQAAxkBAAIFSWBF_m3GHUtZJxQzobvD_iWxYVClAAJuAgACh4hSOhXuVi2-7-xQHgQ')
    bot.sendMessage(chat_id, "can't download one of them")

def downloader(link,chat_id,type):
    PLAYLIST = False
    if type=='AL':
        ITEMS = spotify.album(link)
    elif type == 'AR':
        ITEMS = spotify.artist(link)
    elif type == 'PL':
        ITEMS = spotify.playlist(link)
        PLAYLIST = True
    else:
        ITEMS = []

    MESSAGE = ""
    for song in ITEMS:
        if PLAYLIST:
            song = song['track']
        MESSAGE += song['name'] + " :\n " + song['external_urls']['spotify'] + '\n\n'
    bot.sendMessage(chat_id, MESSAGE)
    for song in ITEMS:
        if PLAYLIST:
            song = song['track']

        try:
            SONGDOWNLOADER(song['href'], chat_id)
        except:
            cantfindone(chat_id)


def START(msg,chat_id):
    print(f"{chat_id}:{msg}")
    msglink = txtfinder(msg)
    if msglink[:30]==('https://open.spotify.com/album') :
        downloader(msg,chat_id,'AL')

    elif msglink[:30]== ('https://open.spotify.com/track')  :
        try:
            SONGDOWNLOADER(msg, chat_id)
        except:
            bot.sendSticker(chat_id,
                            'CAACAgQAAxkBAAIFSWBF_m3GHUtZJxQzobvD_iWxYVClAAJuAgACh4hSOhXuVi2-7-xQHgQ')
            bot.sendMessage(chat_id, "can't download music")

    elif msg[:33] == 'https://open.spotify.com/playlist':
        downloader(msg,chat_id,'PL')

    elif msglink[:31] == ('https://open.spotify.com/artist'):
            downloader(msg,chat_id,'AR')

    elif msg == "/start":
        bot.sendMessage(chat_id,
                        "Hi \nsend me spotify link and I'll give you music\nor use /single or /album or "
                        "/artist")

    elif msg == "/album":
        sort[chat_id]='album'
        bot.sendMessage(chat_id, 'send name and name of artist like this: \nName album\nor for better search use this:\nName album - Name artist')

    elif msg == '/single':
        sort[chat_id]='single'
        bot.sendMessage(chat_id,'send name and name of artist like this: \nName song\nor for better search use this:\nName song - Name artist')
    elif msg == '/artist':
        sort[chat_id]='artist'
        bot.sendMessage(chat_id,'send name and name of artist like this: \nName artist')

    else:
        try:
            if sort[chat_id]=='artist':
                try:
                    downloader(spotify.searchartist(msg),chat_id,'AR')
                    del sort[chat_id]
                except:
                    cantfind(chat_id)
            elif sort[chat_id]=='album':
                try:
                    downloader(spotify.searchalbum(msg),chat_id,'AL')
                    del sort[chat_id]
                except:
                    cantfind(chat_id)
            elif sort[chat_id]=='single':
                try:
                    SONGDOWNLOADER(spotify.searchsingle(msg), chat_id)
                    del sort[chat_id]
                except:
                    cantfind(chat_id)
        except:
            bot.sendSticker(chat_id, 'CAACAgQAAxkBAAIBFGBLNcpfFcTLxnn5lR20ZbE2EJbrAAJRAQACEqdqA2XZDc7OSUrIHgQ')
            bot.sendMessage(chat_id,'send me link or use /single or /album or /artist')


print('Listening ...')




tokenurl = f'https://api.telegram.org/bot{token}'
Update = tokenurl+"/getUpdates"


def UPDATE():
    MESSAGES = requests.get(Update).json()
    return MESSAGES['result']


while 1:
    if threading.activeCount()-1 < 15:
        try:
            for message in UPDATE():
                offset = message['update_id']+1
                offset = Update+f"?offset={offset}"
                offset = requests.post(offset)
                msg = message['message']['text']
                chat_id = message['message']['from']['id']
                thread = threading.Thread(target=START,args=(msg,chat_id))
                thread.start()
        except:
            pass
