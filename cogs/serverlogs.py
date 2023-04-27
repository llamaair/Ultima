import discord
from discord.ext import commands, bridge
import asyncio
import random
import json

class serverlogs(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @bridge.bridge_command(description="Enable or disable serverlogs")
    @commands.has_permissions(administrator = True)
    async def serverlogs(self, ctx):
        with open("loguilds.json") as f:
            automodguild = json.load(f)

        if ctx.guild.id not in automodguild:
            automodguild.append(ctx.guild.id)
            await ctx.respond("Enabled serverlogs, saving settings...")
        elif ctx.guild.id in automodguild:
            automodguild.remove(ctx.guild.id)
            await ctx.respond("Disabled serverlogs, saving settings...")

        with open("loguilds.json", "w+") as f:
            json.dump(automodguild, f)

        await ctx.respond("Settings saved!")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        with open("loguilds.json") as f:
            automodguild = json.load(f)
        if message.guild.id not in automodguild:
            return
        guild=message.author.guild
        author = message.author
        ch = message.channel
        content = message.content
        orange = discord.Color.dark_orange()
        for channel in guild.channels:
            if str(channel.name) == "server-logs":
                msg_del = str(f"{content}")
                aut_name= str(f"{author}")
                ch_name = str(f"{ch.name}")
                embed = discord.Embed(color=orange)
                embed.set_author(name="Message Deleted")
                embed.add_field(name=f"Message", value=msg_del, inline=False)
                embed.add_field(name=f"Message Author", value=aut_name, inline=False)
                embed.add_field(name=f"Channel", value=ch_name, inline=False)
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        with open("loguilds.json") as f:
            automodguild = json.load(f)
        if before.guild.id not in automodguild:
            return
        if before.author.guild_permissions.administrator:
            return
        blue = discord.Colour.blue()
        guild = before.author.guild
        embed=discord.Embed(title=f"{before.author} edited a message", color=blue)
        embed.add_field(name= before.content ,value="This is the message before any edit", inline = True)
        embed.add_field(name = after.content, value="This is the message after the edit", inline = True)
        for channel in guild.channels:
            if str(channel.name) == "server-logs":
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        with open("loguilds.json") as f:
            automodguild = json.load(f)
        if guild.id not in automodguild:
            return
        member = user
        gold = discord.Color.dark_gold()
        for channel in guild.channels:
            if str(channel.name) == "server-logs":
                embed = discord.Embed(color=gold)
                embed.set_author(name=member.name)
                embed.add_field(name="User banned", value=f"{member} has been banned")
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        with open("loguilds.json") as f:
            automodguild = json.load(f)
        if role.guild.id not in automodguild:
            return
        guild = role.guild
        gold = discord.Color.dark_gold()
        for channel in guild.channels:
            if str(channel.name) == "server-logs":
                embed = discord.Embed(color=gold)
                embed.add_field(name="Role created", value=f"The role; {role} has been created")
                await channel.send(embed=embed)
    
    
    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        with open("loguilds.json") as f:
            automodguild = json.load(f)
        if guild.id not in automodguild:
            return
        gold = discord.Color.dark_gold()
        for channel in guild.channels:
            if str(channel.name) == "server-logs":
                embed = discord.Embed(color=gold)
                embed.set_author(name=user.name)
                embed.add_field(name="User unbanned", value=f"{user} has been unbanned")
                await channel.send(embed=embed)


def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(serverlogs(bot)) # add the cog to the bot