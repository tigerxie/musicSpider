# import urllib.request
import re
import requests
import json
from bs4 import BeautifulSoup 
from Logger import Log
default_timeout = 100 

class NetEase:
    def __init__(self):
        self.header = {
            'Accept': '*/*',
            'Accept-Encoding': 'deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/search/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
        }

    def search(self, s, stype=1, offset=0, total='true', limit=100):
        action = 'http://music.163.com/api/search/get/web'
        data = {
            's': s,
            'type': stype,
            'offset': offset,
            'total': total,
            'limit': limit
        }
        return self.httpRequest('POST', action, data)
    
    # song ids --> song urls ( details )
    def songs_detail(self, ids, offset=0):
        tmpids = ids[offset:]
        tmpids = tmpids[0:100]
        tmpids = map(str, tmpids)
        action = 'http://music.163.com/api/song/detail?ids=[' + (',').join(tmpids) + ']'
        try:
            data = self.httpRequest('GET', action)
            return data['songs']
        except:
            return []

    def httpRequest(self, method, action, query=None, urlencoded=None, callback=None, timeout=None):    
        if(method == 'GET'):
            url = action if (query == None) else (action + '?' + query)
            connection = requests.get(url, headers=self.header, timeout=default_timeout)

        elif(method == 'POST'):
            connection = requests.post(
                action,
                data=query,
                headers=self.header,
                timeout=default_timeout
            )

        connection.encoding = "UTF-8"
        print ("------")
        print(connection.text)
        log.info(connection.text)
        connection = json.loads(connection.text)
        return connection

###############################################################################
log = Log.getLogger('MusicSpider')
netEase = NetEase()
limit = 100
musics = netEase.search("imagine",stype=1)
log.info(musics)

song_ids = []
if 'songs' in musics['result']:
    if 'mp3Url' in musics['result']['songs']:
        songs = musics['result']['songs']
        log.info(songs)
        
    # if search song result do not has mp3Url
    # send ids to get mp3Url
    else:
        for i in range(0, len(musics['result']['songs']) ):
            song_ids.append( musics['result']['songs'][i]['id'] )
        songs = netEase.songs_detail(song_ids)
        log.info(songs)
