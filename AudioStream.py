from discord import FFmpegPCMAudio


FFMPEG_PATH = "ffmpeg.exe"  # Path to FFMPEG

FFMPEG_OPTIONS = {
    'before_options':
        '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}


class AudioStream:
    def __init__(self, url):
        self.__stream = FFmpegPCMAudio(
            executable=FFMPEG_PATH,
            source=url,
            **FFMPEG_OPTIONS
        )


    def getAudio(self):
        return self.__stream