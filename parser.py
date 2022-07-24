from yt_dlp import YoutubeDL

YDL_OPTIONS = {
    'cookies': 'coockies.txt',
    'format': 'm4a/bestaudio/best',
    'noplaylist': False,
    'ignoreerrors': True,
    'postprocessors': [
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }
    ]
}

class Parser:
    def __init__(self, url):
        self.__url = url
        with YoutubeDL(YDL_OPTIONS) as ydl:
            self.__info = ydl.extract_info(self.__url, download=False)
            self.__thumbnail = self.__info['thumbnail']
            self.__title = self.__info['title']
            self.__stream = self.__info['url']

    def getThumbnail(self):
        return self.__thumbnail


    def getTitle(self):
        return self.__title


    def getUrl(self):
        return self.__url


    def getStream(self):
        return self.__stream