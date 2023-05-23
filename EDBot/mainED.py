import discord
from discord.ext import commands, bridge
import requests
import math

class EDDNCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command()
    async def nearest_station(self, ctx, system: str):
        """Finds the nearest station in a given system using EDSM API."""
        response = requests.get(f"https://www.edsm.net/api-system-v1/stations?systemName={system}")
        if response.status_code == 200:
            data = response.json()
            stations = data.get("stations", [])
            if len(stations) > 0:
                nearest_station = min(stations, key=lambda station: station.get("distance_to_star", float('inf')))
                station_name = nearest_station.get("name")
                if station_name:
                    await ctx.respond(f"The nearest station in {system} is {station_name}.")
                else:
                    await ctx.respond(f"No station name found for the nearest station in {system}.")
            else:
                # No stations in this system, try to find the nearest system with a station
                response = requests.get(f"https://www.edsm.net/api-system-v1/sphere-systems?x=0&y=0&z=0&radius=50&showInformation=1")
                if response.status_code == 200:
                    systems = response.json().get("systems", [])
                    nearest_system = min(systems, key=lambda system: system.get("distance", math.inf))
                    nearest_system_name = nearest_system.get("name")
                    nearest_system_distance = nearest_system.get("distance")
                    if nearest_system_name and nearest_system_distance is not None:
                        await ctx.respond(f"No stations found in {system}. The nearest system with a station is {nearest_system_name} ({nearest_system_distance:.2f} ly away).")
                    else:
                        await ctx.respond(f"No stations found in {system} or any nearby systems.")
                else:
                    await ctx.respond(f"Error getting nearby systems.")
        else:
            await ctx.respond(f"Error getting stations for {system}.")

def setup(bot):
    bot.add_cog(EDDNCog(bot))
