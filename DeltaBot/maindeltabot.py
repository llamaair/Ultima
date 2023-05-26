import discord
import os
import requests
from datetime import datetime
from discord.ext import commands, bridge

class DeltaApp(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="Fleet Application", custom_id="deltfleet", style=discord.ButtonStyle.primary, emoji="🚀")
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(deltafleetapp(title="Fleet Application"))

class deltafleetapp(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="CMDR Name"))
        self.add_item(discord.ui.InputText(label="Carrier name and ID"))
        self.add_item(discord.ui.InputText(label="Why do you want to join our fleet?", style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="Role you're applying for"))
        

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="New Delta Fleet application!")
        embed.add_field(name="CMDR Name", value=self.children[0].value)
        embed.add_field(name="Carrier name?", value=self.children[1].value)
        embed.add_field(name="Why?", value=self.children[2].value)
        embed.add_field(name="Role", value=self.children[3].value)
        embed.add_field(name="Submitted by", value=interaction.user)
        member = self.bot.get_user(719527356368289802)
        member2 = self.bot.get_user(686846149608734730)
        await member.send(embeds=[embed])
        await member2.send(embeds=[embed])
        await interaction.response.send_message("Successfully submitted application :white_check_mark: Expect response within 24 hours or less!", ephemeral=True)

class DeltaBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(description="Ping!")
    async def ping(self, ctx):
        await ctx.respond("Pong!")

    @bridge.bridge_command(description="Launch the fleet application system")
    async def fleetapp(self, ctx):
        embed=discord.Embed(title="Fleet Application", description="Please press the button below if you wish to apply for the official Delta Interspace fleet", color=discord.Colour.green())
        await ctx.send(embed=embed, view=DeltaApp())



def setup(bot):
    bot.add_cog(DeltaBot(bot))
