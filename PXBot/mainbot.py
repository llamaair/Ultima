import discord
import os
import requests
from datetime import datetime
from pytz import timezone
from bs4 import BeautifulSoup
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

    @bridge.bridge_command()
    async def movie(self, ctx, category:discord.Option(choices=["action", "comedy", "drama", "horror", "romance", "sci_fi", "thriller"]), amount=1):
        await ctx.defer()
        url = f"https://www.imdb.com/search/title?genres={category}"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        movies = soup.select('.lister-item-header a')

        if not movies:
            await ctx.respond(f"No {category} movies found :pensive:")
            return

        movielist = [movie.text for movie in movies][:int(amount)]

        if int(amount) == 1:
            movie = movies[0].text
            await ctx.respond(f"Here's a {category} movie I suggest: {movie}")
        else:
            await ctx.respond(f"Here are {amount} movies I suggest in the category: {category}:\n" + "\n".join(movielist))



def setup(bot):
    bot.add_cog(PXBot(bot))
