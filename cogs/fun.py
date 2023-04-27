import discord
from discord.ext import bridge, commands
from datetime import timedelta
import time
import random

class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

                
def setup(bot):
    bot.add_cog(fun(bot))