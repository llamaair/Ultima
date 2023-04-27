import discord
from discord.ext import bridge, commands
from datetime import timedelta
import time
import random

class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(description="Play rock, paper, scissors!")
    async def rps(self, ctx, *, player_choice):
        username = str(ctx.author).split('#')[0]
        if player_choice == None:
            await ctx.respond("Please enter rock, paper or scissors.")
            return
        choices = ['rock', 'paper', 'scissors']
        bot_choice = random.choice(choices)
        if player_choice.lower() not in choices:
            await ctx.respond('Please enter rock, paper or scissors.')
        else:
            if player_choice.lower() == bot_choice.lower():
                await ctx.respond(f'Tie. We both picked {bot_choice}')
                return
            elif (player_choice.lower() == 'rock' and bot_choice.lower()
              == 'scissors') or (player_choice.lower() == 'scissors'
                                 and bot_choice.lower() == 'paper') or (
                                     player_choice.lower() == 'paper'
                                     and bot_choice.lower() == 'rock'):
                await ctx.respond(
                f'Yes! You won, haha, my choice was {bot_choice}.')
                return
            elif (player_choice.lower() == 'rock' and bot_choice.lower() == 'paper'
              ) or (player_choice.lower() == 'scissors' and bot_choice.lower()
                    == 'rock') or (player_choice.lower() == 'paper'
                                   and bot_choice.lower() == 'scissors'):
                await ctx.respond(
                f"Hey {username}! Don't be mad but i won :slight_smile: My choice was {bot_choice}."
            )
                
    def setup(bot):
        bot.add_cog(fun(bot))