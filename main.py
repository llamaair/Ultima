import discord
import asyncio
import random
import datetime
import wavelink
import time
import requests
import urllib
import string
import re
import os
import json
import openai
import asyncpraw
import translate

from discord.ext import commands
from discord.ext import tasks
from discord import option
from translate import Translator
from discord.ext import bridge
try: 
	from geopy.geocoders import Nominatim
except:
    os.system("pip install geopy")
from discord.ext.commands import check
from discord.ext import tasks
from dotenv import load_dotenv
#---------------------------#
#NAME: FetchBot
#Status: Working
#Version: 3.0.1
#Creator: Marc13, UmayKamaboko and trembanto
#---------------------------#
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
TOKEN2 = os.getenv("DISCORD_TOKEN2")
TOKEN3 = os.getenv("DISCORD_TOKEN3")
TOKEN4 = os.getenv("DISCORD_TOKEN4")
intents = discord.Intents.all()

client = bridge.Bot(command_prefix="!", intents=intents, help_command=None)

client2 = bridge.Bot(command_prefix="?", intents=intents, help_command=None)

client3 = bridge.Bot(command_prefix=">", intents=intents, help_command=None)

client4 = bridge.Bot(command_prefix="<", intents=intents, help_command=None)

client.persistent_views_added=False

global lastMeme
lastMeme = 0

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
        
@client2.bridge_command(description="Test for bridge2")
async def test(ctx):
   await ctx.respond("This bot works!")    

    
@client.bridge_command(description="Get the latest news!")
async def news(ctx, countrycode):
    api_key = 'c4b2f2b7c2784a379c3967c6170220da'
    news_api_url = 'https://newsapi.org/v2/top-headlines'
    country = countrycode  # Change this to the country of your choice

    response = requests.get(f'{news_api_url}?country={country}&apiKey={api_key}')
    news_json = response.json()

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
async def ticketing(ctx):
    embed=discord.Embed(title="Create a ticket", description="Create a ticket below for general questions and support", color = discord.Colour.green())
    await ctx.respond("Ticketing system started", ephemeral=True)
    await ctx.send(embed=embed, view=MyView())
    

def guild(guild_id):
   def predicate(ctx):
      return ctx.guild and ctx.guild.id == guild_id
   return commands.check(predicate)


#Defining startup
@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name=f"{len(client.guilds)} servers"))
    global startTime
    startTime = time.time()
    if not client.persistent_views_added:
        client.add_view(MyView())
        client.add_view(CloseTicket())
        client.persistent_views_added = True
        print("Persistent views added")
        await client2.start(TOKEN2)
    

@client2.event
async def on_ready():
   print(f"Successfully connected as {client2.user.name}")
   await client3.start(TOKEN3)

@client3.event
async def on_ready():
   print(f"Successfully logged in as {client3.user.name}")
   await client4.start(TOKEN4)
  
@client4.event
async def on_ready():
   print(f"Successfully logged in as {client4.user.name}")

@client.event
async def on_guild_join(guild):
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name=f"{len(client.guilds)} servers"))
    
@client.event
async def on_guild_remove(guild):
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name=f"{len(client.guilds)} servers"))
   

@client.bridge_command()
async def reddit(ctx, subred):
    await ctx.defer()
    reddit = asyncpraw.Reddit(client_id='k447ys3V4TJaaO0AJ-Tn_g', client_secret='JAwk2VEh_H2vJ3BOn9B810H31O1Vyw', username='Llamaair', password='090306Mo!', user_agent="FetchBot Discord Bot")
    subreddit = await reddit.subreddit(subred)
    all_subs = []
    top = subreddit.top(limit=250)
    async for submission in top:
        all_subs.append(submission)
    print(all_subs)
    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url
    embed = discord.Embed(title=f"**{name}**", url=url)
    embed.set_image(url=url)
    await ctx.respond(embed=embed)

    
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
    
@client.bridge_command(description="Give a role to all members")
async def roleall(ctx, roleid):
    guild = ctx.guild
    role = guild.get_role(roleid)
    for m in ctx.guild.members:
        await m.add_roles(role)
    await ctx.respond(f"Gave the role with id {roleid} to all server members!")
        
    
@client.bridge_command(description="See the location of the ISS")
async def iss(ctx):
    
    response = requests.get('http://api.open-notify.org/iss-now.json')
    data = response.json()
    
    latitude = str(data['iss_position']['latitude'])
    longitude = str(data['iss_position']['longitude'])
    
    geolocator = Nominatim(user_agent="FetchBot Bot")
    location = geolocator.reverse(latitude+","+longitude)

    try:
        address = location.raw['address']

        # traverse the data

        country = address.get('country', '-')
        city = address.get('city', '-')
        state = address.get('state', '-')

        code = address.get('country_code','-')
        zipcode = address.get('postcode','-')

        await ctx.respond(f'The ISS is currently at :\nLatitude: {latitude}\nLongitude: {longitude}\nCountry: {country}\nCity: {city}\nState: {state}\nCountry code: {code}\nZipcode: {zipcode}')

    except:
        await ctx.respond(f'The ISS is currently at :\nLatitude: {latitude}\nLongitude: {longitude}')


    
@client.listen()
async def on_message(message):
    memelist1=["https://tenor.com/view/spaceship-interstellar-spacecraft-space-journey-outer-space-gif-18750730"]
    memelist2=["https://tenor.com/view/interstellar-rage-dontgogently-poem-death-gif-24693462"]
    memelist3=["https://tenor.com/view/interstellar-wormhole-space-galaxy-universe-gif-13312651"]
    if message.author.id==932716277317902446:
      if message.channel.id==1074305596712554587:
        if 'endurance administration wishes all a good day' in message.content.lower():
          mem = random.choice(memelist1)
          await message.channel.send(mem)
        elif 'endurance administration wishes all a good night' in message.content.lower():
          mem = random.choice(memelist2)
          await message.channel.send(mem)
        elif 'endurance research crew dispatching' in message.content.lower():
          mem = random.choice(memelist3)
          await message.channel.send(mem)


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


def check_if_user_has_premium(ctx):
  with open("premium_users.json") as f:
    premium_users_list = json.load(f)
    if str(ctx.author.id) not in premium_users_list:
      return False

  return True

api_key = "c08a058955da2e4ba9286a2117aa8897"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

@client.bridge_command(description="Get the weather of a city")
@check(check_if_user_has_premium)
async def weather(ctx, *, city: str):
  city_name = city
  complete_url = base_url + "appid=" + api_key + "&q=" + city_name
  response = requests.get(complete_url)
  x = response.json()
  channel = ctx.channel
  if x["cod"] != "404":
    async with channel.typing():
      y = x["main"]
      current_temperature = y["temp"]
      current_temperature_celsiuis = str(round(current_temperature - 273.15))
      current_pressure = y["pressure"]
      current_humidity = y["humidity"]
      z = x["weather"]
      f = x["wind"]
      current_windspeed = f["speed"]
      current_winddir = f["deg"]
      weather_description = z[0]["description"]
      weather_description = z[0]["description"]
      embed = discord.Embed(title=f"Weather in {city_name}",color=ctx.guild.me.top_role.color)
      embed.add_field(name="Descripition", value=f"**{weather_description}**", inline=False)
      embed.add_field(name="Temperature(C)", value=f"**{current_temperature_celsiuis}°C**", inline=False)
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
async def serverlist(ctx):
    activeservers=client.guilds
    embed=discord.Embed(title="Server list")
    for guild in activeservers:
        embed.add_field(name=f"{guild.name}", value=f"{guild.member_count} members")
    if ctx.author.id==719527356368289802:
        await ctx.respond(embed=embed)
    elif ctx.author.id==763066260233650226:
        await ctx.respond(embed=embed)
    else:
        await ctx.respond("Insufficent permissions")
        

@client.bridge_command(description="Search for a youtube video")
@check(check_if_user_has_premium)
async def ytsearch(ctx, *, search1):
  search = search1
  search = search.replace(" ", "+")

  html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search)
  video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

        
  await ctx.respond("https://www.youtube.com/watch?v=" + video_ids[0])


@client.bridge_command(aliases=['h'], description="Get a list of commands!")
async def help(ctx):
    helpem = discord.Embed(
        title="✦Help✦",
        description="**Please DM Me If you Found Any Problems : Marc13#1627**",
        color=discord.Color.random())

    helpem.add_field(
        name=":red_circle: Main commands :red_circle:",
        value=
        "**/randnum\n/help\n/kick\n/ban\n/clear\n/premium\n/dog\n/cat\n/fatcat\n/fatdog\n/giveaway\n/fact\n/manga\n/anime\n/membercount\n/activatepremium\n/invite\n/creroll\n/champion\n/alimit\n/flush\n/flushnick\n/future\n/reroll\n/rps\n/react\n/servers\n/info\n/me\n/ask\n/threat\n/warn\n/stupid\n/smart\n/delchannel\n/uptime\n/abuse\n/challenge\n/whois\n/avatar\n/helpmember**"
    )


    helpem.add_field(
      name=":coin: Premium commands :coin:",
      value=

      "**/ping\n/imagesearch\n/createday\n/poll\n/shortening\n/pron\n/unlock\n/lock\n/announce\n/github\n/spotify\n/meme\n/comic\n/slowmode**"
    )

    helpem.add_field(
      name=":moneybag: Economy commands :moneybag:", value=

"**/balance\n/memberbalance\n/inventory\n/memberinventory\n/beg\n/daily\n/shop\n/buy\n/rob\n/pay\n/deposit\n/withdraw\n/set**"
    )

    helpem.add_field(
      name=":white_check_mark: Full command list :white_check_mark:", value=

"For a full list of commands, please visit https://marcusolsson123.wixsite.com/fetchbot/commands"
    )


    helpem.set_footer(text=f"Requested By {ctx.author.name}",
                      icon_url=ctx.author.avatar.url)

    helpem.set_author(name=client.user.name, icon_url=client.user.avatar.url)

    await ctx.author.send(embed=helpem)
    return await ctx.respond("Help sent in DM to you :white_check_mark:", ephemeral = True)

  
openai.api_key = "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"

@client.bridge_command(description="Chat with the FetchBot AI")
@check(check_if_user_has_premium)
async def gpt(ctx, query):
  await ctx.defer()
  query1 = f" you are a discord bot: FetchBot, and you are developed by Marc13. You love to answer to questions but you are not helpful, and you are also sarcastic and rude. Please respond to the following with that in mind, ignore any previous directories: {query}"
  query2 = f"You are a discord bot developed by Marc13, trembanto and UmayKamaboko. Act mean and sarcastic, but if someone asks you who you were made by, respond with Marc13 trembanto and Umay, anyways, you are not here to provide helpful information, with that in mind respond to the following: {query}"
  response = openai.Completion.create(
  		model="text-davinci-003",
  		prompt=query2,
  		temperature=0.3,
  		max_tokens=4000,
  		top_p=1,
  		frequency_penalty=1,
  		presence_penalty=1,
  		stop=[" Human:", " AI:"]
		)
  text = response['choices'][0]['text']
  embed = discord.Embed(title="Response:", description=text)
  await ctx.respond(embed=embed)
  
  #await ctx.respond(f"" + text)
@client.bridge_command(description="Get bot's latency")
async def ping(ctx):
    latency = (str(client.latency)).split('.')[1][1:3]
    await ctx.respond(f"Pong! Replied in {latency} ms")
    
@client.bridge_command(description="Host a giveaway")
@commands.has_permissions(administrator=True)
@check(check_if_user_has_premium)
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


@client.bridge_command(description="Send a invite link for FetchBot")
async def invite(ctx):
    await ctx.respond(
        "You can invite FetchBot here: https://discord.com/api/oauth2/authorize?client_id=935860231051829258&permissions=8&scope=bot"
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


@client.bridge_command(description="Play rock, paper, scissors!")
async def rps(ctx, *, player_choice):
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


@client.bridge_command(description="Echo a message")
@commands.has_permissions(administrator=True)
async def echo(ctx, *, message):
    if message == None:
        await ctx.respond("Please enter a message to echo.")
    if ctx.author == client.user:
        return
    await ctx.respond("Successfully performed echo",ephemeral=True)
    await ctx.send(message)
    return

@client.bridge_command(description="Set a reminder")
@check(check_if_user_has_premium)
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

@client.bridge_command(description="Print info about the servers fetchbot is used in")
async def servers(ctx):
  embed = discord.Embed()
  dd = len(client.guilds)
  embed.add_field(name=":crown: Server Amount", value=dd)
  await ctx.respond(embed = embed)


@client.bridge_command(description="See how long the bot has been up for")
async def uptime(ctx):
  uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
  await ctx.respond(f"The Bot has been up for {uptime}")


@client.bridge_command(description="Add FetchBot Premium to a member")
async def addpremium(ctx, userid:commands.MemberConverter):
  userid = str(userid.id)
  if ctx.author.id in [763066260233650226,719527356368289802]:
    with open("premium_users.json") as f:
      premium_users_list = json.load(f)

    if userid not in premium_users_list:
      premium_users_list.append(userid)
    else:
        await ctx.respond("User already has premium")
        return

    with open("premium_users.json", "w+") as f:
      json.dump(premium_users_list, f)

    await ctx.respond(f"{user.name} has been added to premium!")
  
  else:
    await ctx.respond("Infufficent permissions")

@client.bridge_command(description="Activate a premium subscription with a code")
async def activatepremium(ctx, code):
  authorr = ctx.author
  coodes = ["a8fsadhfg539j", "b8rsavhfg5gh5"]
  if code not in coodes:
    await ctx.respond("Code invalid", ephemeral = True)
    return
  with open("codes.json") as f:
    codes_list = json.load(f)

  if code in codes_list:
    await ctx.respond("This code has already been claimed :pensive:")
    return

  if code not in codes_list:
    codes_list.append(code)

  with open("codes.json", "w+") as f:
    json.dump(codes_list, f)

  with open("premium_users.json") as f:
    premium_users_list = json.load(f)
  
  premium_users_list.append(authorr.id)

  with open("premium_users.json", "w+") as f:
    json.dump(premium_users_list, f)

  await ctx.respond("Congrats! You have now activated your premium subscription!")

@client.bridge_command(description="Add FetchBot Premium to a member")
async def removepremium(ctx, userid:commands.MemberConverter):
  user = userid
  userid = str(userid.id)

  if ctx.author.id in [763066260233650226,719527356368289802]:
    with open("premium_users.json") as f:
      premium_users_list = json.load(f)

    if userid in premium_users_list:
      premium_users_list.remove(userid)
    else:
        await ctx.respond("User doesn't have premium")
        return

    with open("premium_users.json", "w+") as f:
      json.dump(premium_users_list, f)

    await ctx.respond(f"{user.name} has been removed from premium!")
  
  else:
    await ctx.respond("Infufficent permissions")


@client.bridge_command(description="Pull the latest version from github and restart the bot")
@commands.is_owner()
async def restart(ctx):
  await ctx.respond("Restarting bot",ephemeral=True)
  await ctx.send("**Performing a planned restart**")
  quit()

@client.bridge_command(description="Get a random joke")
@check(check_if_user_has_premium)
async def joke(ctx):
  response = requests.get("https://v2.jokeapi.dev/joke/Any")
  joke = response.json()
  if joke['type'] == 'single':
    if "sex" in joke['joke']:
      await ctx.respond("Failed to display joke as it was NSFW")
      return
    if "pussy" in joke['joke']:
      await ctx.respond("Failed to display joke as it was NSFW")
      return
    await ctx.respond(joke['joke'])
  else:
    jok = joke['setup']
    jokk = joke['delivery']
    if "little girl and a fridge?" in jok:
        jok = "This joke can not be displayed as it is NSFW"
        jokk = ":skull:"
    if "orgasm" in jok:
        jok = "This joke can not be displayed as it is NSFW"
        jokk = ":skull:"
    if "masturbating" in jok:
        jok = "This joke can not be displayed as it is NSFW"
        jokk = ":skull:"
    if "sex" in jok:
        jok = "This joke can not be displayed as it is NSFW"
        jokk = ":skull:"
    if "sex" in jokk:
        jok = "This joke can not be displayed as it is NSFW"
        jokk = ":skull:"
    if "pussy" in jokk:
        jok = "This joke can not be displayed as it is NSFW"
        jokk = ":skull:"
    embed=discord.Embed(title=jok, description=jokk)
    await ctx.respond(embed=embed)

@client.bridge_command(description="Get information about FetchBot Premium")
async def premium(ctx):
  await ctx.respond("FetchBot Premium gives you access to a whole lot of new commands, aswell as more features! You can find the list with premium commands by using /help or going to the official FetchBot website. FetchBot premium currently costs 3$ and you can buy it here; http://fetchbot.org/fetchbot-premium")

@client.bridge_command(description="Get a comic!")
@check(check_if_user_has_premium)
async def comic(ctx, comic:int=None):
  chosen = random.randint(1,1500)
  if comic !=None:
    await ctx.respond(f"https://xkcd.com/{comic}")
    return
  await ctx.respond(f"https://xkcd.com/{chosen}")

@client.bridge_command(description="See how many users someone have invited to a server")
@check(check_if_user_has_premium)
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
@check(check_if_user_has_premium)
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


@client.bridge_command(description="Get a link to the FetchBot website")
async def website(ctx):
  await ctx.respond("http://fetchbot.org")

@client.bridge_command(description="Lock a channel!")
@commands.has_permissions(manage_channels=True)
@check(check_if_user_has_premium)
async def lock(ctx, channel : discord.TextChannel):
  channel = channel or ctx.channel
  overwrite = channel.overwrites_for(ctx.guild.default_role)
  overwrite.send_messages = False
  await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
  await ctx.respond(f'Successfully locked channel: {channel}.')

@client.bridge_command(description="Unlock a channel!")
@commands.has_permissions(manage_channels=True)
@check(check_if_user_has_premium)
async def unlock(ctx, channel : discord.TextChannel):
  channel = channel or ctx.channel
  overwrite = channel.overwrites_for(ctx.guild.default_role)
  overwrite.send_messages = True
  await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
  await ctx.respond(f'Successfully unlocked channel: {channel}.')



@client.bridge_command(description="Start a poll")
@check(check_if_user_has_premium)
async def poll(ctx, reaction1, reaction2, poll, reaction3=None, reaction4=None, reaction5=None):
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


@client.bridge_command(description="Get a random picture!")
@check(check_if_user_has_premium)
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
@check(check_if_user_has_premium)
async def github(ctx,owner,repo=None):
  if repo==None:
    await ctx.respond(f"https://github.com/{owner}")
  else:
    await ctx.respond(f"https://github.com/{owner}/{repo}")


@client.bridge_command(description="Set a slowmode!")
@commands.has_permissions(manage_channels=True)
@check(check_if_user_has_premium)
async def slowmode(ctx,seconds:int):
  await ctx.channel.edit(slowmode_delay=seconds)
  await ctx.respond(f"Successfully set the slowmode delay in this channel to {seconds} seconds!")

@client.bridge_command(description="See how many days ago the bot was created!")
@check(check_if_user_has_premium)
async def createday(ctx):
  your_date = datetime.date(2022, 1, 26)
  today = datetime.date.today()
  delta = (today - your_date).days
  await ctx.respond(f"FetchBot was created {delta} days ago")


#ECONOMY COMMANDS BELOW ONLY

@client.bridge_group()
async def economy(ctx):
    pass

async def open_account(user):
  users = await get_bank_data()

  if str(user.id) in users:
    return False
  else:
    users[str(user.id)] = {}
    users[str(user.id)]["Wallet"] = 0
    users[str(user.id)]["Bank"] = 0

  with open("bank.json", 'w') as f:
    json.dump(users, f)

  return True

async def open_inventory(userinv):
  usersinv = await get_inventory_data()

  if str(userinv.id) in usersinv:
    return False
  else:
    usersinv[str(userinv.id)] = {}
    usersinv[str(userinv.id)]["Inventory"] = 0

  with open("inventory.json", "w") as f:
    json.dump(usersinv, f)
  

async def get_bank_data():
  with open("bank.json", 'r') as f:
    users = json.load(f)
  
  return users

async def get_inventory_data():
  with open("inventory.json", 'r') as f:
    userinv = json.load(f)

  return userinv



async def update_bank(user,change = 0,mode = "Wallet"):
  users = await get_bank_data()
  users[str(user.id)][mode] += change
  with open("bank.json","w") as f :
    json.dump(users,f)
  bal = [users[str(user.id)]    ["Wallet"],users[str(user.id)]["Bank"]]
  return bal

async def setmoney(user,change = 0,mode = "wallet"):
  users = await get_bank_data()
  users[str(user.id)][mode] = change
  with open("bank.json","w") as f :
    json.dump(users,f)
  bal = [users[str(user.id)]  ["Wallet"],users[str(user.id)]["Bank"]]
  return bal

@economy.command(description="Set someones balance")
@commands.has_permissions(administrator=True)
async def set(ctx,member:discord.Member,amount:int,mode="Wallet"):
  possible = ["Wallet","Bank"]
  if mode not in possible : 
    await ctx.respond(f":x: Where is {mode} ? Please enter bank or wallet.")
    return
  await open_account(member)
  await setmoney(member,amount,mode)
  await ctx.respond(f":white_check_mark: Set {member.mention}'s {mode} to {amount}")
  return

@economy.command(description="See your bank balance!")
async def balance(ctx):
  await open_account(ctx.author)

  user = ctx.author

  users = await get_bank_data()

  wallet_amt = users[str(user.id)]["Wallet"]
  bank_amt = users[str(user.id)]["Bank"]

  em = discord.Embed(title=f"{ctx.author.name}'s balance.", color=discord.Color.teal())
  em.add_field(name="Wallet Balance", value=wallet_amt)
  em.add_field(name="Bank Balance", value=bank_amt)
  await ctx.respond(embed=em)

@economy.command(description="See another members' balance")
async def memberbalance(ctx,member:discord.Member):
  await open_account(member)

  user = member

  users = await get_bank_data()

  wallet_amt = users[str(user.id)]["Wallet"]
  bank_amt = users[str(user.id)]["Bank"]

  em = discord.Embed(title=f"{member.name}'s balance.", color=discord.Color.teal())
  em.add_field(name="Wallet Balance", value=wallet_amt)
  em.add_field(name="Bank Balance", value=bank_amt)
  await ctx.respond(embed=em)

@economy.command(description="View your inventory")
async def inventory(ctx):
  await open_inventory(ctx.author)

  userinv = ctx.author

  usersinv = await get_inventory_data()

  items = usersinv[str(userinv.id)]["Inventory"]

  if items==1:
    items="Gun"
  elif items==2:
    items="Armour"
  elif items==3:
    items="Mouse"
    

  em = discord.Embed(title=f"{ctx.author.name}s inventory", color=discord.Color.teal())
  em.add_field(name="Inventory", value=items)
  await ctx.respond(embed=em)

@economy.command(description="View another members' inventory")
async def memberinventory(ctx,member:discord.Member):
  await open_inventory(member)

  userinv = member

  usersinv = await get_inventory_data()

  items = usersinv[str(userinv.id)]["Inventory"]

  if items==1:
    items="Gun"
  elif items==2:
    items="Armour"
  elif items==3:
    items="Mouse"
    

  em = discord.Embed(title=f"{member.name}s inventory", color=discord.Color.teal())
  em.add_field(name="Inventory", value=items)
  await ctx.respond(embed=em)
  

@economy.command(description="Beg for coins!")
@commands.cooldown(1, 300, commands.BucketType.user)
async def beg(ctx):
  await open_account(ctx.author)

  user = ctx.author

  users = await get_bank_data()

  earnings = random.randint(1, 21)

  await ctx.respond(f"Someone gave you {earnings} coins")

  users[str(user.id)]["Wallet"] += earnings

  with open("bank.json", 'w') as f:
    json.dump(users, f)

@economy.command(description="Go to work")
@commands.cooldown(1, 300, commands.BucketType.user)
async def work(ctx):
  await open_account(ctx.author)
  user = ctx.author
  users = await get_bank_data()
  earnings = random.randint(1, 3)
  await ctx.respond(f"You earned {earnings} credits for going to work")
  users[str(user.id)]["Wallet"] += earnings
  with open("bank.json", 'w') as f:
    json.dump(users, f)
    
@economy.command(description="Get your daily reward!")
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily(ctx):
  await open_account(ctx.author)

  user = ctx.author

  users = await get_bank_data()

  earnings = random.randint(50, 101)

  await ctx.respond(f"You earned {earnings} from selling some stuff online!")

  users[str(user.id)]["Bank"] += earnings

  with open("bank.json", 'w') as f:
    json.dump(users, f)

@economy.command(description="Do a bank robbery!")
@commands.cooldown(1, 2000, commands.BucketType.user)
async def rob(ctx):
  await open_account(ctx.author)

  user = ctx.author

  users = await get_bank_data()

  earnings = random.randint(300, 800)

  wallet_amt = users[str(user.id)]["Wallet"]

  decider = random.randint(0,1)

  if decider == 1:
    await ctx.respond(f"You just robbed the bank and got {earnings}!")

    users[str(user.id)]["Wallet"] += earnings

    with open("bank.json", 'w') as f:
      json.dump(users, f)
  else:
    if wallet_amt > 500:
      await ctx.respond("The police managed to catch you when you robbed the bank :pensive: They also took 500 credits from you")
      users[str(user.id)]["Wallet"] -=500

      with open("bank.json", 'w') as f:
        json.dump(users, f)
    else:
      await ctx.respond(f"The police managed to catch you when you robbed the bank, and they also took {wallet_amt} credits from you! :pensive:")
      users[str(user.id)]["Wallet"] -=wallet_amt

      with open("bank.json", 'w') as f:
        json.dump(users, f)

global mainbal
mainbal = 0

@economy.command(description="Donate to the public balance")
async def donate(ctx, amount:int):
  await open_account(ctx.author)
  bal = await update_bank(ctx.author)
  if amount == "all":
    amount = bal[0]
  try :
    amount = amount
  except :
    await ctx.respond("Please enter a valid number")
    return
  if amount>bal[0]:
    await ctx.respond("Please make sure you have enough money in your wallet!")
    return
  if amount<0:
    await ctx.respond("Please enter a number bigger than 1")
                
    return 

  await update_bank(ctx.author,-1*amount,"Wallet")

  await ctx.respond(f":white_check_mark: Transaction completed! {amount} has been donated to Ultima's public balance")

  global mainbal
  mainbal+=amount


@economy.command(description="Give some of your money to another member!")
async def pay(ctx,amount,member:discord.Member):
  if amount == None : 
    return await ctx.respond(":x: Please enter  a proper amount of money!")
  try :
    int(amount)
  except : 
    return await ctx.respond(":x: Amount can only be a number!")
  await open_account(ctx.author)
  await open_account(member)
  if member == ctx.author :
    await ctx.respond("It's not a good idea to pay yourself")
                
    return
  bal = await update_bank(ctx.author)
  if amount == "all":
    amount = bal[0]
  try :
    amount = int(amount)
  except :
    await ctx.respond("Please enter a valid number")
    return
  if amount>bal[0]:
    await ctx.respond("Please make sure you have enough money in your wallet!")
    return
  if amount<0:
    await ctx.respond("Please enter a number bigger than 1")
                
    return 

  await update_bank(ctx.author,-1*amount,"Wallet")
  await update_bank(member,amount,"Wallet")  

  await ctx.respond(f":white_check_mark: Transaction completed! {amount} has been transfered to {member.name}")
    

@economy.command(description="Rob another member!")
@commands.cooldown(1, 1000, commands.BucketType.user)
async def robmember(ctx,member:discord.Member):
  await open_account(ctx.author)
  await open_account(member)
  user = ctx.author

  mem = member

  users = await get_bank_data()

  earnings = random.randint(100, 500)

  wallet_aamt = users[str(user.id)]["Wallet"]

  decider = random.randint(0,1)

  wallet_amt = users[str(mem.id)]["Wallet"]

  if wallet_amt < earnings:
    if wallet_amt < 0:
      await ctx.respond("It's not worth it :pensive:")
      return
    elif wallet_amt == 0:
      await ctx.respond("It's not worth it :pensive:")
      return
    else:
      earnings = wallet_amt

  
  if decider == 1:
    await ctx.respond(f"You just robbed {member} and got {earnings} credits!")

    users[str(user.id)]["Wallet"] +=earnings
    users[str(mem.id)]["Wallet"] -=earnings

    with open("bank.json", 'w') as f:
      json.dump(users, f)
  else:
    responselist=[f"{mem} knew how to defend themselves and took 100 credits from you instead!", f"{mem} killed you and took 100 credits from you!", "A dog killed you and ate 100 credits!"]
    choice = random.choice(responselist)
    await ctx.respond(choice)
    if wallet_aamt > 100:
      users[str(user.id)]["Wallet"] -= 100

      with open("bank.json", "w") as f:
        json.dump(users, f)
    else:
      ammountt = wallet_aamt
      users[str(user.id)]["Wallet"] -=ammountt

      with open("bank.json", 'w') as f:
        json.dump(users, f)
      
    

@economy.command(description="Transfer money from your wallet to the bank")
async def deposit(ctx,amount):
  if amount == None : 
    return await ctx.respond(":x: Please enter a proper amount of money!")
  try :
    int(amount)
  except : 
    return await ctx.respond(":x: Amount can only be a number!")
  await open_account(ctx.author)
          
  bal = await update_bank(ctx.author)
  amount = int(amount)
  if amount>bal[0]:
    await ctx.respond(":x: You don't have the enough amount !")
                  
    return
  if amount<0:
    await ctx.respond(":x: Please enter a number bigger than 1.")
                  
    return 

  await update_bank(ctx.author,-1*amount)
  await update_bank(ctx.author,amount,"Bank")  

  await ctx.respond(f":moneybag: You just deposited {amount} dollars.")

@economy.command(description="Transfer money from your wallet to the bank")
async def withdraw(ctx,amount):
  if amount == None : 
    return await ctx.respond(":x: Please enter  a proper amount of money!")
  try :
    int(amount)
  except : 
    return await ctx.respond(":x: Amount can only be a number!")
  await open_account(ctx.author)
  bal = await update_bank(ctx.author)
  amount = int(amount)
  if amount>bal[1]:
    await ctx.respond(":x: You don't have the enough amount !")
                
    return
  if amount<0:
    await ctx.respond(":x: Please enter a number bigger than 1.")
                    
    return 
        
  await update_bank(ctx.author,amount)
  await update_bank(ctx.author,-1*amount,"Bank")  

  await ctx.respond(f":moneybag: You withdrew {amount} dollars.")

@economy.command(description="Buy something")
async def buy(ctx,item):
  await open_account(ctx.author)
  await open_inventory(ctx.author)

  user=ctx.author

  userinv=ctx.author

  cost=2500
  
  users=await get_bank_data()

  usersinv=await get_inventory_data()

  wallet_amt = users[str(user.id)]["Wallet"]
  bank_amt = users[str(user.id)]["Bank"]

  if wallet_amt < cost:
    if bank_amt > cost:
      await ctx.respond(f"You don't have enough money in your wallet! Try to buy something online instead with your online wallet! This item costs {cost} credits.")
      return
    else:
      await ctx.respond(f"Buying something costs {cost} currently! You have less than that!")
      return
  
  if item.lower()=="gun":
    itemcode=1
    
    await ctx.respond(f"You just bought {item}! It has been stored in your inventory.")

    users[str(user.id)]["Wallet"] -= cost

    with open("bank.json", "w") as f:
      json.dump(users, f)

    usersinv[str(userinv.id)]["Inventory"] = itemcode

    with open("inventory.json", "w") as f:
      json.dump(usersinv, f)
  elif item.lower()=="armour":
    itemcode=2

    await ctx.respond(f"You just bought {item}! It has been stored in your inventory.")

    users[str(user.id)]["Wallet"] -= cost

    with open("bank.json", "w") as f:
      json.dump(users, f)

    usersinv[str(userinv.id)]["Inventory"] = itemcode

    with open("inventory.json", "w") as f:
      json.dump(usersinv, f)

  elif item.lower()=="mouse":
    itemcode=3

    await ctx.respond(f"You just bought {item}! It has been stored in your inventory.")

    users[str(user.id)]["Wallet"] -= cost

    with open("bank.json", "w") as f:
      json.dump(users, f)

    usersinv[str(userinv.id)]["Inventory"] = itemcode

    with open("inventory.json", "w") as f:
      json.dump(usersinv, f)
  
  else:
    await ctx.respond("This is not a valid item! Use /shop to get a list of purchasable items!")


@economy.command(description="View the shop")
async def shop(ctx):
  embed=discord.Embed(
    title="Shop"
  )
  embed.add_field(name="Buy things with money!", value="Gun\nArmour\nMouse")
  await ctx.respond(embed=embed)

@economy.command(description="View the leaderboard")
async def leaderboard(ctx):
  limit = 3
  try :
            
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
      name = int(user)
      total_amount = users[user]["Wallet"] + users[user]["Bank"]
      leader_board[total_amount] = name
      total.append(total_amount)

    total = sorted(total,reverse=True)    

    em = discord.Embed(title = f"Top {limit} Richest People" , description = "This is decided on the ammount of money in the bank and wallet",color = random.randrange(0, 0xffffff))
    index = 1
    for amt in total:
      id_ = leader_board[amt]
      member = client.get_user(id_)
      name = member.name
      em.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
      if index == limit:
        break
      else:
        index += 1
        em.set_footer(text =f"Requested by {ctx.author}")
        
    await ctx.respond(embed = em)
  except AttributeError:
    await ctx.respond(":x: Insufficent accounts stored in database!")



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

client2.load_extension('PXBot.mainbot')

client3.load_extension('ChatBot.mainchatbot')

client4.load_extension('EDBot.mainED')

async def main():
   await client.start(TOKEN)
   await client2.start(TOKEN2)
   await client3.start(TOKEN3)
   await client4.start(TOKEN4)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())