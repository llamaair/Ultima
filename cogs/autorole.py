import discord
from discord.ext import commands, bridge
import json

class autorole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(description="Enable or disable auto role")
    @commands.has_permissions(administrator=True)
    async def autorole(self, ctx, role: discord.Role):
        with open("autoroleg.json", "r") as f:
            automodguild = json.load(f)

        if str(ctx.guild.id) not in automodguild:
            automodguild.append(str(ctx.guild.id))
            await ctx.respond("Enabled auto role, saving settings...")
        else:
            automodguild.remove(str(ctx.guild.id))
            await ctx.respond("Disabled auto role, saving settings...")

        with open("autoroleg.json", "w") as f:
            json.dump(automodguild, f)

        with open("autorole.json", "r") as f:
            smsgs = json.load(f)
        smsgs[str(ctx.guild.id)] = str(role.id)
        with open("autorole.json", "w") as f:
            json.dump(smsgs, f)
        await ctx.respond("Set!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open("autorole.json", "r") as f:
            rollo = json.load(f)
        role_id = rollo.get(str(member.guild.id))
        if role_id:
            role = member.guild.get_role(int(role_id))
            if role:
                await member.add_roles(role)

def setup(bot):
    bot.add_cog(autorole(bot))
