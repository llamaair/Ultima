import discord
from discord.ext import commands, bridge
import json

class autorole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(description="Enable or disable auto role")
    @bridge.has_permissions(administrator=True)
    async def autorole(self, ctx, role: discord.Role):
        ena=None
        with open("autoroleg.json", "r") as f:
            automodguild = json.load(f)

        if str(ctx.guild.id) not in automodguild:
            automodguild.append(str(ctx.guild.id))
            ena ="enabled"
        else:
            automodguild.remove(str(ctx.guild.id))
            ena="disabled"

        with open("autoroleg.json", "w") as f:
            json.dump(automodguild, f)

        with open("autorole.json", "r") as f:
            smsgs = json.load(f)
        smsgs[str(ctx.guild.id)] = str(role.id)
        with open("autorole.json", "w") as f:
            json.dump(smsgs, f)
        embed = discord.Embed(title="Success!", color=discord.Colour.green(), description=f"Successfully {ena} autorole!")
        await ctx.respond(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open("autorole.json", "r") as f:
            rollo = json.load(f)
        role_id = rollo.get(str(member.guild.id))
        if role_id:
            role = member.guild.get_role(int(role_id))
            if role:
                try:
                    await member.add_roles(role)
                except:
                    await member.guild.owner.send(f"Hey! It looks like I'm not able to assign roles when new users join. This is probably as the role I'm trying to assign is higher in the hierarchy than my highest role!")

def setup(bot):
    bot.add_cog(autorole(bot))
