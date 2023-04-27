import discord
import asyncio
import random
from discord.ext import commands, bridge

class report(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot
        
    @bridge.bridge_command(description="Report an issue/bug with the bot")
    async def report(self, ctx, issue):
      user = self.bot.get_user(719527356368289802)
      user1 = self.bot.get_user(763066260233650226)
      embed = discord.Embed(title=f"New report submitted from {ctx.author} with id {ctx.author.id}")
      embed.add_field(name="Reported Issue:", value=issue)
      await user.send(embed=embed)
      await user1.send(embed=embed)
      await ctx.respond("Your report has successfully been submitted. Usual response time is within 24 hours :white_check_mark:", ephemeral=True)
    
    @bridge.bridge_command(description="Reply to a reported issue")
    async def reply(self, ctx, userid, response):
        if ctx.author.id not in [719527356368289802, 763066260233650226]:
            return await ctx.respond("Insufficent permissions")
        usso = self.bot.get_user(int(userid))
        embed = discord.Embed(title=f"Your report just got a reply!")
        embed.add_field(name="Reply", value=response)
        embed.set_footer(text=f"Response provided to you by: {ctx.author.name}")
        await usso.send(embed=embed)
        await ctx.respond("Successfully sent reply :white_check_mark:", ephemeral=True)
        
        
        
def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(report(bot)) # add the cog to the bot