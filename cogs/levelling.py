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

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open('levels.json', 'r') as f:
            users = json.load(f)

        if not f'{member.id}' in users:
            users[f'{member.id}'] = {}
            users[f'{member.id}']['experience'] = 0
            users[f'{member.id}']['level'] = 1

        with open('levels.json', 'r'):
            json.dump(users, f)

    @bridge.bridge_command(description="Enable and disable the leveling system")
    @commands.has_permissions(administrator = True)
    async def activelevel(self, ctx):
        with open("levelguilds.json") as f:
            automodguild = json.load(f)

        if ctx.guild.id not in automodguild:
            automodguild.append(ctx.guild.id)
            await ctx.respond("Enabled levels, saving settings...")
        elif ctx.guild.id in automodguild:
            automodguild.remove(ctx.guild.id)
            await ctx.respond("Disabled levels, saving settings...")

        with open("levelguilds.json", "w+") as f:
            json.dump(automodguild, f)

        await ctx.respond("Settings saved!")

    @bridge.bridge_command()
    async def level(self, ctx, member: discord.Member = None):
        def generate_level_up_image(username, level):
            background = Image.open("background.png")

            image = Image.new("RGBA", background.size, (0, 0, 0, 0))
            image.paste(background, (0, 0))

            font = ImageFont.truetype("arial.ttf", 80)
            draw = ImageDraw.Draw(image)

            # Print username in top left corner
            username_font = ImageFont.truetype("arial.ttf", 60)
            draw.text((10, 10), username, font=username_font, fill=(255, 255, 255))

            # Print level in the middle
            text_width, text_height = draw.textsize(f"Level {level}", font=font)
            x = (background.width - text_width) // 2
            y = (background.height - text_height) // 2

            draw.text((x, y), f"Level {level}", font=font, fill=(255, 255, 255))

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

                


def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(levelling(bot)) # add the cog to the bot