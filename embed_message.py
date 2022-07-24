import discord
from parser import Parser


async def SendEmbed(ctx, thumb, title, url):
    __embed = discord.Embed(
        title="Зараз грає:",
        color=0xFF0000,
    )
    #Очищяем поля эмбеда
    __embed.clear_fields()
    #Установливаем картинку эмбеда из видео
    __embed.set_thumbnail(url=f"{thumb}")
    #Добавляем название и ссылку
    __embed.add_field(
            name=f"{title}",
            value=f"{url}",
            inline=False,
        )
    #Отпрявляем эмбед в чат
    await ctx.send(embed=__embed)


async def NotInChannelError(ctx):
        await ctx.reply(f"{ctx.message.author.mention},\x20"
                        f"Увійди у голосову кімнату")


async def ConnectToOperate(ctx):
        await ctx.reply(f"{ctx.message.author.mention},\x20"
                        f"Щоб керувати мною, тобі потрібно бути у тій\x20"
                        f"голосовій кімнаті, в якій я знаходжусь")


async def CurrentChannelError(ctx):
        await ctx.reply(f"{ctx.message.author.mention},\x20"
                        f"Зараз я знаходжусь в іншому каналі")


async def QueueAdded(ctx, url):
        parser = Parser(url)
        title = parser.getTitle()
        thumbnail = parser.getThumbnail()
        __embed1 = discord.Embed(
            title="Додано в чергу:",
            color=0x007eff,
        )
        # Очищяем поля эмбеда
        __embed1.clear_fields()
        # Установливаем картинку эмбеда из видео
        __embed1.set_thumbnail(url=f"{thumbnail}")
        # Добавляем название и ссылку
        __embed1.add_field(
            name=f"{title}",
            value=f"{url}",
            inline=False,
        )
        # Отпрявляем эмбед в чат
        await ctx.send(embed=__embed1)


async def helpMsg(ctx):
    with open("help.txt", "r") as file:
        __embed = discord.Embed(
            title="Помічник:",
            color=0xfcdb03,
        )
        # Очищяем поля эмбеда
        __embed.clear_fields()
        # Добавляем название и ссылку
        __embed.add_field(
            value=f"{file.read()}",
            inline=False,
        )
        # Отпрявляем эмбед в чат
        await ctx.send(embed=__embed)