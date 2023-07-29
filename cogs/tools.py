import discord
from discord.ext import commands
import asyncio
import time
from math import sqrt
import random
from urllib.request import urlopen
from discord.ext import bridge

class tools(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @bridge.bridge_group()
    async def random(self, ctx):
        pass
        
    @random.command(description="Generate a random number")
    async def number(self, ctx, lowernumber: int, uppernumber: int):
        number = random.randrange(lowernumber, uppernumber)
        await ctx.respond(f"Your random number in range of {lowernumber} and {uppernumber} is {number}")

    @discord.message_command()
    async def getmessageid(self, ctx, message:discord.Message):
        await ctx.respond(f"{message.id}", ephemeral=True)
        
    @discord.user_command()
    async def getuserid(self, ctx, user:discord.User):
        await ctx.respond(f"{user.id}", ephemeral=True)
    
    @bridge.bridge_command(description="Generate a timestamp")
    async def timestamp(self, ctx):
        t1 = discord.utils.format_dt(discord.utils.utcnow(), "f")
        t2 = discord.utils.format_dt(discord.utils.utcnow(), "F")
        t3 = discord.utils.format_dt(discord.utils.utcnow(), "d")
        t4 = discord.utils.format_dt(discord.utils.utcnow(), "D")
        t5 = discord.utils.format_dt(discord.utils.utcnow(), "t")
        t6 = discord.utils.format_dt(discord.utils.utcnow(), "T")
        t7 = discord.utils.format_dt(discord.utils.utcnow(), "R")
        await ctx.respond(f"{t1}\n{t2}\n{t3}\n{t4}\n{t5}\n{t6}\n{t7}")

    @random.command(description="Generate a random hex color!")
    async def color(self, ctx):
        await ctx.defer()
        rcolor = lambda: random.randint(0, 255)
        color = "#%02X%02X%02X" % (rcolor(), rcolor(), rcolor())
        color = color.replace("#", "")
        crgblink = f"https://some-random-api.ml/canvas/misc/rgb?hex={color}"
        crgbpage = urlopen(crgblink)
        crgbbytes = crgbpage.read()
        crgbdecode = crgbbytes.decode("utf-8")
        crgb0 = crgbdecode.replace("{\"r\":", "")
        crgb1 = crgb0.replace("\"g\":", "")
        crgb2 = crgb1.replace("\"b\":", "")
        crgb3 = crgb2.replace("}", "")
        crgb = crgb3.replace(",", ", ")
        embed = discord.Embed(
            title=f"#{color}",
            description=f"Random Color"
        )
        embed.add_field(name=f"RGB", value=f"{crgb}")
        embed.set_image(url=f"https://some-random-api.ml/canvas/misc/colorviewer?hex={color}")
        embed.set_footer(icon_url=ctx.author.avatar.url, text=f"Requested by {ctx.author}")
        await ctx.respond(embed=embed)

    @bridge.bridge_command(description="See a users avatar!")
    async def avatar(self, ctx, *, member: discord.Member = None):
        if member == None:
            member = ctx.author
        embed = discord.Embed(title=f"{str(member)}'s avatar :", color = random.randrange(0, 0xffffff)) 
        embed.set_image(url=member.avatar.url)
        embed.set_footer(icon_url = ctx.author.avatar.url,text =f"Requested By {ctx.author}")
        await ctx.respond(embed=embed)

    @bridge.bridge_command(description="Send a Thanks to another member")
    async def thanks(self, ctx, member: discord.User):
        await ctx.respond("Thanks sent", ephemeral = True)
        embed = discord.Embed(title="Thanks!", description=f"You just received a thank you from {ctx.author.mention} :tada:")
        await member.send(embed=embed)


    @bridge.bridge_command(description="Get the server's current boostcount")
    async def boostcount(self, ctx):
        embed = discord.Embed(title = f'{ctx.guild.name}\'s Boost Count', description = f'{str(ctx.guild.premium_subscription_count)}')
        await ctx.respond(embed = embed)

    @bridge.bridge_command(description="Get a invite link to our discord server!")
    async def support(self, ctx):
        await ctx.respond("Have you found an issue with FetchBot or a bug, or just want to chat with other people using FetchBot? Join our discord server; https://discord.gg/uBEK23mmmK")
    
    @bridge.bridge_group()
    async def math(self, ctx):
        pass

    @math.command(description="Subtract a number from another number!")
    async def subtract(self, ctx, firstnumber:int, secondnumber:int):
        await ctx.respond(f"{firstnumber}-{secondnumber} = {firstnumber-secondnumber}")
        
    @math.command(description="Add a number to another number!")
    async def add(self, ctx, firstnumber:int, secondnumber:int):
        await ctx.respond(f"{firstnumber}+{secondnumber} = {firstnumber+secondnumber}")
        
    @math.command(description="Divide a number from another number!")
    async def divide(self, ctx, firstnumber:int, secondnumber:int):
        await ctx.respond(f"{firstnumber}/{secondnumber} = {firstnumber/secondnumber}")
        
    @math.command(description="Multiply a number with another number!")
    async def multiply(self, ctx, firstnumber:int, secondnumber:int):
        await ctx.respond(f"{firstnumber}*{secondnumber} = {firstnumber*secondnumber}")
        
    @math.command(description="Calculate the square root of a number")
    async def root(self, ctx, number:float):
        await ctx.respond(f"The square root of {number} is {sqrt(number)}")
        
    
    @bridge.bridge_command(description="Get info about the server")
    async def serverinfo(self, ctx):
        id = ctx.guild.id
        txt = len(ctx.guild.text_channels)
        vc = len(ctx.guild.voice_channels)
        tim = str(ctx.guild.created_at)
        owner=ctx.guild.owner
        embed=discord.Embed(
        title=f"Server info"
        )
        embed.add_field(name=":ballot_box: Server Name", value=f"{ctx.guild}")
        embed.add_field(name="Server members", value=f"{ctx.guild.member_count}")
        embed.add_field(name=":crown: Server Owner", value=owner)
        embed.add_field(name=":calendar: Created at", value=f"{tim}")
        embed.add_field(name="Text Channels", value=f"{txt}")
        embed.add_field(name="Voice Channels", value=f"{vc}")
        embed.add_field(name="ID", value=f"{id}")
        await ctx.respond(embed=embed)

        
    @bridge.bridge_command(description="Get info about a member")
    async def whois(self, ctx, member:discord.Member):
        j = str(member.joined_at)[0:11]
        c = str(member.created_at)[0:11]
        embed=discord.Embed(
        title="User Info"
        )
        embed.add_field(name=":name_badge: Name", value=f"{member.name}")
        embed.add_field(name="Nickname", value=f"{member.nick}")
        embed.add_field(name=":flower_playing_cards: Joined Discord", value=f"{c}")
        embed.add_field(name="Joined Server", value=f"{j}")
        embed.add_field(name=":credit_card: ID", value=f"{member.id}")
        embed.add_field(name="Highest role", value=f"{member.top_role.mention}")
        embed.set_footer(text=f"Requested by: {ctx.author.name}")
        await ctx.respond(embed=embed)


def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(tools(bot)) # add the cog to the bot