import discord
from discord.ext import commands
import asyncio
from discord import option
import random
import json
import datetime
import time
from datetime import timedelta
from discord.ext import bridge

class automod(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot
        self.anti_spam = commands.CooldownMapping.from_cooldown(5, 15, commands.BucketType.member)

    @bridge.bridge_command(description="Enable or disable automod")
    @commands.has_permissions(administrator = True)
    async def automod(self, ctx):
        await create_auto_moderation_rule(name="Mention spam block", event_type=on_message, trigger_type=spam, enabled=True)
        

    

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(automod(bot)) # add the cog to the bot