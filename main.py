import discord
from dotenv import load_dotenv
import os
import requests
import urllib
import random
import datetime
import datetime
import time

from discord.ext import commands
from discord import option
from discord.ext import bridge

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.all()

client = bridge.Bot(command_prefix="!", intents=intents, help_command=None)

client.persistent_views_added = False

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(client.guilds)} servers"))
    global startTime
    startTime = time.time()

@client.event
async def on_guild_join(guild):
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(client.guilds)} servers"))

@client.event
async def on_guild_remove():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(client.guilds)} servers"))

@client.bridge_command(description="Ping!")
async def ping(ctx):
    latency = (str(client.latency)).split('.')[1][1:3]
    await ctx.respond(f"Pong! Replied in {latency} ms")

client.load_extension("cogs.moderation")

client.run(TOKEN)