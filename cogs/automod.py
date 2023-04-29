import discord
from discord.ext import commands
import asyncio
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
        with open("automodguilds.json") as f:
            automodguild = json.load(f)

        if ctx.guild.id not in automodguild:
            automodguild.append(ctx.guild.id)
            await ctx.respond("Enabled automod, saving settings...")
        elif ctx.guild.id in automodguild:
            automodguild.remove(ctx.guild.id)
            await ctx.respond("Disabled automod, saving settings...")

        with open("automodguilds.json", "w+") as f:
            json.dump(automodguild, f)

        await ctx.respond("Settings saved!")
        
        
    @bridge.bridge_command(description="Flag or unflag a member to make automod stricter for them")
    @commands.has_permissions(administrator = True)
    async def flag(self, ctx, flaguser:discord.Member):
        with open("flagged.json") as f:
            automodguild = json.load(f)

        if flaguser.id not in automodguild:
            automodguild.append(flaguser.id)
            await ctx.respond(f"Successfully flagged user {flaguser.name}")
        elif flaguser.id in automodguild:
            automodguild.remove(flaguser.id)
            await ctx.respond(f"Successfully unflagged user {flaguser.name}")

        with open("flagged.json", "w+") as f:
            json.dump(automodguild, f)

        print("Flagging list updated.")

    @commands.Cog.listener()
    async def on_message(self, message):
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel.name)
        guild = str(message.guild.name)
        badlinks=["http://donionsixbjtiohce24abfgsffo2l4tk26qx464zylumgejukfq2vead.onion/onions.php", "https://www.propub3r6espa33w.onion", "http://msydqstlz2kzerdg.onion", "https://3g2upl4pq6kufc4m.onion", "https://www.pornhub.com"]
        with open("automodguilds.json") as f:
            automodguild = json.load(f)
        with open("flagged.json") as f:
              hehe = json.load(f)
        if message.guild.id in automodguild:
            if  message.author.bot:
                return 
            if message.author.guild_permissions.administrator:
                return
            for x in badlinks:
              if x in message.content.lower():
                await message.delete()
                if message.author.id in hehe:
                  await message.author.ban(reason="Sending bad links")
                  await ctx.send(f"Successfully autobanned {message.author} for sending bad links")
                else:
                  await message.author.timeout_for(timedelta(minutes=60))
            if 'nigga' in message.content.lower():
                await message.delete()
                await message.channel.send(f"{message.author.mention} watch your mouth :eyes:")
            if 'cunt' in message.content.lower():
                await message.delete()
                await message.channel.send(f"{message.author.mention} watch your mouth :eyes:")
            if 'discord.gg' in message.content.lower():
                if message.guild.id == 975759697162436608:
                    return
                await message.delete()
                await message.channel.send(f"{message.author.mention}, please do not send invite links to other servers here")
            if 'slut' in message.content.lower():
                await message.delete()
                await message.channel.send(f"{message.author.mention} watch your mouth :eyes:")
                await message.author.timeout_for(timedelta(minutes=15))
                print(hehe)
                print(message.author.id)
                if message.author.id in hehe:
                  print("In hehe")
                  await message.author.send(f"You have been banned from {message.guild} for using bad words by FetchBot automod")
                  await message.author.ban(reason="Using bad words")
                  await message.channel.send(f"Autobanned user {message.author} for using bad words")
            if 'whore' in message.content.lower():
                await message.delete()
                await message.channel.send(f"{message.author.mention} watch your mouth :eyes:")
                await message.author.timeout_for(timedelta(minutes=15))
            if 'motherfucker' in message.content.lower():
                await message.delete()
                await message.channel.send(f"{message.author.mention} watch your mouth :eyes:")
            if 'nigger' in message.content.lower():
                await message.delete()
                await message.channel.send(f"{message.author.mention} watch your mouth :eyes:")
                await message.author.timeout_for(timedelta(minutes=15))
            if 'bitch' in message.content.lower():
                await message.delete()
                await message.channel.send(f"{message.author.mention} watch your mouth :eyes:")
            if 'fucker' in message.content.lower():
                await message.delete()
                await message.channel.send(f"{message.author.mention} watch your mouth :eyes:")
            if 'fuck yourself' in message.content.lower():
                await message.delete()
                await message.channel.send(f"{message.author.mention} watch your mouth :eyes:")
                await message.author.timeout_for(timedelta(minutes=20))
            if 'fuck off' in message.content.lower():
                await message.delete()
                await message.channel.send(f"{message.author.mention} watch your mouth :eyes:")
                await message.author.timeout_for(timedelta(minutes=15))
            if len(message.raw_mentions) > 5:
                await message.delete()
                await message.channel.send(f"{message.author.mention} Please do not mass mention people :skull:")
            if len(message.raw_mentions) > 7:
                await message.author.timeout_for(timedelta(minutes=15))
                if message.author.id in hehe:
                  await message.author.send(f"You have been banned from {message.guild} for mass mentioning people by FetchBot Automod")
                  await message.author.ban(reason= "Mass mentioning")
                  await message.channel.send(f"Autobanned user {message.author} for mass mentioning")
            if len(message.raw_mentions) > 14:
                await message.author.send(f"You have been banned from {message.guild} for mass mentioning people by FetchBot Automod")
                await message.author.ban(reason = "Mass mentioning")
                await message.channel.send(f"Autobanned user {message.author} for mass mentioning")
            bucket = self.anti_spam.get_bucket(message)
            retry_after = bucket.update_rate_limit()
            if retry_after:
                await message.delete()
                await message.channel.send(f"{message.author.mention}, don't spam!", delete_after = 10)
                await message.author.timeout_for(timedelta(minutes=30))


def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(automod(bot)) # add the cog to the bot