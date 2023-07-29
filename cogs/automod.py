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

    @automod.command(description="Create an automoderation rule")
    async def create(self, ctx, trigger:discord.Option(choises=["Spam", "Mass mentioning", "Keyword Preset"])):
        metadata = discord.AutoModActionMetadata("Message blocked")
        if trigger =="Spam":
            await ctx.guild.create_auto_moderation_rule(name="Anti-spam", reason="Automod by Ultima", enabled=True, event_type=discord.AutoModEventType.message_send, trigger_type=discord.AutoModTriggerType.spam, trigger_metadata=discord.AutoModTriggerMetadata(), actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)])
        elif trigger=="Mass mentioning":
            await ctx.guild.create_auto_moderation_rule(name="Anti-mention", reason="Automod by Ultima", enabled=True, event_type=discord.AutoModEventType.message_send, trigger_type=discord.AutoModTriggerType.mention_spam, trigger_metadata=discord.AutoModTriggerMetadata(mention_total_limit=5), actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)])
        else:
            await ctx.guild.create_auto_moderation_rule(name="Words", reason="Automod by Ultima", enabled=True, event_type=discord.AutoModEventType.message_send, trigger_type=discord.AutoModTriggerType.keyword_preset, trigger_metadata=discord.AutoModTriggerMetadata(presets=[discord.AutoModKeywordPresetType.profanity, discord.AutoModKeywordPresetType.sexual_content, discord.AutoModKeywordPresetType.slurs]), actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)])
        embed = discord.Embed(title="Success!", color=discord.Colour.green(), description=f"Successfully created automod rule for preventing {trigger}!")
        await ctx.respond(embed=embed)
    

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
                embed = discord.Embed(title="Success!", color=discord.Colour.green(), description=f"Successfully enabled automod!")
                await ctx.respond(embed=embed)
            except:
                embed = discord.Embed(title="Failure!", color=discord.Colour.red(), description=f"Failed to enable automod")
                await ctx.respond(embed=embed)

    @automod.command(description="Disable all automoderation rules")
    async def disable(self, ctx):
        await ctx.defer()
        try:
            rulelist = await ctx.guild.fetch_auto_moderation_rules()
            for rule in rulelist:
                await rule.edit(enabled=False)
            embed = discord.Embed(title="Success!", color=discord.Colour.green(), description=f"Successfully disabled all automod rules!")
            await ctx.respond(embed=embed)
        except:
            embed = discord.Embed(title="Failure!", color=discord.Colour.red(), description=f"Failed to disable all automod rules")
            await ctx.respond(embed=embed)

    @automod.command(description="Delete an automoderation rule")
    async def delete(self, ctx, name:str=None, ruleid=None):
        await ctx.defer()
        if not name and not ruleid:
            return await ctx.respond("Either a name or id must be passed!", ephemeral=True)
        if name:
            rules = await ctx.guild.fetch_auto_moderation_rules()
            matching_rules = [rule for rule in rules if rule.name == name]
            if not matching_rules:
                return await ctx.respond(f"No auto moderation rule found with name '{name}'.", ephemeral=True)
            ruleid = matching_rules[0]
        else:
            ruleid = await ctx.guild.fetch_auto_moderation_rule(ruleid)
        await ruleid.delete()
        embed = discord.Embed(title="Success!", color=discord.Colour.green(), description=f"Successfully deleted automod rule")
        await ctx.respond(embed=embed)




def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(automod(bot)) # add the cog to the bot