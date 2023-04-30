import discord
import os
import requests
from datetime import datetime
from pytz import timezone
from dateutil import parser
from discord.ext import commands, bridge

class PXBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    API_KEY = "bce9536354b644c49c3e7a9e73e02883"
    ARSENAL_TEAM_ID = 57
    URL = f"https://api.football-data.org/v2/teams/{ARSENAL_TEAM_ID}/matches?status=SCHEDULED"

    @bridge.bridge_command(description="See when the next Arsenal match is")
    async def nextmatch(self, ctx):
        headers = {"X-Auth-Token": self.API_KEY}
        response = requests.get(self.URL, headers=headers).json()

        if "message" in response:
            await ctx.respond(f"An error occurred: {response['message']}")
            return

        matches = response.get("matches")
        if not matches:
            await ctx.respond("No upcoming matches found")
            return

        # Get the date and time of the next match
        current_match = None
        for match in matches:
            if match["status"] == "FINISHED":
                current_match = match
            else:
                next_match = match
                break

        if current_match:
            next_match_date = parser.parse(next_match["utcDate"]).astimezone(timezone("Europe/London"))
            next_match_date_string = next_match_date.strftime("%a, %b %d %Y %I:%M %p %Z")
            await ctx.respond(f"The last Arsenal match was played against {current_match['awayTeam']['name']} on {current_match['utcDate']}. The next match is against {next_match['homeTeam']['name']} on {next_match_date_string}.")
        else:
            next_match_date = parser.parse(next_match["utcDate"]).astimezone(timezone("Europe/London"))
            next_match_date_string = next_match_date.strftime("%a, %b %d %Y %I:%M %p %Z")
            opponent = next_match["homeTeam"]["name"] if next_match["awayTeam"]["id"] == self.ARSENAL_TEAM_ID else next_match["awayTeam"]["name"]
            await ctx.respond(f"The next Arsenal match is against {opponent} on {next_match_date_string}")
    
def setup(bot):
    bot.add_cog(PXBot(bot))
