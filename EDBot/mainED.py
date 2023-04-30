import discord
from discord.ext import commands, bridge
import requests

class EDDNCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command()
    async def solsystem(self, ctx):
        system_name = "Sol"

        # Prepare EDDN URL and headers
        url = f"https://eddn.edcd.io/supported-journals?v=1"
        headers = {"Content-Type": "application/json"}

        # Send request to EDDN to get supported journals
        response = requests.get(url, headers=headers)
        supported_journals = response.json()

        # Get the name of the most recent journal from the list of supported journals
        most_recent_journal_name = supported_journals[-1]["name"]

        # Prepare URL and headers for querying EDDN for system data
        url = f"https://eddn.edcd.io/supported-journal/{most_recent_journal_name}"
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Send request to EDDN to get system data for the specified system
        response = requests.get(url, headers=headers, params={"systemName": system_name})

        # Check if the request was successful
        if response.status_code == 200:
            system_data = response.json()
            # Print the system data to the console
            print(system_data)
            # Send the system data as a message to the Discord channel
            await ctx.send(f"System data for {system_name}: {system_data}")
        else:
            # Send an error message to the Discord channel if the request failed
            await ctx.send("Failed to retrieve system data from EDDN.")

def setup(bot):
    bot.add_cog(EDDNCog(bot))
