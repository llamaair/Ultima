import discord
from discord.ext import commands, bridge
import requests
import json

class EDDNCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command()
    async def sysinfo(self, ctx, system):

        # Prepare EDSM URL and headers
        url = f"https://www.edsm.net/api-system-v1/bodies?systemName={system}&showId=1"

        # Send request to EDSM to get system data for the specified system
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            system_data = response.json()
            # Print the system data to the console
            print(system_data)
            # Send the system data as a message to the Discord channel
            await ctx.send(f"System data for {system}: {system_data}")
        else:
            # Send an error message to the Discord channel if the request failed
            await ctx.send("Failed to retrieve system data from EDSM.")

def setup(bot):
    bot.add_cog(EDDNCog(bot))
