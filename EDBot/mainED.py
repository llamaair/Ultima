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
        response = requests.get(f"https://www.edsm.net/api-v1/system?systemName={system}")
        if response.status_code == 200:
            data = response.json()
            if "name" in data:
                system_name = data["name"]
                if "stations" in data and len(data["stations"]) > 0:
                    nearest_station = min(data["stations"], key=lambda station: station.get("distance_to_star", math.inf))
                    station_name = nearest_station.get("name")
                    station_distance = nearest_station.get("distance_to_star")
                    if station_name and station_distance is not None:
                        await ctx.respond(f"The nearest station in {system_name} is {station_name} ({station_distance:.2f} ls away).")
                    else:
                        await ctx.respond(f"No station name found for the nearest station in {system_name}.")
                else:
                    nearest_system = min(data["coords"], key=lambda coord: coord.get("distance", math.inf))
                    nearest_system_name = nearest_system.get("name")
                    nearest_system_distance = nearest_system.get("distance")
                    if nearest_system_name and nearest_system_distance is not None:
                        await ctx.respond(f"No stations found in {system_name}. The nearest system with a station is {nearest_system_name} ({nearest_system_distance:.2f} ly away).")
                    else:
                        await ctx.respond(f"No stations found in {system_name} or any nearby systems.")
            else:
                await ctx.respond(f"System information not found for {system}.")
        else:
            await ctx.respond(f"Error getting system information for {system}.")

def setup(bot):
    bot.add_cog(EDDNCog(bot))
