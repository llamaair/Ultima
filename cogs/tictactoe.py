import discord
from discord.ext import commands, bridge

class TicTacToeView(discord.ui.View):
    def __init__(self, player1, player2):
        super().__init__()

        self.player1 = player1
        self.player2 = player2

        self.current_player = player1
        self.moves = [None] * 9

        for i in range(9):
            button = discord.ui.Button(label="\u200b", custom_id=str(i), style=discord.ButtonStyle.secondary)
            self.add_item(button)

    async def interaction_check(self, interaction):
        return interaction.user == self.current_player

    async def on_timeout(self):
        await self.message.edit(view=None)
        await self.message.channel.send("Game ended due to inactivity.")

    async def on_item_update(self, interaction):
        index = int(interaction.custom_id)

        if self.moves[index] is not None:
            await interaction.response.send_message("This square is already taken.", ephemeral=True)
            return

        if self.current_player == self.player1:
            self.moves[index] = "X"
            button_style = discord.ButtonStyle.primary
            self.current_player = self.player2
        else:
            self.moves[index] = "O"
            button_style = discord.ButtonStyle.danger
            self.current_player = self.player1

        button = self.children[index]
        button.label = self.moves[index]
        button.style = button_style

        if self.check_win():
            await self.message.edit(view=None)
            await self.message.channel.send(f"{self.current_player.mention} wins!")
        elif self.check_tie():
            await self.message.edit(view=None)
            await self.message.channel.send("It's a tie.")

    def check_win(self):
        win_conditions = [
            # horizontal
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            # vertical
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            # diagonal
            (0, 4, 8),
            (2, 4, 6),
        ]

        for condition in win_conditions:
            a, b, c = condition
            if self.moves[a] == self.moves[b] == self.moves[c] and self.moves[a] is not None:
                return True

        return False

    def check_tie(self):
        return all(move is not None for move in self.moves)

class TicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command()
    async def tictactoe(self, ctx, opponent: discord.Member):
        if opponent.bot:
            await ctx.send("You can't play against a bot.")
            return

        view = TicTacToeView(ctx.author, opponent)
        message = await ctx.send(f"{opponent.mention}, {ctx.author.mention} challenged you to a game of tic-tac-toe!", view=view)
        view.message = message

        await view.wait()

def setup(bot):
    bot.add_cog(TicTacToe(bot))
