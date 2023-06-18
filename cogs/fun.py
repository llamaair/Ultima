import discord
from discord.ext import commands
import asyncio
import random
import json
import requests
from discord.ext import bridge

class fun(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot


    @bridge.bridge_command(description="Get a cute cat picture")
    async def cat(self, ctx):
        response = requests.get('https://api.thecatapi.com/v1/images/search')
        if response.status_code == 200:
            data = json.loads(response.text)
            await ctx.respond(data[0]['url'])
        else:
            await ctx.respond('Unable to retrieve cat picture.')
            
    @bridge.bridge_command(description="Get a cute dog picture")
    async def dog(self, ctx):
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        if response.status_code == 200:
            data = response.json()
            await ctx.respond(data['message'])
        else:
            await ctx.respond('Unable to retrieve dog picture.')
        
    @bridge.bridge_command(description="Get a random quote")
    async def quote(self, ctx):
        response = requests.get('https://api.quotable.io/random')
        if response.status_code == 200:
            data = response.json()
            quote = f'"{data["content"]}" - {data["author"]}'
            await ctx.respond(quote)
        else:
            await ctx.respond('Unable to retrieve quote.')
        
    @bridge.bridge_command(description="Get some cute pug pictures!")
    async def pug(self, ctx):
      puglist=["https://c.files.bbci.co.uk/17444/production/_124800359_gettyimages-817514614.jpg", "https://cdn.britannica.com/35/233235-050-8DED07E3/Pug-dog.jpg", "https://www.collinsdictionary.com/images/full/pug_120113251.jpg", "https://www.thesprucepets.com/thmb/LohW6iEtHMcvCfvxASVG-YP29mE=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/pug-dog-breed-profile-1117989-hero-a6ae86cdb7b64214998c9d0c408b46e5.jpg"]
      puggo = random.choice(puglist)
      await ctx.respond(puggo)


    @bridge.bridge_command(description="Get a picture of a fat cat!")
    async def fatcat(self, ctx):
        await ctx.respond(
        "https://live.staticflickr.com/3652/3513292420_6becf54bbf.jpg")


    @bridge.bridge_command(description="Get a picture of a fat dog!")
    async def fatdog(self, ctx):
        fatdoglist = [
        "https://wompampsupport.azureedge.net/fetchimage?siteId=7575&v=2&jpgQuality=100&width=700&url=https%3A%2F%2Fi.kym-cdn.com%2Fentries%2Ficons%2Fmobile%2F000%2F029%2F671%2Fwide_dog_cover2_.jpg",
        "https://s.abcnews.com/images/Entertainment/HT_vincent4_dog_ml_160413_16x9_608.jpg"
    ]
        fatdogchoise = random.choice(fatdoglist)
        await ctx.respond(fatdogchoise)

    @bridge.bridge_command(description="Print a random fact")
    async def fact(self, ctx):
        factlinks = [
        'Rubber bands last longer when refrigerated.',
        'No number from one to 999 includes the letter “a” in its word form.',
        'Edgar Allan Poe married his 13-year-old cousin.',
        'Flamingos can only eat with their heads upside down.',
        'There are 32 muscles in a cat’s ear.',
        'Junk food is as addictive as drugs.',
        'In most advertisements, including newspapers, the time displayed on a watch is 10:10.',
        'A cubic inch of human bone can bear the weight of five standard pickup trucks.',
        'Four out of five children recognize the McDonald’s logo at three years old.',
        'It’s impossible to tickle yourself.',
        'It’s impossible for you to lick your own elbow.',
        'Oreo has made enough cookies to span five back and forth trips to the moon.',
        'Due to a genetic defect, cats can’t taste sweet things.',
        'The average American spends about 2.5 days a year looking for lost items.',
        'If you plug your nose, you can’t tell the difference between an apple, a potato, and an onion.',
        'Somali pirates have such a hatred for Western culture, that the British Navy uses music from Britney Spears to scare them off.',
        'The country of Russia is bigger than Pluto.',
        'Many oranges are actually green.',
        'Playing dance music can help ward off mosquitoes.'
    ]
        factlinkchosen = random.choice(factlinks)
        await ctx.respond(factlinkchosen)
        
    @bridge.bridge_command(description="Get a random challenge!")
    async def challenge(self, ctx):
        challengelist=["Eat a hamburger in 20 seconds", "Say yeet in your most southern accent", "Don't speak today", "Stop watching TV", "Eat slower today", "Do 15 sit-ups", "Learn to draw a face", "Don't drink soda today", "Do something you are scared of", "Abuse FetchBot"]
        challenge = random.choice(challengelist)
        await ctx.respond(challenge)
    
    @bridge.bridge_command(description="Ask me a question!")
    async def ask(self, ctx, *, question):
        responselist=['Yes', 'No', 'Maybe', 'Sure!', 'Of course!', 'Why not', 'I am tired! Ask me later instead.', 'I have no idea', 'Stupid humans...', 'Maybe?', 'Why are you asking me?']
        response = random.choice(responselist)
        await ctx.respond(response)

    @bridge.bridge_command(description="Get a anime picture")
    async def anime(self, ctx):
        animelist = [
        "https://cdn.vox-cdn.com/thumbor/I7I0t87KZ-vf_GSWrH118jwl6d0=/1400x0/filters:no_upscale()/cdn.vox-cdn.com/uploads/chorus_asset/file/23437452/The_Spy_x_Family_Anime_Succeeds_Because_of_Its_Characters_.jpg",
        "https://androspel.com/wp-content/uploads/2022/03/anime-dimensions-tier-list.jpg",
        "https://www.gamespot.com/a/uploads/screen_kubrick/1732/17320263/4019145-anime-dek-image.jpg"
    ]
        animechoise = random.choice(animelist)
        await ctx.respond(animechoise)





def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(fun(bot)) # add the cog to the bot