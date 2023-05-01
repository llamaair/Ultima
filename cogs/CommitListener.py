import os
import requests
import discord
import asyncio
from discord.ext import commands, tasks

class CommitListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_commit_sha = None
        self.check_for_commits.start()

    @tasks.loop(minutes=10)
    async def check_for_commits(self):
        try:
            # Get the latest commit SHA from GitHub
            response = requests.get('https://api.github.com/repos/llamaair/Xavier-Bot/branches/main')
            response.raise_for_status()
            latest_commit_sha = response.json()['commit']['sha']

            # Check if the latest commit SHA is different from the previous one
            if latest_commit_sha != self.last_commit_sha:
                # Quit the Discord client
                await self.bot.close()
                print('Bot has quit due to a new commit.')

            # Update the last commit SHA
            self.last_commit_sha = latest_commit_sha
        except requests.exceptions.RequestException as e:
            print(f'Request failed: {str(e)}')
            await asyncio.sleep(60)  # Wait for 60 seconds before retrying

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready.')

def setup(bot):
    bot.add_cog(CommitListener(bot))
