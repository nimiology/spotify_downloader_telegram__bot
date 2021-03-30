from __future__ import unicode_literals
from youtube_search import YoutubeSearch
import youtube_dl
from valuetotxt import read
import tag


def search(NAME,TIME1,TIME2,TIME3,TIME4):
    song_name_final = NAME.replace(" ", "+")
    pre_url = "https://www.youtube.com/results?search_query="
    yt_search = pre_url + song_name_final
    print(yt_search)
    results = list(YoutubeSearch(str(NAME)).to_dict())
    for URLSSS in results:
        timeyt = URLSSS["duration"]
        print(URLSSS['title'])
        try:
            if timeyt == TIME1:
                LINKASLI = URLSSS['url_suffix']
                break
            elif timeyt == TIME2:
                LINKASLI = URLSSS['url_suffix']
                break
            elif timeyt == TIME3:
                LINKASLI = URLSSS['url_suffix']
                break
            elif timeyt == TIME4:
                LINKASLI = URLSSS['url_suffix']
                break
            else:
                pass
        except:
            pass

    yt_pre = str("https://www.youtube.com/" + LINKASLI)
    print(yt_pre)

    options = {
        # PERMANENT options
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': f'song//{read(3)}.*',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320'
        }],

        # (OPTIONAL options)
        'noplaylist': True
    }

    with youtube_dl.YoutubeDL(options) as mp3:
        mp3.download([yt_pre])
        tag.tag()
