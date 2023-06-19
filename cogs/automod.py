import discord
from discord.ext import commands
import asyncio
import random
import json
import datetime
import time
from datetime import timedelta
from discord.ext import bridge

class automod(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot
        self.anti_spam = commands.CooldownMapping.from_cooldown(5, 15, commands.BucketType.member)

        
        
    @bridge.bridge_command(description="Automod rule creation")
    async def automod(self, ctx):
        try:
            metadata = discord.AutoModActionMetadata("This message was blocked.")
            await ctx.guild.create_auto_moderation_rule(name="Anti-mention", reason="Automod", enabled=True, event_type=discord.AutoModEventType.message_send, trigger_type=discord.AutoModTriggerType.mention_spam, trigger_metadata=discord.AutoModTriggerMetadata(mention_total_limit=5), actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)])
            await ctx.guild.create_auto_moderation_rule(name="Anti-spam", reason="Automod", enabled=True, event_type=discord.AutoModEventType.message_send, trigger_type=discord.AutoModTriggerType.spam, trigger_metadata=discord.AutoModTriggerMetadata(), actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)])
            await ctx.guild.create_auto_moderation_rule(name="Words", reason="Automod", enabled=True, event_type=discord.AutoModEventType.message_send, trigger_type=discord.AutoModTriggerType.keyword_preset, trigger_metadata=discord.AutoModTriggerMetadata(presets=discord.AutoModKeywordPresetType["profanity", "sexual_content", "slurs"]), actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)])
            await ctx.respond("AutoMod Enabled! :white_check_mark:")
        except Exception as e:
            await ctx.respond("Failed to enable automod. One reason to this could be that automod is already enabled :x:")
            print(e)

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(automod(bot)) # add the cog to the bot