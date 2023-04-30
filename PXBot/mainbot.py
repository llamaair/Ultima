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

        # Find the next upcoming match that hasn't already happened
        for match in matches:
            match_date = parser.isoparse(match["utcDate"]).astimezone(timezone("Europe/London"))
            if match_date > datetime.now(timezone("Europe/London")):
                next_match = match
                break
        else:
            await ctx.respond("No upcoming matches found")
            return

        # Get the date and time of the next match
        match_date_string = match_date.strftime("%a, %b %d %Y %I:%M %p %Z")

        # Get the opponent
        home_team = next_match.get("homeTeam")
        away_team = next_match.get("awayTeam")
        if home_team and away_team:
            opponent = home_team["name"] if home_team["id"] != self.ARSENAL_TEAM_ID else away_team["name"]
        else:
            opponent = "Unknown"

        # Create the embed
        embed = discord.Embed(title="Next Arsenal Match", description=f"Against {opponent} on {match_date_string}", color=discord.Color.green())
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(PXBot(bot))
