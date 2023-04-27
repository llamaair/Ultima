import discord
from discord.ext import commands
import asyncio
import time
from discord.ext import bridge
from datetime import timedelta

global badword
badword = ["ass", "fucker", "fuck", "cunt", "bitch", "anal", "nigga", "nigger", "pussy", "dick", "slut", "whore", "cock", "arse"]

class Vieww(discord.ui.View):
    @discord.ui.button(label="Yes", style=discord.ButtonStyle.primary)
    async def but_one_callback(self, button, interaction):
        global badword
        lis = []
        count = 0
        for member in interaction.guild.members:
            for word in badword:
                if word.lower() in str(member.nick).lower():
                    await member.edit(nick="Moderated nickname")
                    count+=1
                    lis.append(member.name)
                    
        await interaction.response.send_message("Successfully changed all members with bad nicks nicknames :white_check_mark:")

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command()
    async def testo(self, ctx):
        loop = asyncio.get_event_loop()
        loop.create_task(self.nickscan(ctx))

    @bridge.bridge_command(description="Kick people")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user:discord.User, reason="No reason provided"):
        if user.guild_permissions.administrator:
            return await ctx.respond("You can't kick another admin!")
        try:
            await ctx.guild.kick(user, reason=reason)
            embed = discord.Embed(title="Kicked", description=f"You have been kicked from {ctx.guild}!", color=discord.Colour.red())
            await ctx.respond(f"Successfully kicked user {user.mention} for {reason}")
            try:
                await user.send(embed=embed)
            except:
                pass
        except Exception as e:
            await ctx.respond(f"Unable to kick this member")
    
    @bridge.bridge_command(description="Ban people")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user:discord.User, reason="No reason provided"):
        if user.guild_permissions.administrator:
            return await ctx.respond("You can't ban another admin!")
        try:
            await ctx.guild.ban(user, reason=reason)
            embed = discord.Embed(title="Banned", description=f"You have been banned from {ctx.guild}!", color=discord.Colour.red())
            await ctx.respond(f"Successfully banned user {user.mention} for {reason}")
            try:
                await user.send(embed=embed)
            except:
                pass
        except Exception as e:
            await ctx.respond(f"Unable to ban this member")
    
    @bridge.bridge_command(description="Delete messages")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount:int, member:discord.Member=None):
        if member!=None:
            msg = []
            async for m in ctx.channel.history():
                if len(msg) == amount:
                    break
                if m.author.id == member.id:
                    msg.append(m)
                await ctx.channel.delete_messages(msg)
                await ctx.respond(f"Messages from {member} has been purged")
                return
        await ctx.respond("Purging messages...", ephemeral=True)
        await ctx.channel.purge(limit=amount)
    
    @bridge.bridge_command(description="Time out another member")
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member:discord.Member, minutes:int):
        duration = timedelta(minutes=minutes)
        await member.timeout_for(duration)
        await ctx.respond(f"Successfully timeout out {member} for {minutes} minutes", ephemeral=True)
        embed = discord.Embed(title="Timed out", description=f"You have been timed out for {minutes} minutes in {ctx.guild}", color=discord.Colour.red())
        try:
            await member.send(embed=embed)
        except:
            pass
    
    @bridge.bridge_command(description="Unmute a member")
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member:discord.Member):
        try:
            await member.remove_timeout()
            await ctx.respond(f"Successfully removed timeout from {member}", ephemeral=True)
            embed = discord.Embed(title="Timeout removed", description=f"You have been unmuted in {ctx.guild}", color=discord.Colour.green())
        except:
            await ctx.respond("Failed to remove timeout from {member}. Possible reasons for this could be that the member isn't timed out.", ephemeral=True)

    @bridge.bridge_command(description="Warn a member")
    @commands.has_permissions(moderate_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason):
        await ctx.respond("Warning sent",ephemeral=True)
        await member.send(f"{member.mention}, you have been warned by {ctx.author.mention} for {reason} in {ctx.guild.name}")
        
    @bridge.bridge_command()
    async def testo(self, ctx):
        loop = asyncio.get_event_loop()
        loop.create_task(self.nickscan(ctx))
        
    @bridge.bridge_command(description="Scan through all members nicks")
    @commands.has_permissions(moderate_members=True)
    async def nickscan(self, ctx):
        msg = await ctx.respond("Scanning nicks...")
        count = 0
        global badword
        lis = []
        for member in ctx.guild.members:
            for word in badword:
                if word.lower() in str(member.nick).lower():
                    count+=1
                    lis.append(member.name)
        view = Vieww()
        await ctx.respond(f"Found {count} member/s with bad nicks. Do you wish to moderate these nicks?", view=view)
        await view.wait()

def setup(bot):
    bot.add_cog(moderation(bot))