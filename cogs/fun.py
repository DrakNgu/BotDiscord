import asyncio
import os
import sys

import discord
import yaml
import discord,requests
import random
from discord.ext import commands
from bs4 import BeautifulSoup


if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found! Please add it and try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)


class Fun(commands.Cog, name="fun"):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="rps")
    async def rock_paper_scissors(self, context):
        """
        Faite une petite partie de pierre Feuille ciseau avec GadgetBot
        Wanna play against GadgetBot at Rock paper scissors
        """
        choices = {
            0: "rock",
            1: "paper",
            2: "scissors"
        }
        reactions = {
            "🪨": 0,
            "🧻": 1,
            "✂": 2
        }
        embed = discord.Embed(title="Faite votre choix", color=config["warning"])
        embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
        choose_message = await context.send(embed=embed)
        for emoji in reactions:
            await choose_message.add_reaction(emoji)

        def check(reaction, user):
            return user == context.message.author and str(reaction) in reactions

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=10, check=check)

            user_choice_emote = reaction.emoji
            user_choice_index = reactions[user_choice_emote]

            bot_choice_emote = random.choice(list(reactions.keys()))
            bot_choice_index = reactions[bot_choice_emote]

            result_embed = discord.Embed(color=config["success"])
            result_embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
            await choose_message.clear_reactions()

            if user_choice_index == bot_choice_index:
                result_embed.description = f"**Egalité**\nJoueur : {user_choice_emote} GadgetBod :  {bot_choice_emote}."
                result_embed.colour = config["warning"]
            elif user_choice_index == 0 and bot_choice_index == 2:
                result_embed.description = f"**Vous avez gagnée!**\nJoueur :  {user_choice_emote} GadgetBot : {bot_choice_emote}."
                result_embed.colour = config["success"]
            elif user_choice_index == 1 and bot_choice_index == 0:
                result_embed.description = f"**Vous avez gagnée!**\nJoueur :  {user_choice_emote} GadgetBot :  {bot_choice_emote}."
                result_embed.colour = config["success"]
            elif user_choice_index == 2 and bot_choice_index == 1:
                result_embed.description = f"**Vous avez gagnée!**\nJoueur :  {user_choice_emote} GadgetBot :  {bot_choice_emote}."
                result_embed.colour = config["success"]
            else:
                result_embed.description = f"**J'ai gagnée**\nJoueur : {user_choice_emote} GadgetBot :  {bot_choice_emote}."
                result_embed.colour = config["error"]
                await choose_message.add_reaction("🇱")
            await choose_message.edit(embed=result_embed)
        except asyncio.exceptions.TimeoutError:
            await choose_message.clear_reactions()
            timeout_embed = discord.Embed(title="Vous avez mis trop de temps pour choisir", color=config["error"])
            timeout_embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
            await choose_message.edit(embed=timeout_embed)
            
    @commands.command()
    async def cat(self,ctx):
        """
        Affichez un P'otit chat trop mimi
        Display cat
        """
        r = requests.get("https://api.thecatapi.com/v1/images/search").json()
        cat_embed = discord.Embed()
        cat_embed.set_image(url=f"{r[0]['url']}")
        await ctx.send(embed=cat_embed)
        
    @commands.command()
    async def dog(self,ctx):
        """
        Affichez un P'otit chien  (Objectivement mieux que les chats)
        Display a random dog
        """
        r = requests.get("https://api.thedogapi.com/v1/images/search").json()
        dog_embed = discord.Embed()
        dog_embed.set_image(url=f"{r[0]['url']}")
        await ctx.send(embed=dog_embed)
        
    @commands.command()
    async def cert(self,ctx):
        """
        Quelques petites infos cyber car c'est quand même le but de la formation
        Display cert last info
        """
        r = requests.get("https://www.cert.ssi.gouv.fr")
        soup = BeautifulSoup(r.content, 'html.parser')
        all_div = [div for div in soup.find_all("div", {"class": "item cert-alert open"},"\n")]
        for i in  all_div:
            for n in i.text.split("\n"):
                if n:
                    await ctx.send(n)
        await ctx.send("https://www.cert.ssi.gouv.fr")
                    

            

def setup(bot):
    bot.add_cog(Fun(bot))
