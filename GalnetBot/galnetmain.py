import discord
import aiohttp
import asyncio
from discord.ext import commands, bridge

class GalNetCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.galnet_task = self.bot.loop.create_task(self.check_for_galnet_articles())

    def cog_unload(self):
        self.galnet_task.cancel()

    async def get_galnet_articles(self):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://community.elitedangerous.com/galnet/') as resp:
                if resp.status != 200:
                    return None
                data = await resp.text()
                return data

    async def check_for_galnet_articles(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(1078626878199439380) # Replace with your channel ID

        while not self.bot.is_closed():
            galnet_data = await self.get_galnet_articles()

            # Parse the data for the latest news article
            # Assuming that the latest article is at the top of the page
            article_start = galnet_data.find('<div class="news-title">')
            article_end = galnet_data.find('</div>', article_start) + 6
            article_data = galnet_data[article_start:article_end]

            # Send the article to the channel
            await channel.send(article_data)

            # Wait 5 minutes before checking again
            await asyncio.sleep(300)

    @bridge.bridge_command(name='galnet', help='Starts sending GalNet news articles to a specified channel.')
    async def start_galnet(self, ctx):
        await ctx.send('Starting to send GalNet news articles.')
        self.galnet_task = self.bot.loop.create_task(self.check_for_galnet_articles())

    @bridge.bridge_command(name='stopgalnet', help='Stops sending GalNet news articles.')
    async def stop_galnet(self, ctx):
        await ctx.send('Stopping to send GalNet news articles.')
        self.galnet_task.cancel()

def setup(bot):
    bot.add_cog(GalNetCog(bot))
