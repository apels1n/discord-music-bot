"""
Discord music bot
Server: Tea (https://discord.gg/ryZ5bVgKqP)
Authors: apels1n (https://github.com/apels1n)
Version: 1.3
"""
from asyncio import sleep
from urls import *
from embed_message import *
from AudioStream import AudioStream
from discord.ext import commands


TOKEN = open("TOKEN", "r", encoding='utf-8').read()
bot = commands.Bot(command_prefix='!')
queue_list = []


@bot.command()
async def play(ctx, arg):
    global vc
    if validateUrl(arg):
        __url = getValidatedUrl()
        queue_list.append(__url)
        """Удаляем сообщение с командой"""
        await ctx.message.delete()
        await QueueAdded(ctx, __url)
        await connect(ctx)
    else:
        await ctx.reply("Хибне посилання")
        return

    if not vc.is_playing() and not vc.is_paused():
        for i in queue_list:
            await newTrackPlay(ctx, i)
            while vc.is_playing() or vc.is_paused():
                await sleep(1)
        if not vc.is_paused():
            queue_list.clear()
            await ctx.send("Кінець черги")
            await sleep(1)
            await vc.disconnect()


@bot.command()
async def pause(ctx):
    """
    Resume func
    Функция приостанавливает воспроизведение.
    Функция проверяет находиться ли пользователь
    в том же голосовом канале что и бот и если канал не совпадает
    функция уведомляет пользователя
    """
    if ctx.voice_client.channel == ctx.message.author.voice.channel:
        vc.pause()
        await ctx.message.delete()
        await ctx.send("Paused")
    else:
        await ConnectToOperate(ctx)


@bot.command()
async def resume(ctx):
    """
    Resume func
    Функция возобновляет воспроизведение.
    Функция проверяет находиться ли пользователь
    в том же голосовом канале что и бот и если канал не совпадает
    функция уведомляет пользователя
    """
    if ctx.voice_client.channel == ctx.message.author.voice.channel:
        vc.resume()
        await ctx.message.delete()
        await ctx.send("Resumed")
    else:
        await ConnectToOperate(ctx)


@bot.command()
async def stop(ctx):
    """
    Stop func
    Функция очищяет очередь и отключает бота от голосового
    канала. Функция проверяет находиться ли пользователь
    в том же голосовом канале что и бот и если канал не совпадает
    функция уведомляет пользователя
    """
    """Защита от "случайного" отключения бота"""

    if ctx.voice_client.channel == ctx.message.author.voice.channel:
        queue_list.clear()
        await vc.disconnect()
        await ctx.message.delete()
    else:
        await ConnectToOperate(ctx)


@bot.command()
async def skip(ctx):
    """
        skip func
        Функция переключения трека. Функция проверяет находиться ли
        пользователь в том же голосовом канале что и бот и если канал не
        совпадает функция уведомляет пользователя
    """
    """Защита от "случайного" отключения бота"""
    try:
        if ctx.voice_client.channel == ctx.message.author.voice.channel:
            vc.stop()
            #await newTrackPlay(ctx)
        else:
            await ConnectToOperate(ctx)
    except:
        return


@bot.command()
async def clear(ctx):
    """
        clear func
        Функция очищяет очередь Функция проверяет находиться ли пользователь
        в том же голосовом канале что и бот и если канал не совпадает
        функция уведомляет пользователя
        """
    """Защита от "случайной" очистки очереди"""
    if ctx.voice_client.channel == ctx.message.author.voice.channel:
        queue_list.clear()
        await ctx.reply("Черга очищена")
    else:
        await ConnectToOperate(ctx)


"""Обработчики сокращённых комманд"""
"""Play command"""
@bot.command()
async def go(ctx, arg):
    await play(ctx, arg)


"""Pause command"""
@bot.command()
async def p(ctx):
    await pause(ctx)


"""Resume command"""
@bot.command()
async def r(ctx):
    await resume(ctx)


"""Stop command"""
@bot.command()
async def s(ctx):
    await stop(ctx)


"""Skip command"""
@bot.command()
async def n(ctx):
    await skip(ctx)


"""Clear command"""
async def c(ctx):
    await clear(ctx)


"""Служебные функции"""
async def newTrackPlay(ctx, track):
    vc.stop()
    parser = Parser(track)
    url = parser.getUrl()
    title = parser.getTitle()
    thumbnail = parser.getThumbnail()
    stream = AudioStream(parser.getStream())

    """Отправляем сообщение с играющим треком"""
    await SendEmbed(ctx, thumbnail, title, url)
    """Начинаем воспроизведение"""
    vc.play(stream.getAudio())


async def connect(ctx):
    global vc

    """Подключаемся в голосовой канал"""
    """Проверяем находится ли пользователь в голосовом канале"""
    if not ctx.message.author.voice:
        await NotInChannelError(ctx)

    """Если канал бота и пользователя не совпадают то говорим об этом"""
    if ctx.guild.voice_client is not None and ctx.message.author.voice \
            is not None:
        if not ctx.voice_client.channel == ctx.message.author.voice.channel:
            await CurrentChannelError(ctx)

    """Проверяем находиться ли бот в голосовом канале"""
    if not ctx.guild.voice_client:
        channel = ctx.message.author.voice.channel
        vc = await channel.connect()
        await ctx.guild.change_voice_state(
            channel=channel,
            self_deaf=True)


def main():
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
