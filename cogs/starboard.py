import discord
from discord.ext import commands, bridge
import asyncio
import random
import json

class starboard(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @bridge.bridge_command(description="Enable or disable starboard")
    @commands.has_permissions(administrator = True)
    async def serverlogs(self, ctx):
        with open("starboard.json") as f:
            automodguild = json.load(f)

        if ctx.guild.id not in automodguild:
            automodguild.append(ctx.guild.id)
            await ctx.respond("Enabled starboard, saving settings...")
            overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel = True, send_messages=False)
            }
            channel = await ctx.guild.create_text_channel(f'⭐starboard', overwrites = overwrites, reason = f"StarBoard")         
        elif ctx.guild.id in automodguild:
            automodguild.remove(ctx.guild.id)
            await ctx.respond("Disabled starboard, saving settings...")

        with open("starboard.json", "w+") as f:
            json.dump(automodguild, f)

        await ctx.respond("Settings saved!")


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        exists = False
        if reaction.emoji != "⭐":
            return
        with open("starboard.json") as f:
            automodguild = json.load(f)
        if reaction.guild.id not in automodguild:
            return
        for channel in reaction.guild.channels:
            if str(channel.name) == "⭐starboard":
                embed = discord.Embed(title="Starred image", description=f"By {reaction.message.author}")
                embed.set_image(url=reaction.message.attatchments[0].url)
                await channel.send(embed=embed)
                

        

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(starboard(bot)) # add the cog to the bot