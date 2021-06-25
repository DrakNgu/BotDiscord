import json
import os
import random
import sys
import requests

import aiohttp
import discord
import yaml
from discord.ext import commands

if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found! Please add it and try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)


class general(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info", aliases=["botinfo"])
    async def info(self, ctx):
        """
        Des informations utile (ou pas) sur le serveur
        Get some useful (or not) information about the server.
        """
        server = ctx.guild
        nbChatChan = len(server.text_channels)
        nbVoiceChan = len(server.voice_channels)
        serverDesc = server.description
        nbPerson = server.member_count
        serverName = server.name
        message = f"Le serveur **{serverName}** contient **{nbPerson}** personnes.\nLa description du serveur est : **{serverDesc}**\nCe serveur possède **{nbChatChan}** chats et **{nbVoiceChan}** salon vocal "
        await ctx.send(message)
    

    @commands.command(name="serverinfo")
    async def serverinfo(self, context):
        """
        Des informations utile (ou pas) sur le serveur (plus que la commande info)
        Get some useful (or not) information about the server (more than info).
        """
        server = context.message.guild
        roles = [x.name for x in server.roles]
        role_length = len(roles)
        if role_length > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)
        channels = len(server.channels)
        time = str(server.created_at)
        time = time.split(" ")
        time = time[0]

        embed = discord.Embed(
            title="**Server Name:**",
            description=f"{server}",
            color=config["success"]
        )
        embed.set_thumbnail(
            url=server.icon_url
        )
        if(server.owner != None):
            embed.add_field(
                name="Owner",
                value=f"{server.owner}\n{server.owner.id}"
        )
    
        embed.add_field(
            name="Server ID",
            value=server.id
        )
        embed.add_field(
            name="Member Count",
            value=server.member_count
        )
        embed.add_field(
            name="Text/Voice Channels",
            value=f"{channels}"
        )
        embed.add_field(
            name=f"Roles ({role_length})",
            value=roles
        )
        embed.set_footer(
            text=f"Created at: {time}"
        )
        await context.send(embed=embed)

    @commands.command(name="ping")
    async def ping(self, context):
        """
        Regardez si le bot est encore en vie
        Check if the bot is alive.
        """
        embed = discord.Embed(
            color=config["success"]
        )
        embed.add_field(
            name="Pong!",
            value=":ping_pong:",
            inline=True
        )
        embed.set_footer(
            text=f"Pong request by {context.message.author}"
        )
        await context.send(embed=embed)

    @commands.command(name="invite")
    async def invite(self, context):
        """
        Recevoir le liens pour invitez le bot sur son serveur
        Get the invite link of the bot to be able to invite it.
        """
        await context.send("I sent you a private message!")
        application_id = config["application_id"]
        await context.author.send(f"Invite me by clicking here: https://discordapp.com/oauth2/authorize?&client_id={application_id}&scope=bot&permissions=8")


    @commands.command(name="poll")
    async def poll(self, context, *args):
        """
        Crée un sondage
        Create a poll where members can vote.
        """
        poll_title = " ".join(args)
        embed = discord.Embed(
            title="A new poll has been created!",
            description=f"{poll_title}",
            color=config["success"]
        )
        embed.set_footer(
            text=f"Poll created by: {context.message.author} • React to vote!"
        )
        embed_message = await context.send(embed=embed)
        await embed_message.add_reaction("👍")
        await embed_message.add_reaction("👎")
        await embed_message.add_reaction("🤷")

    @commands.command(name="8ball")
    async def eight_ball(self, context, *args):
        """
        Posez un question au bot
        Ask any question to the bot.
        """
        answers = ['It is certain.', 'It is decidedly so.', 'You may rely on it.', 'Without a doubt.',
                   'Yes - definitely.', 'As I see, yes.', 'Most likely.', 'Outlook good.', 'Yes.',
                   'Signs point to yes.', 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.',
                   'Cannot predict now.', 'Concentrate and ask again later.', 'Don\'t count on it.', 'My reply is no.',
                   'My sources say no.', 'Outlook not so good.', 'Very doubtful.']
        embed = discord.Embed(
            title="**My Answer:**",
            description=f"{answers[random.randint(0, len(answers))]}",
            color=config["success"]
        )
        embed.set_footer(
            text=f"Question asked by: {context.message.author}"
        )
        await context.send(embed=embed)

    @commands.command(name="bitcoin")
    async def bitcoin(self, context):
        """
        Afficher le prix actuel du bitcoin en dollar
        Get the current price of bitcoin.
        """
        url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
        # Async HTTP request
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            responseUSD = await raw_response.text()
            responseUSD = json.loads(responseUSD)
            responsefr = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
            datafr = responsefr.json()
            embedUSD = discord.Embed(
                title=":information_source: Info",
                description=f"Bitcoin price is: $ {responseUSD['bpi']['USD']['rate']}",
                color=config["success"]
            )
            embedfr = discord.Embed(
                title=":information_source: Info",
                description=f"Le prix du Bitcoin est: {datafr['bpi']['EUR']['rate']} €",
                color=config["success"]
            )
            await context.send(embed=embedfr)
            await context.send(embed=embedUSD)


def setup(bot):
    bot.add_cog(general(bot))
