import discord
from discord.ext import bridge, commands

class recording(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    connections = {}

    @bridge.bridge_command(description="Start recording in a voice channel")
    async def record(self, ctx):
        voice = ctx.author.voice

        if not voice:
            await ctx.respond("You are not in a voice channel!")
        
        vc = await voice.channel.connect()
        self.connections.update({ctx.guild.id: vc})

        vc.start_recording(
            discord.sinks.WaveSink(),
            self.once_done,
            ctx.channel,
            ctx.author.id
        )

        await ctx.respond("Started recording!")

    async def once_done(self, sink: discord.sinks, channel:discord.TextChannel, user_id, *args):
        recorded_users = [
            f"<@{self.user_id}>"
            for user_id, audio in sink.audio_data.items()

        ]
        await sink.vc.disconnect()
        files = [discord.File(self.audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()]
        await channel.send(f"Finished recording audio for: {', '.join(recorded_users)}.", files=files)

    @bridge.bridge_command(description="Stop the recording")
    async def stop_recording(self, ctx):
        if ctx.guild.id in self.connections:
            vc = self.connections[ctx.guild.id]
            vc.stop_recording()
            del self.connections[ctx.guild.id]
            await ctx.delete()
        else:
            await ctx.respond("I am currently not recording here", ephemeral=True)

def setup(bot):
    bot.add_cog(recording(bot))