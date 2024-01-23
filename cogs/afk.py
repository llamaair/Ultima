import discord
from discord.ext import bridge, commands
import json
from main import guild

class afk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_group()
    async def afk(self, ctx):
        pass

    @afk.command(description="Set your AFK message")
    async def set(self, ctx, status:str):
        with open("afkstatus.json", "r") as f:
            afkstat = json.load(f)
        
        afkstat[str(ctx.author.id)] = str(status)

        with open("afkstatus.json", "w") as f:
            json.dump(afkstat, f)
        
        embed = discord.Embed(title="Success!", color=discord.Colour.green(), description=f"Successfully set AFK status to {status}!")
        await ctx.respond(embed=embed, ephemeral=True)

    @afk.command(description="Set your AFK status")
    async def status(self, ctx):
        with open("afk.json", "r") as f:
            afkk = json.load(f)

        status = None

        if str(ctx.author.id) not in afkk:
            afkk.append(str(ctx.author.id))
            status = "Appended"
        
        else:
            afkk.remove(str(ctx.author.id))
            status = "Removed"
        
        with open("afk.json", "w") as f:
            json.dump(afkk, f)
        
        if status == "Removed":
            embed = discord.Embed(title="Success!", color=discord.Colour.green(), description=f"Successfully removed AFK status!")
            await ctx.respond(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="Success!", color=discord.Colour.green(), description=f"Successfully set status to afk!")
            await ctx.respond(embed=embed, ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        with open("afk.json", "r") as f:
            rolla = json.load(f)

        with open("afkstatus.json", "r") as w:
            rollv = json.load(w)

        for item in rolla:
            if f"<@{item}>" in message.content:
                stat = rollv.get(str(item))
                await message.reply(f"User is AFK: {stat}")



def setup(bot):
    bot.add_cog(afk(bot))