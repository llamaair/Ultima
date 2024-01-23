import discord
from discord.ext import commands, bridge
import json

class tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tags = self.load_tags()

    @staticmethod
    def load_tags():
        try:
            with open('tags.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_tags(self):
        with open('tags.json', 'w') as file:
            json.dump(self.tags, file)

    @bridge.bridge_command(description="Create a new tag")
    @bridge.has_permissions(administrator=True)
    async def tags_create(self, ctx, tag_name: str, *, tag_response: str):
        self.tags.setdefault(str(ctx.guild.id), {})[tag_name] = tag_response
        self.save_tags()
        await ctx.respond(f'Tag "{tag_name}" has been created.')

    @bridge.bridge_command(description="View a tag")
    async def tag(self, ctx, tag_name: str):
        guild_tags = self.tags.get(str(ctx.guild.id), {})
        if tag_name in guild_tags:
            await ctx.respond(f'{guild_tags[tag_name]}')
        else:
            await ctx.respond(f'Tag "{tag_name}" does not exist.', ephemeral=True)

    @bridge.bridge_command(description="Delete a tag")
    @bridge.has_permissions(administrator=True)
    async def tags_delete(self, ctx, tag_name: str):
        guild_tags = self.tags.get(str(ctx.guild.id), {})
        if tag_name in guild_tags:
            del guild_tags[tag_name]
            self.save_tags()
            await ctx.respond(f'Tag "{tag_name}" has been deleted.')
        else:
            await ctx.respond(f'Tag "{tag_name}" does not exist.', ephemeral=True)

    @bridge.bridge_command(description="List all tags")
    async def tags_list(self, ctx):
        guild_tags = self.tags.get(str(ctx.guild.id), {})
        if guild_tags:
            tags_list = '\n'.join(guild_tags.keys())
            await ctx.respond(f'**Tags:**\n\n{tags_list}')
        else:
            await ctx.respond('There are no tags in this server.', ephemeral=True)

    @bridge.bridge_command(description="Modify a tag's content")
    @bridge.has_permissions(administrator=True)
    async def tags_modify(self, ctx, tag_name: str, *, new_response: str):
        guild_tags = self.tags.get(str(ctx.guild.id), {})
        if tag_name in guild_tags:
            guild_tags[tag_name] = new_response
            self.save_tags()
            await ctx.respond(f'Tag "{tag_name}" has been modified.')
        else:
            await ctx.respond(f'Tag "{tag_name}" does not exist.', ephemeral=True)

def setup(bot):
    bot.add_cog(tags(bot))
