import os
import requests
import discord
from discord.ext import commands, tasks, bridge

class CommitListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_commit_sha = None
        self.check_for_commits.start()

    @tasks.loop(minutes=1)
    async def check_for_commits(self):
        # Get the latest commit SHA from GitHub
        response = requests.get('https://api.github.com/repos/llamaair/Xavier-Bot/branches/main')
        latest_commit_sha = response.json()['commit']['sha']

        # Check if the latest commit SHA is different from the previous one
        if latest_commit_sha != self.last_commit_sha:
            # Quit the Discord client
            await self.bot.close()
            print('Bot has automatically quit due to a new commit.')

        # Update the last commit SHA
        self.last_commit_sha = latest_commit_sha

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot cog is ready.')

def setup(bot):
    bot.add_cog(CommitListener(bot))
