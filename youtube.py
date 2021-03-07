from __future__ import unicode_literals
from youtube_search import YoutubeSearch
import youtube_dl
from detail import Detail
import os
import tag


def search(NAME,TIME,TIME2,minuts,seconds):
    song_name_final = NAME.replace(" ", "+")
    pre_url = "https://www.youtube.com/results?search_query="
    yt_search = pre_url + song_name_final
    print(yt_search)
    results = list(YoutubeSearch(str(NAME)).to_dict())
    minuts += 1
    for URLSSS in results:
        try:
            timeyt = URLSSS["duration"]
            #Myoutube = timeyt[timeyt.find(':')+1:]
            #Syoutube = timeyt[:timeyt.find(':')]
            #Myoutube=int(Myoutube)
            #Syoutube = int(Syoutube)
            if timeyt == TIME:
                LINKASLI = URLSSS['url_suffix']
            #elif seconds+30>=Syoutube and Myoutube==minuts:
                #LINKASLI = results[URLSSS]['url_suffix']
            elif timeyt == TIME2:
                LINKASLI = URLSSS['url_suffix']
            else:
                pass
        except:
            pass
    global yt_pre
    yt_pre = str("https://www.youtube.com/" + LINKASLI)
    print(yt_pre)
    print("Starting download...")

def Download(lenk):
    DETAIL = Detail(lenk)
    options = {
        # PERMANENT options
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': f'song//{DETAIL.song_name_folder}.*',
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
        tag.tag(lenk, DETAIL.song_name_folder)
        print("Download Completed!")
