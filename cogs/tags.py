import discord
from discord.ext import commands, bridge
import json

class tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tags = self.load_tags()

    def load_tags(self):
        try:
            with open('tags.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_tags(self):
        with open('tags.json', 'w') as file:
            json.dump(self.tags, file)

    @bridge.bridge_command()
    @commands.has_permissions(administrator=True)
    async def create_tag(self, ctx, tag_name: str, *, tag_response: str):
        self.tags.setdefault(str(ctx.guild.id), {})[tag_name] = tag_response
        self.save_tags()
        await ctx.respond(f'Tag "{tag_name}" has been created.')

    @bridge.bridge_command()
    async def tag(self, ctx, tag_name: str):
        guild_tags = self.tags.get(str(ctx.guild.id), {})
        if tag_name in guild_tags:
            await ctx.respond(f'{guild_tags[tag_name]}')
        else:
            await ctx.respond(f'Tag "{tag_name}" does not exist.')

def setup(bot):
    bot.add_cog(tags(bot))
