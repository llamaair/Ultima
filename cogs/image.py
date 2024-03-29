import discord
from discord.ext import commands, bridge
import requests
import json
from main import guild
from main import oapi_key

class image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @bridge.bridge_command(description="Generate an image from a prompt")
    async def image(self, ctx, prompt:str):
        await ctx.defer()
        API_KEY = oapi_key
        response = requests.post(
    "https://api.openai.com/v1/images/generations",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "model": "image-alpha-001",
        "prompt": prompt,
        "num_images": 1,
        "size": "512x512",
        "response_format": "url"
    }
)

        image_url = response.json()["data"][0]["url"]

        image_data = requests.get(image_url).content

        with open("generated_image.png", "wb") as f:
            f.write(image_data)

        await ctx.respond(file=discord.File("generated_image.png"))

def setup(bot):
    bot.add_cog(image(bot))