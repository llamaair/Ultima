import discord
import asyncio
import random
import datetime
import wavelink
import time
import urllib
import re
import os
import json
import openai
from typing import List
import aiohttp
import logging
from threading import Thread

from db import Database

import psutil

import requests
from bs4 import BeautifulSoup

from discord.ext.pages import Paginator, Page
from flask import Flask

from discord.utils import get
from discord.ext import commands
from discord.ext import tasks
from discord import option
from translate import Translator
from discord.ext import bridge
try: 
	from geopy.geocoders import Nominatim
except:
    os.system("pip install geopy")
from dotenv import load_dotenv
#---------------------------#
#NAME: Ultima
#Status: Working
#Version: 4.0.1
#Creator: Marc13, UmayKamaboko and trembanto
#---------------------------#
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
TOKEN5 = os.getenv("DISCORD_TOKEN5")
TOKEN8 = os.getenv("DISCORD_TOKEN8")
TOKEN10 = os.getenv("DISCORD_TOKEN10")
TOKEN11 = os.getenv("DISCORD_TOKEN11")
openai.api_key = os.getenv("OPENAI_KEY")
oapi_key = openai.api_key
intents = discord.Intents.all()

DB_HOST = "54.37.204.19"
DB_USER = "u77345_B1HfvsHZDE"
DB_PASSWORD = "F16tUi@Zjzrr3dyC.3cPaN.^"
DB_DATABASE = "s77345_economy_database"

db = Database(DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE)

class Ultima(bridge.Bot):
   TOKEN = os.getenv("DISCORD_TOKEN")
   intents = discord.Intents.all()
   help_command=None

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    server_id = str(message.guild.id)
    custom_prefix = prefixes.get(server_id, '!')  # Default prefix is '!'
    return custom_prefix

client = Ultima(intents=Ultima().intents, help_command=Ultima().help_command, command_prefix=get_prefix)

client5 = bridge.Bot(command_prefix="!", intents=intents, help_command=None)

client8 = bridge.Bot(command_prefix="e", intents=intents, help_command=None)


client.persistent_views_added=False
client8.persistent_views_added=False

global lastMeme
lastMeme = 0



#logger = logging.getLogger('discord')
#logger.setLevel(logging.DEBUG)
#handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
#handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
#logger.addHandler(handler)

class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = "X"
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = discord.ButtonStyle.success
            self.label = "O"
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        self.disabled = True
        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = "X won!"
            elif winner == view.O:
                content = "O won!"
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


class TicTacToe(discord.ui.View):
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],

        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == -3:
            return self.X
        elif diag == 3:
            return self.O

        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None

class advancedticket(discord.ui.View):
   def __init__(self):
      super().__init__(timeout=None)
   
   @discord.ui.select(
      custom_id="select-1",
      placeholder = "Open a ticket!",
      min_values = 1,
      max_values = 1,
      options = [
         discord.SelectOption(
            label="Report",
            description="Report a user"
         ),
         discord.SelectOption(
            label="Suggestion",
            description="Suggest an improvement for the server"
         ),
         discord.SelectOption(
            label="Other",
            description="Open a ticket for an issue not listed above"
         )
      ]
   )
   async def select_callback(self, select, interaction):
      overwrites = {
        interaction.guild.default_role: discord.PermissionOverwrite(view_channel = False),
        interaction.user: discord.PermissionOverwrite(view_channel = True, send_messages= True, embed_links=True),
        interaction.guild.me: discord.PermissionOverwrite(view_channel = True, send_messages = True, read_message_history = True)
        }
      channel = await interaction.guild.create_text_channel(f'ticket-{interaction.user.name}', overwrites = overwrites, reason = f"Ticket for {interaction.user}")
      await interaction.response.send_message(f"Ticket opened at {channel.mention}", ephemeral=True)
      if select.values[0]=="Report":
         await channel.send(f"Welcome to your ticket {interaction.user.mention}. The support team will be with you shortly. Please specify which user you wish to report, and why.", view=CloseTicket())
      elif select.values[0]=="Suggestion":
         await channel.send(f"Welcome to your ticket {interaction.user.mention}. The support team will be with you shortly. What would you like to suggest for the server?", view=CloseTicket())
      else:
         await channel.send(f"Welcome to your ticket {interaction.user.mention}. The support team will be with you shortly. What do you need help with?", view=CloseTicket())

class MyViewa(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Developer application", custom_id="dev-app", row=0, style=discord.ButtonStyle.primary, emoji="🚀")
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(DevApp(title="Developer Application"))
    
    @discord.ui.button(label="Mod application", custom_id="admin-app", row=0, style=discord.ButtonStyle.primary, emoji="⚙️")
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_modal(ModApp(title="Mod Application"))
        

    
class RulesView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Verify", custom_id="rules-accept", style=discord.ButtonStyle.primary, emoji="✅")
    async def button_callback(self, button, interaction):
        role = get(interaction.user.guild.roles, name="Verified")
        if role in interaction.user.roles:
            await interaction.response.send_message("You are already verified!", ephemeral=True)
            return
        await interaction.user.add_roles(role)
        await interaction.response.send_message("You are now verified :white_check_mark: Breaking the rules will result in a timeout, kick or ban.", ephemeral=True)
        
class FrontBack(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="Frontend", custom_id="frontend", row=0, style=discord.ButtonStyle.success)
    async def button_callback(self, button, interaction):
        role = get(interaction.user.guild.roles, name="Frontend")
        if role not in interaction.user.roles:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("Successfully assigned Frontend role :white_check_mark:", ephemeral=True)
        else:
            await interaction.response.send_message("You already have the Frontend role!", ephemeral=True)
    
    @discord.ui.button(label="Backend", custom_id="backend", row=0, style=discord.ButtonStyle.success)
    async def button2_callback(self, button, interaction):
        role = get(interaction.user.guild.roles, name="Backend")
        if role not in interaction.user.roles:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("Successfully assigned Backend role :white_check_mark:", ephemeral=True)
        else:
            await interaction.response.send_message("You already have the Backend role!", ephemeral=True)
    
    @discord.ui.button(label="Operations", custom_id="ops", row=0, style=discord.ButtonStyle.success)
    async def button3_callback(self, button, interaction):
        role = get(interaction.user.guild.roles, name="Operations")
        if role not in interaction.user.roles:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("Successfully assigned Operations role :white_check_mark:", ephemeral=True)
        else:
            await interaction.response.send_message("You already have the Operations role!", ephemeral=True)

class DevApp(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="What experiences do you have in programming?", style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="Why do you want to join the developer team?", style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="GitHub Username"))
        

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="New developer application!")
        embed.add_field(name="Experiences", value=self.children[0].value)
        embed.add_field(name="Why?", value=self.children[1].value)
        embed.add_field(name="GitHub Username", value=self.children[2].value)
        embed.add_field(name="Submitted by", value=interaction.user)
        member = client8.get_user(719527356368289802)
        member2 = client8.get_user(245258174553260033)
        member3 = client8.get_user(315957528846663683)
        chan = client8.get_channel(1118034066634199040)
        await chan.send(embeds=[embed])
        await interaction.response.send_message("Successfully submitted application :white_check_mark: You will get a DM from an admin soon!", ephemeral=True)
        
class ModApp(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="How old are you?"))
        self.add_item(discord.ui.InputText(label="What experiences do you have in moderation?", style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="Have you moderated any other discord servers?", style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="Why do you want to become a moderator?", style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="What can you do for the server?", style=discord.InputTextStyle.long))
        

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="----------------------------------\nNew moderator application in EDPN!")
        embed.add_field(name="Age", value=self.children[0].value)
        embed.add_field(name="Experiences", value=self.children[1].value)
        embed.add_field(name="Moderated other servers?", value=self.children[2].value)
        embed.add_field(name="Why", value=self.children[3].value)
        embed.add_field(name="What can you do?", value=self.children[4].value)
        embed.add_field(name="Submitted by", value=interaction.user)
        await interaction.response.send_message("Successfully submitted moderator application :white_check_mark: You will get a DM from an admin soon!", ephemeral=True)
        member = client8.get_user(719527356368289802)
        member2 = client8.get_user(245258174553260033)
        

        await member.send("----------------------------------\n**New admin application!**")
        await member.send(self.children[0].value)
        await member.send(self.children[1].value)
        await member.send(self.children[2].value)
        await member.send(self.children[3].value)
        await member.send(self.children[4].value)
        await member.send(f"Submitted by {interaction.user}\n**End of application**\n----------------------------------")
        
        await member2.send("----------------------------------\n**New admin application!**")
        await member2.send(self.children[0].value)
        await member2.send(self.children[1].value)
        await member2.send(self.children[2].value)
        await member2.send(self.children[3].value)
        await member2.send(self.children[4].value)
        await member2.send(f"Submitted by {interaction.user}\n**End of application**\n----------------------------------")
            
class DeltaModApp(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="How old are you?"))
        self.add_item(discord.ui.InputText(label="What experiences do you have in moderation?", style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="Have you moderated any other discord servers?", style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="Why do you want to become a mod?", style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="What can you do for the server?", style=discord.InputTextStyle.long))
        

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="----------------------------------\nNew moderator application in Cremorrah!")
        embed.add_field(name="Age", value=self.children[0].value)
        embed.add_field(name="Experiences", value=self.children[1].value)
        embed.add_field(name="Moderated other servers?", value=self.children[2].value)
        embed.add_field(name="Why", value=self.children[3].value)
        embed.add_field(name="What can you do?", value=self.children[4].value)
        embed.add_field(name="Submitted by", value=interaction.user)
        await interaction.response.send_message("Successfully submitted moderator application :white_check_mark: You will get a DM from an admin soon!", ephemeral=True)
        guild = client5.get_guild(1110974953974665387)
        chan = guild.get_channel(1131160637205119006)
        

        await chan.send("----------------------------------\n**New mod application!**")
        await chan.send(f"Age: *{self.children[0].value}*")
        await chan.send(f"Experiences: *{self.children[1].value}*")
        await chan.send(f"Moderated other servers: *{self.children[2].value}*")
        await chan.send(f"Why: *{self.children[3].value}*")
        await chan.send(f"What can you do for the server: *{self.children[4].value}*")
        await chan.send(f"Submitted by {interaction.user}\n**End of application**\n----------------------------------")

class DeltaApp(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="Fleet Application", custom_id="deltfleet", style=discord.ButtonStyle.primary, emoji="🚀")
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(deltafleetapp(title="Fleet Application"))
    
    @discord.ui.button(label="Moderator Application", custom_id="moddeltafleet", style=discord.ButtonStyle.primary, emoji="🔨")
    async def button_two_callback(self, button, interaction):
       await interaction.response.send_modal(DeltaModApp(title="Moderator Application"))

class deltafleetapp(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="CMDR Name"))
        self.add_item(discord.ui.InputText(label="Carrier name and ID"))
        self.add_item(discord.ui.InputText(label="Why do you want to join our fleet?", style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="Role you're applying for"))
        

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="New Cremorrah Fleet application!")
        embed.add_field(name="CMDR Name", value=self.children[0].value)
        embed.add_field(name="Carrier name?", value=self.children[1].value)
        embed.add_field(name="Why?", value=self.children[2].value)
        embed.add_field(name="Role", value=self.children[3].value)
        embed.add_field(name="Submitted by", value=interaction.user)
        member = client5.get_user(719527356368289802)
        member2 = client5.get_user(686846149608734730)
        await member.send(embeds=[embed])
        await member2.send(embeds=[embed])
        await interaction.response.send_message("Successfully submitted application :white_check_mark: Expect response within 24 hours or less!", ephemeral=True)

class MyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Create a ticket", style=discord.ButtonStyle.primary, emoji="📩", custom_id="persistent_view:primary")
    async def button_callback(self, button, interaction):
        overwrites = {
        interaction.guild.default_role: discord.PermissionOverwrite(view_channel = False),
        interaction.user: discord.PermissionOverwrite(view_channel = True, send_messages= True, embed_links=True),
        interaction.guild.me: discord.PermissionOverwrite(view_channel = True, send_messages = True, read_message_history = True)
        }
        channel = await interaction.guild.create_text_channel(f'ticket-{interaction.user.name}', overwrites = overwrites, reason = f"Ticket for {interaction.user}")
        await channel.send(f"Welcome to your ticket {interaction.user.mention}. The support team will be with you shortly. What do you need help with?", view=CloseTicket())
        await interaction.response.send_message(f"Ticket opened at {channel.mention}", ephemeral=True)

        
class CloseTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Close ticket", style=discord.ButtonStyle.danger, emoji="🔒", custom_id="persistent_view:red")
    async def button_callback(self, button, interaction):
        await interaction.response.send_message(":white_check_mark: Closing this ticket...")
        await asyncio.sleep(2)
        await interaction.channel.delete()
        
    
@client.bridge_command(description="Get the latest news!")
async def news(ctx, countrycode):
    api_key = 'c4b2f2b7c2784a379c3967c6170220da'
    news_api_url = 'https://newsapi.org/v2/top-headlines'
    country = countrycode 

    async with aiohttp.ClientSession() as session:
        url = f"{news_api_url}?country={country}&apiKey={api_key}"
        async with session.get(url) as response:
            news_json = await response.json()

    if news_json['status'] == 'ok':
        articles = news_json['articles']
        for article in articles:
            article_title = article['title']
            article_url = article['url']
            article_description = article['description']

            embed = discord.Embed(title=article_title, url=article_url, description=article_description)
            await ctx.respond(embed=embed)
            return
    else:
        await ctx.respond('Error retrieving news')
        
@client.bridge_command(description="Start the ticketing system")
@commands.has_permissions(ban_members=True)
async def ticketing(ctx, system:discord.Option(choices=['Basic', 'Advanced'])):
    if system=="Advanced":
       embed = discord.Embed(title="Create a ticket", description="Choose a category below for your ticket", color=discord.Colour.green())
       embed2 = discord.Embed(title="Success!", color=discord.Colour.green(), description=f"Successfully started ticketing system!")
       await ctx.respond(embed=embed2, ephemeral=True)
       await ctx.send(embed=embed, view=advancedticket())
       return  
    embed=discord.Embed(title="Create a ticket", description="Create a ticket below for general questions and support", color = discord.Colour.green())
    embed2 = discord.Embed(title="Success!", color=discord.Colour.green(), description=f"Successfully started ticketing system!")
    await ctx.respond(embed=embed2, ephemeral=True)
    await ctx.send(embed=embed, view=MyView())
   
    
@client.bridge_command(description="Unban a user")
async def unban(ctx, userid):
    try:
      user = await client.fetch_user(int(userid))
      guildo = ctx.guild
      await guildo.unban(user)
      embed = discord.Embed(title="Success!", color=discord.Colour.green(), description=f"Successfully unbanned user {user.name}")
      await ctx.respond(embed=embed, ephemeral=True)
    except:
       embed = discord.Embed(title="Failure", color=discord.Colour.green(), description=f"Failed to unban user!")
       await ctx.respond(embed=embed, ephemeral=True)

def guild(guild_id):
   def predicate(ctx):
      return ctx.guild and ctx.guild.id == guild_id
   return commands.check(predicate)

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    server_id = str(message.guild.id)
    custom_prefix = prefixes.get(server_id, '!')  # Default prefix is '!'
    return custom_prefix


@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    server_id = str(guild.id)
    prefixes[server_id] = '!'  # Set default prefix as '!' for the new server

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@tasks.loop(seconds=15)
async def presence():
   list1 = ['/help', '/iss', '/joke', '/ttt', '/reddit', '/economy beg', '/economy rob', '/economy robmember', '/level', '/ask', '/afk set', '/autorole', '/avatar', '/cat', '/fatcat', '/dog', '/embed', '/github', '/imagesearch']
   choice = random.choice(list1)
   await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{choice}"))

@client.bridge_command(description="Get information about the bot")
async def about(ctx):
    total_guilds = len(client.guilds)
    total_members = sum(guild.member_count for guild in client.guilds)
    total_shards = client.shard_count
    ram_usage = psutil.virtual_memory().used / (1024 ** 3)
    cpu_usage = psutil.cpu_percent()

    embed = discord.Embed(title="About Ultima", color=discord.Color.blue())
    embed.add_field(name="Total Guilds", value=str(total_guilds))
    embed.add_field(name="Total Members", value=str(total_members))
    embed.add_field(name="Total Shards", value=str(total_shards))
    embed.add_field(name="RAM Usage", value=f"{ram_usage:.2f} MB")
    embed.add_field(name="CPU Usage", value=f"{cpu_usage:.2f}%")
    await ctx.respond(embed=embed)

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")
    await db.connect()
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name=f"{len(client.guilds)} servers"))
    global startTime
    startTime = time.time()
    if not client.persistent_views_added:
        client.add_view(MyView())
        client.add_view(advancedticket())
        client.add_view(CloseTicket())
        client5.add_view(DeltaApp())
        client.persistent_views_added = True
        print("Persistent views added")
        presence.start()
        try:
          await client5.start(TOKEN5)
        except:
           pass
        
@client.event
async def on_disconnect():
   await db.close()
   print("Database connection closed!")
       
@client.bridge_command()
async def ttt(ctx):
    """Starts a tic-tac-toe game."""
    await ctx.respond("Tic Tac Toe: X goes first", view=TicTacToe())
    
@client8.bridge_command()
@commands.has_role('Moderator')
async def strike(ctx, user:discord.User):
    role = get(ctx.guild.roles, name="Strike 1")
    if role in user.roles:
        role2=get(ctx.guild.roles, name="Strike 2")
        if role2 in user.roles:
            role3=get(ctx.guild.roles, name="Strike 3")
            if role3 in user.roles:
                try:
                    await user.ban(reason="No reason provided")
                    await ctx.respond("User kicked...", ephemeral=True)
                except:
                    pass
            else:
                await user.add_roles(role3)
                await ctx.respond("Added Strike 3 to user", ephemeral=True)
                await user.send("You have received your third strike. One more will cause a ban")
                return
        else:
            await user.add_roles(role2)
            await ctx.respond("Added Strike 2 to user", ephemeral=True)
            await user.send("You have received your second strike. 2 more will cause a ban")
            return
    else:
        await user.add_roles(role)
        await ctx.respond("Added Strike 1 to user", ephemeral=True)
        await user.send("You have received your first strike. 3 more will cause a ban")
        return
    
@client8.event
async def on_ready():
    print(f"Logged in as {client8.user.name}")
    client8.add_view(MyViewa())
    client8.add_view(RulesView())
    client8.add_view(FrontBack())

@client8.bridge_command()
async def nasa_image(ctx):
    url = 'https://apod.nasa.gov/apod/astropix.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    link = soup.find('a', href=lambda href: href.endswith('.jpg') or href.endswith('.png'))

    if link:
        image_url = f'https://apod.nasa.gov/apod/{link["href"]}'
        embed = discord.Embed(title='NASA Astronomy Picture of the Day')
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)
    else:
        await ctx.respond("Unable to fetch NASA image.")
    
@client8.bridge_command()
async def apps(ctx):
   await ctx.send(embed=discord.Embed(title="Applications", description="Press one of the buttons below to start the form for developer or moderator applications."), view=MyViewa())
    
    
@client.bridge_command(description="Set the prefix for this server")
@commands.has_permissions(administrator=True)
async def setprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    server_id = str(ctx.guild.id)
    prefixes[server_id] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.respond(f"The prefix for this server has been set to: {prefix}")

@client5.event
async def on_ready():
   print(f"Successfully logged in as {client5.user.name}")
   await client8.start(TOKEN8)

    
@client.bridge_command(description="Translate your message!")
async def translate(ctx, message, language: discord.Option(choices=["English","Spanish","Portuguese","Chinese","Afrikaans","Arabic","Danish","Esperanto","French","Swedish","Tagalog","Japanese","German","Polish"])):
    await ctx.defer()
    if language in ["English"]:
        translator = Translator(provider="mymemory",to_lang="en")
    elif language in ["Spanish"]:
        translator = Translator(provider="mymemory",to_lang="es")
    elif language in ["Portuguese"]:
        translator = Translator(provider="mymemory",to_lang="pt")
    elif language in ["Chinese"]:
        translator = Translator(provider="mymemory",to_lang="zh")
    elif language in ["Afrikaans"]:
        translator = Translator(provider="mymemory",to_lang="af")
    elif language in ["Arabic"]:
        translator = Translator(provider="mymemory",to_lang="ar")
    elif language in ["Danish"]:
        translator = Translator(provider="mymemory",to_lang="da")
    elif language in ["Esperanto"]:
        translator = Translator(provider="mymemory",to_lang="eo")
    elif language in ["French"]:
        translator = Translator(provider="mymemory",to_lang="fr")
    elif language in ["Swedish"]:
        translator = Translator(provider="mymemory",to_lang="sv")
    elif language in ["Tagalog"]:
        translator = Translator(provider="mymemory",to_lang="tl")
    elif language in ["Japanese"]:
        translator = Translator(provider="mymemory",to_lang="ja")
    elif language in ["German"]:
        translator = Translator(provider="mymemory",to_lang="de")
    elif language in ["Polish"]:
        translator = Translator(provider="mymemory",to_lang="pl")
    translation = translator.translate(f"{message}")
    await ctx.respond(f"{message}\n\n{translation}")


@client.bridge_command(description="See the location of the ISS")
async def iss(ctx):
    url = 'http://api.open-notify.org/iss-now.json'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    latitude = str(data['iss_position']['latitude'])
    longitude = str(data['iss_position']['longitude'])

    geolocator = Nominatim(user_agent="Ultima Bot")
    location = geolocator.reverse(latitude+","+longitude)

    try:
        address = location.raw['address']

        country = address.get('country', '-')
        city = address.get('city', '-')
        state = address.get('state', '-')

        code = address.get('country_code','-')
        zipcode = address.get('postcode','-')

        await ctx.respond(f'The ISS is currently at :\nLatitude: {latitude}\nLongitude: {longitude}\nCountry: {country}\nCity: {city}\nState: {state}\nCountry code: {code}\nZipcode: {zipcode}')

    except:
        await ctx.respond(f'The ISS is currently at :\nLatitude: {latitude}\nLongitude: {longitude}')


@client.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond("This command is currently on cooldown!")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.respond("You do not have the required permissions to do this!")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.respond("I do not have enough permissions to do this!")
    elif isinstance(error, commands.NSFWChannelRequired):
        await ctx.respond("This command can only be used in an NSFW channel!")
    else:
        raise error


api_key = "c08a058955da2e4ba9286a2117aa8897"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

@client.bridge_command(description="Get the weather of a city")
async def weather(ctx, *, city: str):
    city_name = city
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name

    async with aiohttp.ClientSession() as session:
        async with session.get(complete_url) as response:
            x = await response.json()

    channel = ctx.channel
    if x["cod"] != "404":
        async with channel.typing():
            y = x["main"]
            current_temperature = y["temp"]
            current_temperature_celsius = str(round(current_temperature - 273.15))
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]
            f = x["wind"]
            current_windspeed = f["speed"]
            current_winddir = f["deg"]
            weather_description = z[0]["description"]
            embed = discord.Embed(title=f"Weather in {city_name}", color=ctx.guild.me.top_role.color)
            embed.add_field(name="Description", value=f"**{weather_description}**", inline=False)
            embed.add_field(name="Temperature(C)", value=f"**{current_temperature_celsius}°C**", inline=False)
            embed.add_field(name="Humidity(%)", value=f"**{current_humidity}%**", inline=False)
            embed.add_field(name="Atmospheric Pressure(hPa)", value=f"**{current_pressure}hPa**", inline=False)
            embed.add_field(name="Wind Direction", value=f"**{current_winddir}**", inline=False)
            embed.add_field(name="Wind Speed", value=f"**{current_windspeed} m/s**", inline=False)
            embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            await ctx.respond(embed=embed)
    else:
        await ctx.respond("City not found.")

@client.bridge_command()
@commands.is_owner()
async def serverlist(ctx):
    activeservers=client.guilds
    embed=discord.Embed(title="Server list")
    marc = client.get_user(719527356368289802)
    for guild in activeservers:
        embed.add_field(name=f"{guild.name}", value=f"{guild.member_count} members")
    if ctx.author.id==719527356368289802:
        await ctx.respond(embed=embed)
    elif ctx.author.id==763066260233650226:
        await ctx.respond(embed=embed)
    else:
        await ctx.respond("Insufficent permissions")
        

@client.bridge_command(aliases=['yt' ,'ytcmd'], description="Search for a youtube video")
async def ytsearch(ctx, *, search1):
  search = search1
  search = search.replace(" ", "+")

  html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search)
  video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

        
  await ctx.respond("https://www.youtube.com/watch?v=" + video_ids[0])

my_pages = [
    Page(
        embeds=[
            discord.Embed(title="Ultima", description="Ultima is a multipurpose bot offering economy, automod, moderation, fun & utility commands, ticketing, polls and much more!\n\nMake sure to vote for our bot on top.gg: https://top.gg/bot/1113874631489753148\n\nIf you need support, join our support server: https://discord.gg/HHxRfnYEZb"),
        ],
    ),
    Page(
        embeds=[
            discord.Embed(title=":red_circle: Main commands :red_circle:", description="**/random color\n/random number\n/help\n/kick\n/ban\n/purge\n/dog\n/cat\n/fatcat\n/fatdog\n/giveaway\n/fact\n/manga\n/anime\n/membercount\n/invite\n/creroll\n/alimit\n/nick\n/nickscan\n/reroll\n/rps\n/serverinfo\n/ask\n/threat\n/warn\n/uptime\n/abuse\n/challenge\n/whois\n/avatar\n/record start\n/record stop\n/ticketing**"),
        ],
    ),
    Page(
        embeds=[
           discord.Embed(title=":moneybag: Economy commands :moneybag:", description="**/balance\n/memberbalance\n/inventory\n/memberinventory\n/beg\n/daily\n/shop\n/buy\n/rob\n/pay\n/deposit\n/withdraw\n/set\n/robmember\n/donate\n/work\n/leaderboard**")
        ],
    ),
    Page(
        embeds=[
            discord.Embed(
                title="Full command list.",
                description="For a full list of commands, please visit http://fetchbot.org/commands",
            )
        ],
    ),
]

@client.bridge_command(description="Ultima help")
async def help(ctx):
   paginator = Paginator(pages=my_pages)
   await paginator.respond(ctx.interaction)


@client.bridge_command(aliases=['ai'], description="Chat with the Ultima AI")
async def gpt(ctx, query):
  await ctx.defer()
  query2 = f"You are a discord bot developed by Marc13, trembanto and UmayKamaboko. Act mean and sarcastic, but if someone asks you who you were made by, respond with Marc13 trembanto and Umay, anyways, you are not here to provide helpful information, with that in mind respond to the following: {query}"
  response = openai.Completion.create(
  		model="text-davinci-003",
  		prompt=query,
  		temperature=0.3,
  		max_tokens=4000,
  		top_p=1,
  		frequency_penalty=1,
  		presence_penalty=1,
  		stop=[" Human:", " AI:"]
		)
  text = response['choices'][0]['text']
  for item in ["hi", "hello", "hey"]:
     if item.lower() in query:
        text = "Hey, what's up?"
  await ctx.respond(text)
  
@client.bridge_command(description="Get bot's latency")
async def ping(ctx):
    latency = (str(client.latency)).split('.')[1][1:3]
    await ctx.respond(f"Pong! Replied in {latency} ms")
    
@client.bridge_command(description="Host a giveaway")
@commands.has_permissions(administrator=True)
async def giveaway(ctx):
    await ctx.respond(
        "Hello . Please answer to these questions within 15 Seconds to Start the giveaway."
    )

    await asyncio.sleep(2)

    questions = [
        "Please mention the channel to host the giveaway : ",
        "What should be the duration of the giveaway? (1s,1m,1h,1d,...)",
        "What is the prize of this giveaway?"
    ]
    answers = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    for i in questions:
        await ctx.respond(i)
        try:
            msg = await client.wait_for('message', timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send(
                'You didn\'t answer in time, please be quicker next time!')
            return
        else:
            answers.append(msg.content)

    try:
        c_id = int(answers[0][2:-1])

    except:
        await ctx.send(
            f"You didn't mention a channel properly . Do it like this {ctx.channel.mention} ."
        )
        return

    channel = client.get_channel(c_id)
    time = convert(answers[1])
    if time == -1:
        await ctx.send(
            f"You didn't answer the time with a proper unit . Use (S|M|H|D) . Ex : 5m ( 5 Minutes )"
        )
        return
    elif time == -2:
        await ctx.send("Time must be a number !")
        return
    prize = answers[2]

    await ctx.send(
        f"The giveaway will be in {channel.mention} and will last for {answers[1]} ."
    )

    embed = discord.Embed(title=":tada: **Giveaway!** :tada:",
                          description=f"{prize}",
                          color=ctx.author.color)
    embed.add_field(name="Hosted by:", value=ctx.author.mention)
    embed.set_footer(text=f"Ends in {answers[1]} !")
    my_msg = await channel.send(embed=embed)

    await my_msg.add_reaction("🎉")
    await asyncio.sleep(time)
    try:
        new_msg = await channel.fetch_message(my_msg.id)
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(client.user))
        winner = random.choice(users)

        await channel.send(f"Congratulations! {winner.mention} won {prize}!")
    except:
        await channel.send(
            "Giveaway ended and there were no winners because nobody reacted :pensive:"
        )
        return


def convert(time):
    pos = ["s", "m", "h", "d"]

    time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}
    unit = time[-1]
    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2

    return val * time_dict[unit]




@client.bridge_command(aliases=["mc", "members"],
                description="Get the current membercount in this server")
async def membercount(ctx):

    a = ctx.guild.member_count
    b = discord.Embed(title=f"Members in {ctx.guild.name}",
                      description=a,
                      color=discord.Color((0xffff00)))
    await ctx.respond(embed=b)

    
@client.bridge_command(description="Sync commands")
@commands.is_owner()
async def sync(ctx):
    await client.sync_commands(force=True)
    await ctx.respond("Successfully resynced client commands")

@client.bridge_command(description="Send a invite link for Ultima")
async def invite(ctx):
    await ctx.respond(
        "You can invite Ultima here: https://discord.com/api/oauth2/authorize?client_id=935860231051829258&permissions=8&scope=bot"
    )


@client.bridge_command(pass_context=True, description="Change a member's nick")
@commands.has_permissions(moderate_members=True)
async def nick(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)
    await ctx.respond(f'Successfully changed {member.mention}s nick')

@client.bridge_command(description="Reroll a giveaway")
@commands.has_permissions(administrator=True)
async def reroll(ctx, channel: discord.TextChannel, id_):
    if channel == None:
        await ctx.respond("Please mention a channel.")
        return
    if id_ == None:
        await ctx.respond("Please enter the giveaway's ID.")
        return
    try:
        new_msg = await channel.fetch_message(id_)
    except:
        await ctx.respond("The id was entered incorrectly.")
        return

    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await channel.send(f"Congratulations! The new winner is {winner.mention}!")


@client.bridge_command(description="Create an embed!")
async def embed(ctx, title, description, image:discord.Attachment=None, thumbnail:discord.Attachment=None):
    embed = discord.Embed(title=title, description=description)
    if thumbnail is not None:
      embed.set_thumbnail(url=thumbnail)
    if image is not None:
      embed.set_image(url=image)
    await ctx.send(embed=embed)
    await ctx.respond("Successfully created embed!", ephemeral=True)
    
@client.bridge_command(description="Play rock, paper, scissors!")
async def rps(ctx, *, player_choice:discord.Option(choices=['rock', 'paper', 'scissors'])):
    username = str(ctx.author).split('#')[0]
    if player_choice == None:
        await ctx.respond("Please enter rock, paper or scissors.")
        return
    choices1 = ['rock', 'paper', 'scissors']
    bot_choice = random.choice(choices1)
    if player_choice.lower() not in choices1:
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


@client.bridge_command(description="Echo a message")
@commands.has_permissions(administrator=True)
async def echo(ctx, *, message):
    if message == None:
        await ctx.respond("Please enter a message to echo.")
    if ctx.author == client.user:
        return
    await ctx.respond("Successfully performed echo", ephemeral=True)
    await ctx.send(message)
    return

@client.bridge_command(description="Set a reminder")
async def reminder(ctx, time, *, reminder):
    print(time)
    print(reminder)
    user = ctx.author
    embed = discord.Embed(color=0x55a7f7)
    embed.set_footer(text="If you have any questions, suggestions or bug reports, please join our support Discord Server: https://discord.gg/6BHkmhezU4")
    seconds = 0
    if time.lower().endswith("d"):
        seconds += int(time[:-1]) * 60 * 60 * 24
        counter = f"{seconds // 60 // 60 // 24} days"
    if time.lower().endswith("h"):
        seconds += int(time[:-1]) * 60 * 60
        counter = f"{seconds // 60 // 60} hours"
    elif time.lower().endswith("m"):
        seconds += int(time[:-1]) * 60
        counter = f"{seconds // 60} minutes"
    elif time.lower().endswith("s"):
        seconds += int(time[:-1])
        counter = f"{seconds} seconds"
    if seconds == 0:
        embed.add_field(name='Warning',
                        value='Please specify a proper duration')
    elif seconds < 300:
        embed.add_field(name='Warning',
                        value='You have specified a too short duration!\nMinimum duration is 5 minutes.')
    elif seconds > 7776000:
        embed.add_field(name='Warning', value='You have specified a too long duration!\nMaximum duration is 90 days.')
    else:
        await ctx.respond(f"You have successfully set a reminder for {reminder} in {counter}.", ephemeral = True)
        await asyncio.sleep(seconds)
        await ctx.send(f"Hello {ctx.author.mention}, you asked me to remind you about {reminder} {counter} ago.")
        return
    await ctx.respond(embed=embed)

@client.bridge_command(description="Print info about the servers Ultima is used in")
async def servers(ctx):
  embed = discord.Embed()
  dd = len(client.guilds)
  embed.add_field(name=":crown: Server Amount", value=dd)
  await ctx.respond(embed = embed)


@client.bridge_command(description="See how long the bot has been up for")
async def uptime(ctx):
  uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
  embed = discord.Embed(title="Ultima Uptime", description=f"Ultima has been up for {uptime}", color=discord.Colour.green())
  await ctx.respond(embed=embed)




@client.bridge_command(description="Pull the latest version from github and restart the bot")
@commands.is_owner()
async def restart(ctx):
  await ctx.respond("Restarting bot",ephemeral=True)
  await ctx.send("**Performing a planned restart**")
  quit()

@client.bridge_command(description="Get a dad joke")
async def dadjoke(ctx):
    async with aiohttp.ClientSession() as session:
        url = "https://icanhazdadjoke.com/"
        
        headers = {
            'Accept': 'application/json'
        }
        
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                joke = data['joke']
                await ctx.respond(joke)
            else:
                await ctx.respond("Failed to fetch dad joke.")

@client.bridge_command(description="Get a random joke")
async def joke(ctx):
    async with aiohttp.ClientSession() as session:
        url = "https://v2.jokeapi.dev/joke/Any"
        async with session.get(url) as response:
            joke = await response.json()

    if joke['type'] == 'single':
        if "sex" in joke['joke'] or "pussy" in joke['joke']:
            await ctx.respond("Failed to display joke as it was NSFW")
            return
        await ctx.respond(joke['joke'])
    else:
        jok = joke['setup']
        jokk = joke['delivery']
        if "little girl and a fridge?" in jok or "orgasm" in jok or "masturbating" in jok or "sex" in jok or "sex" in jokk or "pussy" in jokk:
            jok = "This joke cannot be displayed as it is NSFW"
            jokk = ":skull:"
        embed = discord.Embed(title=jok, description=jokk)
        await ctx.respond(embed=embed)

@client.bridge_command(description="Get a comic!")
async def comic(ctx, comic:int=None):
  chosen = random.randint(1,1500)
  if comic !=None:
    await ctx.respond(f"https://xkcd.com/{comic}")
    return
  await ctx.respond(f"https://xkcd.com/{chosen}")

@client.bridge_command(description="See how many users someone have invited to a server")
async def invites(ctx, member: discord.Member=None):
  if member == None:
    user = ctx.author
  else:
    user = member
  total_invites = 0
  for i in await ctx.guild.invites():
    if i.inviter == user:
      total_invites += i.uses
  await ctx.respond(f"{user.name} has invited {total_invites} member{'' if total_invites == 1 else 's'}!")

@client.bridge_command(description="Post a meme!")
async def meme(ctx):
  global lastMeme
  memelist=["https://cdn.discordapp.com/attachments/1062778746303680574/1062788689727602898/05c73f974ebbc739fa720e677029f2a5.png","https://cdn.discordapp.com/attachments/1062778746303680574/1062788672887476234/5b1ec1ca8975f12ea2f24f307873f014.png","https://cdn.discordapp.com/attachments/1062778746303680574/1062788385938362388/bde967cac7de114f8d7a587a8862e8a9.png","https://cdn.discordapp.com/attachments/1062778746303680574/1062787897402605619/2c44aa4096423a7f8426dabec159cbf0.png","","https://cdn.discordapp.com/attachments/1062778746303680574/1062787146311794839/37ad1a2814db78e5c7b3fbac7429f371.png" ,"https://cdn.discordapp.com/attachments/1062778746303680574/1062787067068821564/IMG_2220.jpg", "https://cdn.discordapp.com/attachments/1054423887598854165/1062785610164744222/7bf8cbf4f37461087bd8e83f8671edb1.png", "https://cdn.discordapp.com/attachments/1062778746303680574/1062786023622443088/7d7c1a38f1b09d123535945eb22cc7ac.png", "https://cdn.discordapp.com/attachments/1062778746303680574/1062786191822422046/267140c36ae0b4698fb43c28ea35ecc4.png", "https://cdn.discordapp.com/attachments/1062778746303680574/1062786299276308600/5365ad123560b8f2b2100846042adb50.png"]
  meme = random.choice(memelist)
  if meme==lastMeme:
    meme = random.choice(memelist)
    await ctx.respond(meme)
    lastMeme = meme
  else:
    await ctx.respond(meme)
    lastMeme = meme


@client.bridge_command(description="Get a link to the Ultima website")
async def website(ctx):
  await ctx.respond("http://fetchbot.org")

@client.bridge_command(description="Lock a channel!")
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel : discord.TextChannel):
  channel = channel or ctx.channel
  overwrite = channel.overwrites_for(ctx.guild.default_role)
  overwrite.send_messages = False
  await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
  await ctx.respond(f'Successfully locked channel: {channel}.')

@client.bridge_command(description="Unlock a channel!")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel : discord.TextChannel):
  channel = channel or ctx.channel
  overwrite = channel.overwrites_for(ctx.guild.default_role)
  overwrite.send_messages = True
  await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
  await ctx.respond(f'Successfully unlocked channel: {channel}.')

@client.bridge_command(description="Get a random Chuck Norris fact")
async def chuck(ctx):
  async with aiohttp.ClientSession() as session:
    async with session.get("https://api.chucknorris.io/jokes/random") as response:
      if response.status == 200:
        data = await response.json()
        fact = data["value"]
        embed = discord.Embed(title="Chuck Norris Fact", description=fact, color=discord.Color.blue())
        await ctx.respond(embed=embed)
      else:
        await ctx.respond("Failed to fetch a Chuck Norris fact.")

@client.bridge_command(description="Get info about a song from iTunes")
async def song(ctx, *, song_name):
    await ctx.defer()
    async with aiohttp.ClientSession() as session:
        url = "https://itunes.apple.com/search"
        
        params = {
            'term': song_name,
            'entity': 'song',
            'limit': 1
        }
        
        headers = {
            'Accept': 'application/json'
        }
        
        async with session.get(url, params=params, headers=headers) as response:
            if response.status == 200:
                try:
                    data = await response.json(content_type=None)
                    results = data.get('results', [])
                    
                    if results:
                        song_info = results[0]
                        artist_name = song_info.get('artistName', 'Unknown Artist')
                        track_name = song_info.get('trackName', 'Unknown Track')
                        preview_url = song_info.get('previewUrl', '')
                        
                        embed = discord.Embed(title=f"Song Info - {track_name}", color=discord.Color.blue())
                        embed.add_field(name="Artist", value=artist_name, inline=False)
                        embed.add_field(name="Preview URL", value=f"[Click here]({preview_url})", inline=False)
                        
                        await ctx.respond(embed=embed)
                    else:
                        await ctx.respond("No results found for the specified song.")
                except aiohttp.ContentTypeError:
                    await ctx.respond("Failed to fetch song information.")
            else:
                await ctx.respond("Failed to fetch song information.")

@client.bridge_command(description="Start a poll")
async def poll(ctx, poll, reaction1, reaction2, reaction3=None, reaction4=None, reaction5=None):
  polle = discord.Embed(
    title=poll
    
  )
  lol = await ctx.send(embed=polle)
  await lol.add_reaction(reaction1)
  await lol.add_reaction(reaction2)
  await ctx.respond("Poll started", ephemeral=True)
  if reaction3!=None:
    await lol.add_reaction(reaction3)
  if reaction4!=None:
    await lol.add_reaction(reaction4)
  if reaction5!=None:
    await lol.add_reaction(reaction5)


@client.bridge_command(description="Search for a picture!")
async def imagesearch(ctx, image):
  embed = discord.Embed(
    title = 'Image',
    description = 'Your image',
    colour = discord.Colour.purple()
    )
  embed.set_image(url='https://source.unsplash.com/1600x900/?{}'.format(image))            
  embed.set_footer(text=f"{image}")
  await ctx.respond(embed=embed)

@client.bridge_command(description="Look up a github repo or user!")
async def github(ctx,owner,repo=None):
  if repo==None:
    await ctx.respond(f"https://github.com/{owner}")
  else:
    await ctx.respond(f"https://github.com/{owner}/{repo}")


@client.bridge_command(description="Set a slowmode!")
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx,seconds:int):
  await ctx.channel.edit(slowmode_delay=seconds)
  await ctx.respond(f"Successfully set the slowmode delay in this channel to {seconds} seconds!")

@client.bridge_command(description="See how many days ago the bot was created!")
async def createday(ctx):
  your_date = datetime.date(2022, 1, 26)
  today = datetime.date.today()
  delta = (today - your_date).days
  await ctx.respond(f"Ultima was created {delta} days ago")


#ECONOMY COMMANDS BELOW ONLY

@client.bridge_group()
async def economy():
    pass

@economy.command()
async def set(ctx, member:discord.Member, wallet: int, bank: int):
    # Get the user ID from the message author
    user_id = member.id

    # Insert the user's balance into the database
    await db.insert_user_balance(user_id, wallet, bank)

    await ctx.send(f"User balance for {member.mention} has been set: Wallet: {wallet}, Bank: {bank}")

@economy.command(description="See your bank balance!")
async def balance(ctx):
  wallet, bank = await db.get_user_balance(ctx.author.id)

  em = discord.Embed(title=f"{ctx.author.name}'s balance.", color=discord.Color.teal())
  em.add_field(name="Wallet Balance", value=wallet)
  em.add_field(name="Bank Balance", value=bank)
  await ctx.respond(embed=em)

@economy.command(description="See another members' balance")
async def memberbalance(ctx,member:discord.Member):
  wallet, bank = await db.get_user_balance(member.id)

  em = discord.Embed(title=f"{member.name}'s balance.", color=discord.Color.teal())
  em.add_field(name="Wallet Balance", value=wallet)
  em.add_field(name="Bank Balance", value=bank)
  await ctx.respond(embed=em)
  

@economy.command(description="Beg for coins!")
@commands.cooldown(1, 300, commands.BucketType.user)
async def beg(ctx):
  user_id = ctx.author.id

  earnings = random.randint(10, 50)

  await db.add_to_wallet(user_id, earnings)

  await ctx.respond(f"Someone gave you {earnings} credits!")

@economy.command(description="Go to work")
@commands.cooldown(1, 300, commands.BucketType.user)
async def work(ctx):
  user_id = ctx.author.id
  earnings = random.randint(1, 10)
  await db.add_to_wallet(user_id, earnings)
  await ctx.respond(f"You earned {earnings} credits for going to work!")
    
@economy.command(description="Get your daily reward!")
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily(ctx):
  user_id = ctx.author.id

  earnings = random.randint(50, 101)

  await db.add_to_wallet(user_id, earnings)

  await ctx.respond(f"You got {earnings} credits as your daily reward!")

@economy.command(description="Do a bank robbery!")
@commands.cooldown(1, 2000, commands.BucketType.user)
async def rob(ctx):
  user_id = ctx.author.id

  earnings = random.randint(300, 800)

  decider = random.randint(0,1)

  wallet_amt = await db.get_wallet_balance(user_id)

  if decider == 1:
    await ctx.respond(f"You just robbed the bank and got {earnings} credits!")
    await db.add_to_wallet(user_id, earnings)
  else:
    if wallet_amt > 500:
      await ctx.respond("The police managed to catch you when you robbed the bank :pensive: They also took 500 credits from you")
      await db.add_to_wallet(user_id, -500)
    else:
      if wallet_amt > 0:
        await ctx.respond(f"The police managed to catch you when you robbed the bank, and they also took {wallet_amt} credits from you! :pensive:")
        await db.add_to_wallet(user_id, -wallet_amt)
      else:
         await ctx.respond(f"The police managed to catch you when you robbed the bank :pensive:")

@economy.command(description="Give some of your money to another member!")
async def pay(ctx, amount: int, member: discord.Member):
    if amount <= 0:
        return await ctx.respond(":x: Amount must be a positive number!")

    if member == ctx.author:
        return await ctx.respond("It's not a good idea to pay yourself")

    sender_balance = await db.get_wallet_balance(ctx.author.id)

    if amount > sender_balance:
        return await ctx.respond("Please make sure you have enough money in your wallet!")

    # Assuming 'db' is the instance of your database class
    await db.add_to_wallet(ctx.author.id, -amount)
    await db.add_to_wallet(member.id, amount)

    await ctx.respond(f":white_check_mark: Transaction completed! {amount} credits have been transferred to {member.name}")
    

@economy.command(description="Rob another member!")
@commands.cooldown(1, 1000, commands.BucketType.user)
async def robmember(ctx,member:discord.Member):

  earnings = random.randint(100, 500)

  robber_bal = await db.get_wallet_balance(ctx.author.id)
  victim_bal = await db.get_wallet_balance(member.id)

  decider = random.randint(0,1)

  if victim_bal < earnings:
    if victim_bal < 0:
      await ctx.respond("It's not worth it :pensive:")
      return
    elif victim_bal == 0:
      await ctx.respond("It's not worth it :pensive:")
      return
    else:
      earnings = victim_bal

  
  if decider == 1:
    await ctx.respond(f"You just robbed {member} and got {earnings} credits!")
    await db.add_to_wallet(ctx.author.id, earnings)
    await db.add_to_wallet(member.id, -earnings)
  else:
    responselist=[f"{member} knew how to defend themselves and took 100 credits from you instead!", f"{member} killed you and took 100 credits from you!"]
    choice = random.choice(responselist)
    await ctx.respond(choice)
    if robber_bal > 100:
      await db.add_to_wallet(ctx.author.id, -100)
      await db.add_to_wallet(member.id, 100)
    else:
       return
      
    

@economy.command(description="Transfer money from your wallet to the bank")
async def deposit(ctx,amount:int):
  dep_bal = await db.get_wallet_balance(ctx.author.id)
  if dep_bal < amount:
     return await ctx.respond("Make sure you have enough credits in your wallet!")
  await db.add_to_bank(ctx.author.id, amount)
  await db.add_to_wallet(ctx.author.id, -amount)

  await ctx.respond(f":moneybag: You just deposited {amount} credits.")

@economy.command(description="Transfer money from your bank to the wallet")
async def withdraw(ctx,amount:int):
  dep_wallet, dep_bank = await db.get_user_balance(ctx.author.id)
  if dep_bank < amount:
     return await ctx.respond("Make sure you have enough credits in your bank!")
  await db.add_to_bank(ctx.author.id, -amount)
  await db.add_to_wallet(ctx.author.id, amount)

  await ctx.respond(f":moneybag: You just deposited {amount} credits.")

@economy.command(description="Show the leaderboard of users with the most credits")
async def leaderboard(ctx):
    query = "SELECT user_id, (wallet + bank) AS total_amount FROM economy_balance ORDER BY total_amount DESC LIMIT 10"

    async with db.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(query)
            results = await cursor.fetchall()

    leaderboard_embed = discord.Embed(title="Leaderboard", color=discord.Color.gold())

    for index, (user_id, total_amount) in enumerate(results, start=1):
        user = client.get_user(user_id)
        if user:
            leaderboard_embed.add_field(name=f"{index}. {user.name}", value=f"Total Amount: {total_amount}", inline=False)
        else:
            leaderboard_embed.add_field(name=f"{index}. Unknown User", value=f"Total Amount: {total_amount}", inline=False)

    await ctx.respond(embed=leaderboard_embed)

@client5.bridge_command()
async def fleetapp(ctx):
  embed=discord.Embed(title="Applications", description="Please press one of the buttons below if you wish to apply for either the official Cremorrah Fleet, or to become a moderator.", color=discord.Colour.green())
  await ctx.send(embed=embed, view=DeltaApp())

client.load_extension('cogs.moderation')
client.load_extension('cogs.fun')
client.load_extension('cogs.tools')
client.load_extension('cogs.automod')
client.load_extension('cogs.levelling')
client.load_extension('cogs.serverlogs')
client.load_extension('cogs.welcome')
client.load_extension('cogs.report')
client.load_extension('cogs.autorole')
client.load_extension('cogs.starboard')
client.load_extension('cogs.afk')
client.load_extension('cogs.image')
client.load_extension('cogs.recording')
client.load_extension('cogs.tags')

client5.load_extension('DeltaBot.maindeltabot')

async def bot_main():
    print("Bot starting...")
    await client.start(TOKEN)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(bot_main()))