import discord
from discord.ext import commands
import asyncio
import random
import json
from discord.ext import bridge

class levelling(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot


    @bridge.bridge_command(description="Enable or disable the leveling system")
    @bridge.has_permissions(administrator = True)
    async def leveling(self, ctx):
        ena=None
        with open("levelguilds.json") as f:
            automodguild = json.load(f)

        if ctx.guild.id not in automodguild:
            automodguild.append(ctx.guild.id)
            ena="enabled"
        elif ctx.guild.id in automodguild:
            automodguild.remove(ctx.guild.id)
            ena="disabled"

        with open("levelguilds.json", "w+") as f:
            json.dump(automodguild, f)

        embed = discord.Embed(title="Success!", color=discord.Colour.green(), description=f"Successfully {ena} server leveling!")
        await ctx.respond(embed=embed)

    @bridge.bridge_command(description="Get your current level")
    async def level(self, ctx, member: discord.Member = None):
        await ctx.defer()
        if not member:
            member = ctx.author

        id = str(member.id)
        with open('levels.json', 'r') as f:
            users = json.load(f)

        if id not in users:
            users[id] = {}
            users[id]['experience'] = 0
            users[id]['level'] = 1

        lvl = users[id]['level']
        await ctx.respond(embed=discord.Embed(title=f"{member.name}'s level", description=f"{member.name} is at level {lvl}!"))

        with open('levels.json', 'w') as f:
            json.dump(users, f)

    @commands.Cog.listener()
    async def on_message(self, message):
        with open("levelguilds.json") as f:
            automodguild = json.load(f)
        try:
            if message.guild.id not in automodguild:
                return
        except:
            return
        if message.author.bot == False:
            with open('levels.json', 'r') as f:
                users = json.load(f)

            if not f'{message.author.id}' in users:
                users[f'{message.author.id}'] = {}
                users[f'{message.author.id}']['experience'] = 0
                users[f'{message.author.id}']['level'] = 1

            users[f'{message.author.id}']['experience'] += 5
            experience = users[f'{message.author.id}']['experience']
            lvl_start = users[f'{message.author.id}']['level']
            lvl_end = int(experience ** (1 / 4))
            if lvl_start < lvl_end:
                await message.channel.send(f'{message.author.mention} has reached level {lvl_end}! **GG**', delete_after=10, silent=True)
                users[f'{message.author.id}']['level'] = lvl_end

            with open('levels.json', 'w') as f:
                json.dump(users, f)

                


def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(levelling(bot)) # add the cog to the bot