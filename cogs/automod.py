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

    @bridge.bridge_group()
    async def automod():
        pass

    @automod.command(description="Set up the automod system")
    async def enable(self, ctx):
        await ctx.defer()
        try:
            metadata = discord.AutoModActionMetadata("This message was blocked.")
            await ctx.guild.create_auto_moderation_rule(name="Anti-mention", reason="Automod by Ultima", enabled=True, event_type=discord.AutoModEventType.message_send, trigger_type=discord.AutoModTriggerType.mention_spam, trigger_metadata=discord.AutoModTriggerMetadata(mention_total_limit=5), actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)])
            await ctx.guild.create_auto_moderation_rule(name="Anti-spam", reason="Automod by Ultima", enabled=True, event_type=discord.AutoModEventType.message_send, trigger_type=discord.AutoModTriggerType.spam, trigger_metadata=discord.AutoModTriggerMetadata(), actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)])
            await ctx.guild.create_auto_moderation_rule(name="Words", reason="Automod by Ultima", enabled=True, event_type=discord.AutoModEventType.message_send, trigger_type=discord.AutoModTriggerType.keyword_preset, trigger_metadata=discord.AutoModTriggerMetadata(presets=[discord.AutoModKeywordPresetType.profanity, discord.AutoModKeywordPresetType.sexual_content, discord.AutoModKeywordPresetType.slurs]), actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)])
            await ctx.guild.create_auto_moderation_rule(name="Block certain words", reason="Automod by Ultima", enabled=True, event_type=discord.AutoModEventType.message_send, trigger_type=discord.AutoModTriggerType.keyword, trigger_metadata=discord.AutoModTriggerMetadata(keyword_filter=["cunt", "asshole", "bitch", "beitch", "motherfucker", "brotherfucker", "kys"]), actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)])
            await ctx.respond("AutoMod Enabled! :white_check_mark:")
        except:
            try:
                rulelist = await ctx.guild.fetch_auto_moderation_rules()
                for rule in rulelist:
                    await rule.delete()
                metadata = discord.AutoModActionMetadata("This message was blocked.")
                await ctx.guild.create_auto_moderation_rule(name="Anti-mention", reason="Automod by Ultima", enabled=True, event_type=discord.AutoModEventType.message_send, trigger_type=discord.AutoModTriggerType.mention_spam, trigger_metadata=discord.AutoModTriggerMetadata(mention_total_limit=5), actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)])
                await ctx.guild.create_auto_moderation_rule(name="Anti-spam", reason="Automod by Ultima", enabled=True, event_type=discord.AutoModEventType.message_send, trigger_type=discord.AutoModTriggerType.spam, trigger_metadata=discord.AutoModTriggerMetadata(), actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)])
                await ctx.guild.create_auto_moderation_rule(name="Words", reason="Automod by Ultima", enabled=True, event_type=discord.AutoModEventType.message_send, trigger_type=discord.AutoModTriggerType.keyword_preset, trigger_metadata=discord.AutoModTriggerMetadata(presets=[discord.AutoModKeywordPresetType.profanity, discord.AutoModKeywordPresetType.sexual_content, discord.AutoModKeywordPresetType.slurs]), actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)])
                await ctx.guild.create_auto_moderation_rule(name="Block certain words", reason="Automod by Ultima", enabled=True, event_type=discord.AutoModEventType.message_send, trigger_type=discord.AutoModTriggerType.keyword, trigger_metadata=discord.AutoModTriggerMetadata(keyword_filter=["cunt", "asshole", "bitch", "beitch", "motherfucker", "brotherfucker", "kys"]), actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)])
                await ctx.respond("AutoMod Enabled! :white_check_mark:")
            except:
                await ctx.respond("Failed to enable automod due to unknown reason.")

    @automod.command(description="Disable all automoderation rules")
    async def disable(self, ctx):
        await ctx.defer()
        try:
            rulelist = await ctx.guild.fetch_auto_moderation_rules()
            for rule in rulelist:
                await rule.edit(enabled=False)
            await ctx.respond("Successfully disabled all automod rules")
        except:
            await ctx.respond("Failed to disable automod rules")

    @automod.command(description="Delete an automoderation rule")
    async def delete(self, ctx, name:str=None, ruleid=None):
        await ctx.defer()
        if not name and not ruleid:
            return await ctx.respond("Either a name or id must be passed!", ephemeral=True)
        if name:
            rules_response = await ctx.guild.fetch_auto_moderation_rules()
            rules = rules_response
            matching_rules = [rule for rule in rules if rule['name'] == name]
            if not matching_rules:
                return await ctx.respond(f"No auto moderation rule found with name '{name}'.", ephemeral=True)
            ruleid = matching_rules[0]['id']
        await ruleid.delete()
        await ctx.respond("Successfully deleted rule!")




def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(automod(bot)) # add the cog to the bot