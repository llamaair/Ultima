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


    @bridge.bridge_command(description="Fetch a cat image")
    async def cat(self, ctx):
        response = requests.get('https://api.thecatapi.com/v1/images/search')
        if response.status_code == 200:
            data = json.loads(response.text)
            await ctx.respond(data[0]['url'])
        else:
            await ctx.respond('Unable to retrieve cat picture.', ephemeral=True)
            
    @bridge.bridge_command(description="Fetch a dog image")
    async def dog(self, ctx):
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        if response.status_code == 200:
            data = response.json()
            await ctx.respond(data['message'])
        else:
            await ctx.respond('Unable to retrieve dog picture.', ephemeral=True)
        
    @bridge.bridge_command(description="Get a random quote")
    async def quote(self, ctx):
        response = requests.get('https://api.quotable.io/random')
        if response.status_code == 200:
            data = response.json()
            quote = f'"{data["content"]}" - {data["author"]}'
            await ctx.respond(quote)
        else:
            await ctx.respond('Unable to retrieve quote.', ephemeral=True)
        
    @bridge.bridge_command(description="Get some cute pug pictures!")
    async def pug(self, ctx):
      puglist=["https://c.files.bbci.co.uk/17444/production/_124800359_gettyimages-817514614.jpg", "https://cdn.britannica.com/35/233235-050-8DED07E3/Pug-dog.jpg", "https://www.collinsdictionary.com/images/full/pug_120113251.jpg", "https://www.thesprucepets.com/thmb/LohW6iEtHMcvCfvxASVG-YP29mE=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/pug-dog-breed-profile-1117989-hero-a6ae86cdb7b64214998c9d0c408b46e5.jpg"]
      puggo = random.choice(puglist)
      await ctx.respond(puggo)

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
        'Playing dance music can help ward off mosquitoes.',
        'Movie trailers got their name because they were originally shown after the movie.',
        'Salt used to be a currency.',
        'Women blink nearly twice as much as men.',
        'On average, 100 people choke to death on ballpoint pens every year.',
        'Only one person in two billion will live to be 116 or older.',
        'A snail can sleep for three years.',
        'Americans, on average, eat 18 acres of pizza every day.',
        'The "pound" key on your keyboard (#) is called an octotroph.'
    ]
        factlinkchosen = random.choice(factlinks)
        await ctx.respond(factlinkchosen)
        
    @bridge.bridge_command(description="Get a random challenge!")
    async def challenge(self, ctx):
        challengelist=["Eat a hamburger in 20 seconds", "Say yeet in your most southern accent", "Don't speak today", "Don't watch TV, YouTube and TikTok for a whole day.", "Eat slower today", "Do 15 sit-ups", "Learn to draw a face", "Don't drink soda today", "Do something you are scared of", "Abuse FetchBot"]
        challenge = random.choice(challengelist)
        await ctx.respond(challenge)
    
    @bridge.bridge_command(description="Ask me a question!")
    async def ask(self, ctx, *, question):
        responselist=['Yes', 'No', 'Maybe', 'Sure!', 'Of course!', 'Why not', 'I am tired! Ask me later instead.', 'I have no idea', 'Stupid humans...', 'Maybe?', 'Why are you asking me?', 'whaaat??']
        response = random.choice(responselist)
        await ctx.respond(response)


def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(fun(bot)) # add the cog to the bot