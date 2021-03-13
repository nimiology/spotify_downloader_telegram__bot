import youtube
from spotify import Detail
import telepot
import spotify
import valuetotxt
import requests

token = 'token bot father'

bot = telepot.Bot(token)

sort = {}
def cantfind(chat_id):
    bot.sendSticker(chat_id, 'CAACAgQAAxkBAAIBE2BLNclvKLFHC-grzNdOEXKGl6cLAALzAAMSp2oDSBk1Yo7wCGUeBA')
    bot.sendMessage(chat_id, "can't find it")

def cantfindone(chat_id):
    bot.sendSticker(chat_id, 'CAACAgQAAxkBAAIFSWBF_m3GHUtZJxQzobvD_iWxYVClAAJuAgACh4hSOhXuVi2-7-xQHgQ')
    bot.sendMessage(chat_id, "can't download one of them")


def send(link,chat_id):
    DETAIL = Detail(link)
    song_name_folder = valuetotxt.read(3)
    trackname = valuetotxt.read(3)
    song_name = valuetotxt.read(2)
    try:
        bot.sendAudio(chat_id, open(f'song//{song_name_folder}.mp3', 'rb'),
                      title=trackname)
    except:
        youtube.search(song_name, valuetotxt.read(5),
                       valuetotxt.read(6), valuetotxt.read(10),
                       valuetotxt.read(11))
        bot.sendAudio(chat_id, open(f'song//{song_name_folder}.mp3', 'rb'),
                      title=trackname)


def albumdownload(link,chat_id):
    messagealbum = ""
    for song in spotify.album(link):
        messagealbum += song['name'] + " :\n " + song['external_urls']['spotify'] + '\n'
    bot.sendMessage(chat_id, messagealbum)

    for album in spotify.album(link):
        try:
            send(album['id'],chat_id)
        except:
            cantfindone(chat_id)


def artist(artistlink,chat_id):
    messagealbum = ""
    for song in spotify.artist(artistlink):
        messagealbum += song['name'] + " :\n " + song['external_urls']['spotify'] + '\n\n'
    bot.sendMessage(chat_id, messagealbum)
    for song in spotify.artist(artistlink):
        try:
            send(song['href'],chat_id)
        except:
            cantfindone(chat_id)


def START(msg,chat_id):
    try:
        print(msg)

        if msg[:30]==('https://open.spotify.com/album') :
            albumdownload(msg,chat_id)

        elif msg[:30]== ('https://open.spotify.com/track')  :
            try:
                send(msg,chat_id)
            except:
                bot.sendSticker(chat_id, somthing_went_wrong)
                bot.sendMessage(chat_id, "can't download music")

        elif msg[:31] == ('https://open.spotify.com/artist'):
                artist(msg,chat_id)

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
                        artist(spotify.searchartist(msg),chat_id)
                        del sort[chat_id]
                    except:
                        cantfind(chat_id)
                elif sort[chat_id]=='album':
                    try:
                        albumdownload(spotify.searchalbum(msg),chat_id)
                        del sort[chat_id]
                    except:
                        cantfind(chat_id)
                elif sort[chat_id]=='single':
                    try:
                        send(spotify.searchsingle(msg),chat_id)
                        del sort[chat_id]
                    except:
                        cantfind(chat_id)
            except:
                bot.sendSticker(chat_id, 'CAACAgQAAxkBAAIBFGBLNcpfFcTLxnn5lR20ZbE2EJbrAAJRAQACEqdqA2XZDc7OSUrIHgQ')
                bot.sendMessage(chat_id,'send me link or use /single or /album or /artist')
    except :
        pass


print('Listening ...')




tokenurl = f'https://api.telegram.org/bot{token}'
Update = tokenurl+"/getUpdates"


def UPDATE():
    MESSAGES = requests.get(Update).json()
    return MESSAGES['result']


while 1:
    try:
        for message in UPDATE():
            offset = message['update_id']+1
            offset = Update+f"?offset={offset}"
            offset = requests.post(offset)
            msg = message['message']['text']
            chat_id = message['message']['from']['id']
            START(msg,chat_id)
    except:
        pass



