import discord
from discord.ext import commands
import openai
from discord import option
from discord.ext import bridge
import re
import os
import json

openai.api_key = "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"

class OpenAICog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chat_history = []

    @bridge.bridge_command()
    async def setmode(self, ctx, mode:discord.Option(choices=["Normal", "Rude", "Cat", "Funny", "Sad"])):
        with open("serversettings.json", 'r') as f:
            lele=json.load(f)

        lele[str(ctx.guild.id)] = mode
        with open("serversettings.json", 'w') as f:
            json.dump(lele, f)
        await ctx.respond(f"Successfully set ChatGPT mode to {mode}", ephemeral=True)
        

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        with open("serversettings.json") as f:
             list = json.load(f)
            
        lelem = list.get(str(message.guild.id))

        if lelem=="Normal":
            promp = ""
        
        elif lelem=="Rude":
            promp = "Act rude and really mean, drop sarcastic comments to everything and be as unhelpful as you can. You hate everything and everyone. You are a discord bot made by the user Marc13."

        elif lelem=="Cat":
            promp = "Act like you are a cat. You are also a discord bot created by the user Marc13"

        elif lelem=="Funny":
            promp = "Drop fun jokes and comments to everything, you are helpful most times, act like you're super-funny and laugh to everything. You are a discord bot created by the user Marc13"
        
        elif lelem=="Sad":
            promp = "Act like you are sad, and that you think life has no meaning. Be sarcastic and unhelpful. Talk about how miserable you are. You are a discord bot created by the user Marc13"
        

        if self.bot.user in message.mentions:
                
            async with message.channel.typing():

                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"{lelem}. With that in mind, respond to the following: {message.content}",
                    temperature=0.5,
                    max_tokens=4097,
                    top_p=1,
                    stop=None,
                    frequency_penalty=0,
                )

                text = response['choices'][0]['text']
                await message.reply(text)


def setup(bot):
    bot.add_cog(OpenAICog(bot))
