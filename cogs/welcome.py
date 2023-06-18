import discord
from discord.ext import commands, bridge
import asyncio
import random
import json

class welcome(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @bridge.bridge_command(description="Enable or disable auto welcome")
    @commands.has_permissions(administrator = True)
    async def welcoming(self, ctx, message):
        with open("welcoming.json") as f:
            automodguild = json.load(f)

        if ctx.guild.id not in automodguild:
            automodguild.append(ctx.guild.id)
            await ctx.respond("Enabled auto welcoming, saving settings...")
        elif ctx.guild.id in automodguild:
            automodguild.remove(ctx.guild.id)
            await ctx.respond("Disabled auto welcoming, saving settings...")

        with open("welcoming.json", "w+") as f:
            json.dump(automodguild, f)

        await ctx.respond("Settings saved!")
        
        with open("server_welcome_messages.json") as f:
            smsgs = json.load(f)
        smsgs[str(ctx.guild.id)] = message
        with open("server_welcome_messages.json", "w") as f:
            json.dump(smsgs, f)
            
    @bridge.bridge_command(description="Enable or disable DM welcoming")
    @commands.has_permissions(administrator = True)
    async def dmwelcoming(self, ctx, message):
        with open("dmwelcoming.json") as f:
            automodguild = json.load(f)

        if ctx.guild.id not in automodguild:
            automodguild.append(ctx.guild.id)
            await ctx.respond("Enabled dm welcoming, saving settings...")
        elif ctx.guild.id in automodguild:
            automodguild.remove(ctx.guild.id)
            await ctx.respond("Disabled dm welcoming, saving settings...")

        with open("dmwelcoming.json", "w+") as f:
            json.dump(automodguild, f)

        await ctx.respond("Settings saved!")
        
        with open("server_welcome_messages.json") as f:
            smsgs = json.load(f)
        smsgs[str(ctx.guild.id)] = message
        with open("server_welcome_messages.json", "w") as f:
            json.dump(smsgs, f)
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open("welcoming.json") as f:
            automodguild = json.load(f)
        if member.guild.id in automodguild:
            if member.guild.system_channel: # If it is not None
                with open("server_welcome_messages.json") as f:
                    welcomemsgs = json.load(f)
                welcome_message = welcomemsgs.get(str(member.guild.id))
                welcome_msg2 = f"{member.mention}, {welcome_message}"
                await member.guild.system_channel.send(f"{welcome_msg2}")
        with open("dmwelcoming.json") as r:
            lea = json.load(r)
        if member.guild.id in lea:
            with open("server_welcome_messages.json") as r:
                welcomemsgs1 = json.load(r)
            welcome_message = welcomemsgs1.get(str(member.guild.id))
            await member.send(f"{welcome_message}")
            print("another test")


def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(welcome(bot)) # add the cog to the bot