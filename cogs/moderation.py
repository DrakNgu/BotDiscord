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


class moderation(commands.Cog, name="moderation"):
    def __init__(self, commands):
        self.commands = commands
        
    

    @commands.command(name='kick', pass_context=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *args):
        """
        Expulser une personne du serveur
        Kick a user out of the server.
        """
        if member.guild_permissions.administrator:
            embed = discord.Embed(
                title="Error!",
                description="User has Admin permissions.",
                color=config["error"]
            )
            await ctx.send(embed=embed)
        else:
            try:
                reason = " ".join(args)
                await member.kick(reason=reason)
                embed = discord.Embed(
                    title="User Kicked!",
                    description=f"**{member}** was kicked by **{ctx.message.author}**!",
                    color=config["success"]
                )
                embed.add_field(
                    name="Reason:",
                    value=reason
                )
                await ctx.send(embed=embed)
                try:
                    await member.send(
                        f"You were kicked by **{ctx.message.author}**!\nReason: {reason}"
                    )
                except:
                    pass
            except:
                embed = discord.Embed(
                    title="Error!",
                    description="An error occurred while trying to kick the user.",
                    color=config["success"]
                )
                await ctx.message.channel.send(embed=embed)

    @commands.command(name="nick")
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, context, member: discord.Member, *, name: str):
        """
        Change le pseudo d'une personne
        Change the nickname of a user on a server.
        """
        try:
            if name.lower() == "!reset":
                    name = None
                    
            embed = discord.Embed(
                title="Changed Nickname!",
                description=f"**{member}'s** new nickname is **{name}**!",
                color=config["success"]
            )
            await member.edit(nick=name) 
            await context.send(embed=embed)
            
        except:
            embed = discord.Embed(
                title="Error!",
                description="An error occurred while trying to change the nickname of the user.",
                color=config["warning"]
            )
            await context.message.channel.send(embed=embed)

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, context, member: discord.Member, *args):
        """
        Bannir une personne 
        Bans a user from the server.
        """
        try:
            if member.guild_permissions.administrator:
                embed = discord.Embed(
                    title="Error!",
                    description="User has Admin permissions.",
                    color=config["success"]
                )
                await context.send(embed=embed)
            else:
                reason = " ".join(args)
                await member.ban(reason=reason)
                embed = discord.Embed(
                    title="User Banned!",
                    description=f"**{member}** was banned by **{context.message.author}**!",
                    color=config["success"]
                )
                embed.add_field(
                    name="Reason:",
                    value=reason
                )
                await context.send(embed=embed)
                await member.send(f"You were banned by **{context.message.author}**!\nReason: {reason}")
        except:
            embed = discord.Embed(
                title="Error!",
                description="An error occurred while trying to ban the user.",
                color=config["success"]
            )
            await context.send(embed=embed)

    @commands.command(name="warn")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, context, member: discord.Member, *args):
        """
        Donner un avertissement a une personne 
        Warns a user in his private messages.
        """
        reason = " ".join(args)
        embed = discord.Embed(
            title="User Warned!",
            description=f"**{member}** was warned by **{context.message.author}**!",
            color=config["success"]
        )
        embed.add_field(
            name="Reason:",
            value=reason
        )
        await context.send(embed=embed)
        try:
            await member.send(f"You were warned by **{context.message.author}**!\nReason: {reason}")
        except:
            pass

    @commands.command()
    @commands.has_permissions(manage_messages=True, manage_channels=True)
    async def clear(self,ctx, nombre :int = 1):
        """
        Supprimer un nombre de message choisit
        Dell a number of massages you want
        """
        await ctx.channel.purge(limit = nombre + 1) 
        clear = discord.Embed(title=f":negative_squared_cross_mark: Clear !", description =f"**{nombre} messages ont été supprimé !**")
        await ctx.channel.send(embed=clear)


    @commands.command()
    @commands.has_permissions(manage_messages=True, manage_channels=True)
    async def nuke(self,ctx):
        """
        Supprimer tous les messages
        Dell all message of a channel.
        """
        path= os.getcwd()
        id_channel = ctx.channel.id
        posChan = ctx.channel.position
        existing_channel = self.commands.get_channel(id_channel)
        reactions = {
            "✅": 0,
            "❌": 1
        }
        embed = discord.Embed(title=f":boom:** EXPLOSIONNNNN !!! **:boom:",color=discord.Color.gold(), description=f"Voulez vous supprimer tous les messages ?  Veuillez valider en réagissant avec ✅. Sinon réagissez avec ❌")
        file2 = discord.File(path+"/cogs/LocalPicture/KonoSuba.png", filename="image.png")
        embed.set_image(url="attachment://image.png")
        message = await ctx.send(file=file2, embed=embed)
       
        for emoji in reactions:
            await message.add_reaction(emoji)
        
        def checkEmoji(reaction,user):
            return user == ctx.message.author and str(reaction) in reactions
        
        
        try:
            
            reaction, user = await self.commands.wait_for('reaction_add', timeout=5, check=checkEmoji)
            user_choice = reaction.emoji
            if user_choice == "✅":
                await ctx.send("** La suppresion à commencé ! **.")
                if existing_channel:
                    await ctx.send("Suppression de tous les messages")
                    new_chan = await existing_channel.clone(reason="Has been nuked")
                    await existing_channel.delete()
                    await new_chan.edit(position = posChan)
                    nuke = discord.Embed(title=f":boom:**EXPLOSIONNNNN !!!**:boom:",color=discord.Color.gold(), description=f"")
                    file = discord.File(path+"/cogs/LocalPicture/Explosion.gif", filename="image.gif")
                    nuke.set_image(url="attachment://image.gif")
                    await new_chan.send(file=file, embed=nuke)
                
                
                
                else:
                    await ctx.send(f'No channel  was found')
            else:
                await ctx.channel.purge(limit = 1) 
                new_embed = discord.Embed(title=f":sob:**Supression anulée !!!**:sob:",color=discord.Color.blue())
                file3 = discord.File(path+"/cogs/LocalPicture/Fail.png", filename="image.png")
                new_embed.set_image(url="attachment://image.png")
                await ctx.send(file=file3, embed = new_embed)
        except TimeoutError:
            await ctx.channel.purge(limit = 1) 
            new_embed = discord.Embed(title=f":sob:** Supression anulée !!! **:sob:",color=discord.Color.blue())
            file3 = discord.File(path+"/cogs/LocalPicture/Fail.png", filename="image.png")
            new_embed.set_image(url="attachment://image.png")
            await ctx.send(file=file3, embed = new_embed)
        

       
    @clear.error 
    async def new_error(ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send("**Vous n'avez pas les droits nécéssaire**")
            
            

                    

def setup(commands):
    commands.add_cog(moderation(commands))
