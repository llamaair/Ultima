import discord
from discord.ext import commands, bridge
import requests

class EDDNCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command()
    async def nearest_station(self, ctx, system: str):
        """Finds the nearest station in a given system using EDSM API."""
        response = requests.get(f"https://www.edsm.net/api-system-v1/stations?systemName={system}")
        if response.status_code == 200:
            data = response.json()
            stations = data.get("stations", [])  # Use get() method to handle missing key
            if len(stations) > 0:
                station_distances = [(station["name"], station.get("distance_to_star")) for station in stations]
                nearest_station = min(station_distances, key=lambda x: x[1])
                if nearest_station[1] is not None:
                    await ctx.respond(f"The nearest station in {system} is {nearest_station[0]} ({nearest_station[1]:.2f} ls away).")
                else:
                    await ctx.respond(f"The distance to the star for the nearest station in {system} is not available.")
            else:
                # No stations in this system, try to find the nearest system with a station
                response = requests.get(f"https://www.edsm.net/api-system-v1/sphere-systems?x=0&y=0&z=0&radius=50&showInformation=1")
                if response.status_code == 200:
                    systems = response.json().get("systems", [])  # Use get() method to handle missing key
                    systems_with_stations = [(system["name"], system.get("distance")) for system in systems if system.get("information", {}).get("stations", 0) > 0]
                    if len(systems_with_stations) > 0:
                        nearest_system_with_station = min(systems_with_stations, key=lambda x: x[1])
                        if nearest_system_with_station[1] is not None:
                            await ctx.respond(f"No stations found in {system}. The nearest system with a station is {nearest_system_with_station[0]} ({nearest_system_with_station[1]:.2f} ly away).")
                        else:
                            await ctx.respond(f"The distance to the nearest system with a station from {system} is not available.")
                    else:
                        await ctx.respond(f"No stations found in {system} or any nearby systems.")
                else:
                    await ctx.respond(f"Error getting nearby systems.")
        else:
            await ctx.respond(f"Error getting stations for {system}.")

def setup(bot):
    bot.add_cog(EDDNCog(bot))
