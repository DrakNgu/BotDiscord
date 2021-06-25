
import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
from time import sleep
import asyncio
import sys
import yaml
 
youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""
    @classmethod

    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

class music(commands.Cog, name="music"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='join')
    async def join(self,ctx):
        """
        Faire rejoindre le bot dans le channel
        Bot join the channel
        """
    
        if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()

    @commands.command(name='leave')
    async def leave(self,ctx):
        """
        Quite le channel 
        Bot leave the channel
        """
        voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice_client != None:
            await voice_client.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")

    @commands.command(name='play')
    async def play(self,ctx,url):
        """
        Joue une musique
        Play a song
        """
        try :
            server = ctx.message.guild
            voice_channel = server.voice_client
            async with ctx.typing():
                filename = await YTDLSource.from_url(url)
                print("test")
                voice_channel.play(discord.FFmpegPCMAudio(source=filename))
                print("test")
            await ctx.send('**Now playing:** {}'.format(filename))
        except:
            await ctx.send("The bot is not connected to a voice channel.")

    @commands.command(name='pause')
    async def pause(self,ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command(name='resume', help='Resumes the song')
    async def resume(self,ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
        else:
            await ctx.send("The bot was not playing anything before this. Use play_song command")
    

def setup(bot):
    bot.add_cog(music(bot))


        
 



