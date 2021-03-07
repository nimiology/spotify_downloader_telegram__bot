import youtube
from detail import Detail
import telepot
import time
import tag
import detail


token = 'your token'
bot = telepot.Bot(token)

sort = {}
def START(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    bot.sendMessage(-1001427071315,chat_id)
    def DOWNLOADER(lenk):
        DETAIL = Detail(lenk)
        youtube.search(DETAIL.song_name, DETAIL.time_duration,
                       DETAIL.time_duration1, DETAIL.minutes,
                       DETAIL.seconds)
        youtube.Download(lenk)

    def sendtrack(link):
        DOWNLOADER(link)
        bot.sendAudio(-1001316788330, open(f'song//{Detail(link).song_name_folder}.mp3', 'rb'),
                      title=Detail(link).trackname)
        bot.sendAudio(chat_id, open(f'song//{Detail(link).song_name_folder}.mp3', 'rb'), title=Detail(link).trackname)

    def send(link):
        DOWNLOADER(link)
        bot.sendAudio(chat_id, open(f'song//{Detail(link).song_name_folder}.mp3', 'rb'),
                      title=Detail(link).trackname)
        bot.sendAudio(-1001316788330, open(f'song//{Detail(link).song_name_folder}.mp3', 'rb'),
                      title=Detail(link).trackname)

    def albumdownload(link):
        messagealbum = ""
        for song in Detail.album(link):
            messagealbum += song['name'] + " :\n " + song['external_urls']['spotify'] + '\n'
        bot.sendMessage(chat_id, messagealbum)
        for album in Detail.album(link):
            try:
                send(album['id'])
            except:
                bot.sendMessage(chat_id, "somthing went wrong")



    msg = msg['text']



    if content_type == 'text':

        if msg[:30]==('https://open.spotify.com/album') :
            albumdownload(msg)

        elif msg[:30]== ('https://open.spotify.com/track')  :
            try:
                sendtrack(msg)
            except:
                bot.sendMessage(chat_id, "somthing went wrong")

        elif msg[:31] == ('https://open.spotify.com/artist'):
            messagealbum= ""
            for song in detail.artist(msg):
                messagealbum += song['name']+" :\n "+song['external_urls']['spotify']+'\n\n'
            bot.sendMessage(chat_id,messagealbum)
            for song in detail.artist(msg):
                try:
                    send(song['href'])
                except:
                    bot.sendMessage(chat_id,"somthing went wrong")

        elif msg == "/start":
            bot.sendMessage(chat_id,
                            "Hi \nsend me spotify link and I'll give you music\nor use /single or /album")

        elif msg == "/album":
            sort[chat_id]='a'
            bot.sendMessage(chat_id, 'send name and name of artist like this \nAlbum - Name artist')

        elif msg == '/single':
            sort[chat_id]='single'
            bot.sendMessage(chat_id,'send name and name of artist like this \nName - Name artist')

        elif msg.find("-")>0:
            print(sort)
            if sort[chat_id]=='album':
                albumdownload(detail.searchalbum(msg))
                del sort[chat_id]
            elif sort[chat_id]=='single':
                send(detail.searchsingle(msg))
                del sort[chat_id]

            else :
                bot.sendMessage(chat_id,"You didn't sort it")

        else:
            bot.sendMessage(chat_id,'send me link or use /single or /album')

bot.message_loop(START)
print('Listening ...')

while 1:
    time.sleep(10)

