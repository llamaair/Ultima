import discord
import os
import requests
from datetime import datetime
from discord.ext import commands, bridge

class DeltaBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(description="Ping!")
    async def ping(self, ctx):
        await ctx.respond("Pong!")

    

def setup(bot):
    bot.add_cog(DeltaBot(bot))
