import os
import sys

import discord
import yaml
from discord.ext import commands

if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found! Please add it and try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
class boutique(commands.Cog, name="boutique"):
    def __init__(self, bot):
        self.bot = bot



def setup(bot):
    bot.add_cog(boutique(bot))
