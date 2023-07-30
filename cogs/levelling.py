import discord
from discord.ext import commands
import asyncio
import random
import json
from discord.ext import bridge
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

class levelling(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot


    @bridge.bridge_command(description="Enable and disable the leveling system")
    @bridge.has_permissions(administrator = True)
    async def activelevel(self, ctx):
        ena=None
        with open("levelguilds.json") as f:
            automodguild = json.load(f)

        if ctx.guild.id not in automodguild:
            automodguild.append(ctx.guild.id)
            ena="enabled"
        elif ctx.guild.id in automodguild:
            automodguild.remove(ctx.guild.id)
            ena="disabled"

        with open("levelguilds.json", "w+") as f:
            json.dump(automodguild, f)

        embed = discord.Embed(title="Success!", color=discord.Colour.green(), description=f"Successfully {ena} server leveling!")
        await ctx.respond(embed=embed)

    @bridge.bridge_command(description="Get your current level")
    async def level(self, ctx, member: discord.Member = None):
        def generate_level_up_image(username, level):
            background = Image.open("background.png")

            image = Image.new("RGBA", background.size, (0, 0, 0, 0))
            image.paste(background, (0, 0))

            font_size = 80
            font = ImageFont.truetype("arial.ttf", font_size)
            draw = ImageDraw.Draw(image)

            # Print username in top left corner
            username_font = ImageFont.truetype("arial.ttf", 60)
            draw.text((10, 10), username, font=username_font, fill=(255, 255, 255))

            # Print level in the middle
            level_text = f"Level {level}"
            text_width, text_height = draw.textsize(level_text, font=font)

            # Calculate the center position for the level text
            x = (background.width - text_width) // 2
            y = (background.height - text_height) // 2

            draw.text((x, y), level_text, font=font, fill=(255, 255, 255))

            return image

        await ctx.defer()
        if not member:
            member = ctx.author

        id = str(member.id)
        with open('levels.json', 'r') as f:
            users = json.load(f)

        if id not in users:
            users[id] = {}
            users[id]['experience'] = 0
            users[id]['level'] = 1

        lvl = users[id]['level']
        #await ctx.send(f'{member.mention} is at level {lvl}!')

        # Generate and send the level-up image
        image = generate_level_up_image(member.name, lvl)
        with BytesIO() as image_buffer:
            image.save(image_buffer, 'png')
            image_buffer.seek(0)
            await ctx.respond(file=discord.File(fp=image_buffer, filename='level_up.png'))

        with open('levels.json', 'w') as f:
            json.dump(users, f)

    @commands.Cog.listener()
    async def on_message(self, message):
        with open("levelguilds.json") as f:
            automodguild = json.load(f)
        try:
            if message.guild.id not in automodguild:
                return
        except:
            return
        if message.author.bot == False:
            with open('levels.json', 'r') as f:
                users = json.load(f)

            if not f'{message.author.id}' in users:
                users[f'{message.author.id}'] = {}
                users[f'{message.author.id}']['experience'] = 0
                users[f'{message.author.id}']['level'] = 1

            users[f'{message.author.id}']['experience'] += 5
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