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

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open('levels.json', 'r') as f:
            users = json.load(f)

        if not f'{member.id}' in users:
            users[f'{member.id}'] = {}
            users[f'{member.id}']['experience'] = 0
            users[f'{member.id}']['level'] = 1

        with open('levels.json', 'r'):
            json.dump(users, f)

    @bridge.bridge_command(description="Enable and disable the leveling system")
    @commands.has_permissions(administrator = True)
    async def activelevel(self, ctx):
        with open("levelguilds.json") as f:
            automodguild = json.load(f)

        if ctx.guild.id not in automodguild:
            automodguild.append(ctx.guild.id)
            await ctx.respond("Enabled levels, saving settings...")
        elif ctx.guild.id in automodguild:
            automodguild.remove(ctx.guild.id)
            await ctx.respond("Disabled levels, saving settings...")

        with open("levelguilds.json", "w+") as f:
            json.dump(automodguild, f)

        await ctx.respond("Settings saved!")

    @bridge.bridge_command()
    async def level(self, ctx, member: discord.Member = None):
        if not member:
            id = ctx.author.id
            with open('levels.json', 'r') as f:
                users = json.load(f)
            lvl = users[str(id)]['level']
            await ctx.respond(f'You are at level {lvl}!')
        else:
            id = member.id
            with open('levels.json', 'r') as f:
                users = json.load(f)
            lvl = users[str(id)]['level']
            await ctx.respond(f'{member} is at level {lvl}!')
    
    @commands.Cog.listener()
    async def on_message(self, message):
        with open("levelguilds.json") as f:
            automodguild = json.load(f)
        if message.guild.id not in automodguild:
            return
        if message.author.bot == False:
            with open('levels.json', 'r') as f:
                users = json.load(f)

            if not f'{message.author.id}' in users:
                users[f'{message.author.id}'] = {}
                users[f'{message.author.id}']['experience'] = 0
                users[f'{message.author.id}']['level'] = 1
            
            users[f'{message.author.id}']['experience'] += 5
            with open('levelling.json', 'r') as g:
                levels = json.load(g)
            experience = users[f'{message.author.id}']['experience']
            lvl_start = users[f'{message.author.id}']['level']
            lvl_end = int(experience ** (1 / 4))
            if lvl_start < lvl_end:
                await message.channel.send(f'{message.author.mention} has reached level {lvl_end}! **GG**')
                users[f'{message.author.id}']['level'] = lvl_end

            with open('levels.json', 'w') as f:
                json.dump(users, f)
                


def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(levelling(bot)) # add the cog to the bot