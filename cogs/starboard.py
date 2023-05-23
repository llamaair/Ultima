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
    async def starboard(self, ctx):
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
        if reaction.emoji != "⭐":
            return

        with open("starboard.json") as f:
            automodguild = json.load(f)

        if user.guild.id not in automodguild:
            return

        if reaction.count > 3:
            starboard_channel = discord.utils.get(user.guild.channels, name="⭐starboard")
            if not starboard_channel:
                overwrites = {
                user.guild.default_role: discord.PermissionOverwrite(view_channel=True, send_messages=False)
                }
                starboard_channel = await user.guild.create_text_channel("⭐starboard", overwrites=overwrites, reason="StarBoard")

            embed = discord.Embed(title="Starred message", description=reaction.message.content)
            embed.set_author(name=reaction.message.author.display_name, icon_url=reaction.message.author.avatar_url)
            embed.add_field(name="Original Message", value=f"[Jump to message]({reaction.message.jump_url})")

            await starboard_channel.send(embed=embed)

                

        

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(starboard(bot)) # add the cog to the bot