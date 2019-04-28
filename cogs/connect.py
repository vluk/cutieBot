import discord
from discord.ext import commands
from utils import bitecoin
from utils.bitecoin import add_exp, add_coins
import asyncio

class Connect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.nums = ["1\u20E3", "2\u20E3", "3\u20E3", "4\u20E3", "5\u20E3", "6\u20E3", "7\u20E3"]
        self.black = "⚫"
        self.blue = "🔵"
        self.red = "🔴"

    async def drop(self, board, place, color):
        for i in list(reversed(range(len(board)))):
            if (board[i][place] == 0):
                board[i][place] = color
                return [i, place]

    async def check_victory(self, pos, board, color):
        for i in range(len(board) - 3):
            if (all([board[i + j][pos[1]] == color for j in range(4)])):
                return True
        for i in range(len(board[0]) - 3):
            if (all([board[pos[0]][i + j] == color for j in range(4)])):
                return True
        down = 5 - pos[0]
        top = pos[0]
        left = pos[1]
        right = 6 - pos[1]
        nw_dist = min(top, left)
        sw_dist = min(down, left)
        se_dist = min(down, right)
        ne_dist = min(top, right)
        for i in range(4):
            if (nw_dist >= 3 - i and se_dist >= i):
                if (all([board[pos[0] + j + i - 3][pos[1] + j + i - 3] == color
                    for j in range(4)])):
                    return True
            if (sw_dist >= 3 - i and ne_dist >= i):
                if (all([board[pos[0] - (i - 3) - j][pos[1] + j + i - 3] == color
                    for j in range(4)])):
                    return True
        return False

    async def generate_board(self, board):
        output = ""
        for i in board:
            for j in i:
                if (j == 0):
                    output += self.black
                if (j == 1):
                    output += self.blue
                if (j == 2):
                    output += self.red
            output += "\n"
        for i in self.nums:
            output += i
        return output

    async def generate_winning_board(self, board):
        output = ""
        for i in board:
            for j in i:
                if (j == 0):
                    output += self.black
                if (j == 1):
                    output += self.blue
                if (j == 2):
                    output += self.red
            output += "\n"
        return output

    @commands.command()
    async def connect(self, ctx, person : discord.Member=None, timeout : int=None):
        first = ctx.message.author
        second = person

        board = [[0 for i in range(7)] for j in range(6)]

        turn = first
        not_turn = second
        first_turn = True
        turn_count = 0

        first_embed = discord.Embed(
            title = "VS",
            description = "..."
        )
        first_embed.set_author(
            name = first.name,
            icon_url = first.avatar_url
        )
        if second == None:
            first_embed.set_footer(
                text = "???",
                icon_url = "https://vignette.wikia.nocookie.net/youtubepedia/images/d/dd/Discord.png/revision/latest?cb=20180125115059&path-prefix=es"
            )
        else:
            first_embed.set_footer(
                text = second.name,
                icon_url = second.avatar_url
            )

        message = await ctx.send(
            await self.generate_board(board),
            embed = first_embed
        )

        for i in self.nums:
            await message.add_reaction(i)

        while (True):

            def check(reaction, user):
                return (
                    reaction.message.id == message.id
                    and reaction.emoji in self.nums
                    and (turn == None or user.id == turn.id)
                )

            current_timeout = timeout
            if first_turn:
                current_timeout = None
            try:
                reaction, member = await self.bot.wait_for(
                    "reaction_add",
                    check=check,
                    timeout=current_timeout
                )
            except asyncio.TimeoutError:
                winning_description = "Opponent timed out."
                winning_embed = discord.Embed(
                    title = "Winner",
                    description = winning_description)
                winning_embed.set_author(
                    name = not_turn.name,
                    icon_url = not_turn.avatar_url)
                winning_embed.set_footer(
                    text = turn.name,
                    icon_url = turn.avatar_url)

                await message.edit(
                    content = await self.generate_winning_board(board),
                    embed = winning_embed
                )
            else:
                emoji = reaction.emoji

                place = self.nums.index(emoji)

                if (turn == None and board[0][place] == 0):
                    second = member
                    turn = second

                if (turn == member and board[0][place] == 0):

                    turn_count = turn_count + 1

                    await message.remove_reaction(emoji, member)

                    if (turn == first and first_turn):
                        color = 1
                        first_turn = False
                    elif (turn == second and not first_turn):
                        color = 2
                        first_turn = True

                    pos = await self.drop(board, place, color)

                    if (await self.check_victory(pos, board, color)):
                        await message.clear_reactions()

                        winning_description = "That took " + str(turn_count) + " turns."

                        if turn.id != not_turn.id:
                            winning_description += " (+100 exp, +1000 bitecoins!)"
                            await add_exp(self.bot.session, ctx, turn, 100)
                            await add_coins(self.bot.session, ctx, turn, 1000)

                        winning_embed = discord.Embed(
                            title = "Winner",
                            description = winning_description)
                        winning_embed.set_author(
                            name = turn.name,
                            icon_url = turn.avatar_url)
                        winning_embed.set_footer(
                            text = not_turn.name,
                            icon_url = not_turn.avatar_url)

                        await message.edit(
                            content = await self.generate_winning_board(board),
                            embed = winning_embed
                        )
                        return

                    if (second != None):
                        new_embed = discord.Embed(
                            title = "VS",
                            description = "..."
                        )
                        new_embed.set_footer(
                            text = not_turn.name,
                            icon_url = not_turn.avatar_url
                        )
                        new_embed.set_author(
                            name = turn.name,
                            icon_url = turn.avatar_url
                        )
                    else:
                        new_embed = discord.Embed( 
                            title = "VS",
                            description = "..."
                        )
                        new_embed.set_author(
                            name = "???",
                            icon_url = "https://vignette.wikia.nocookie.net/youtubepedia/images/d/dd/Discord.png/revision/latest?cb=20180125115059&path-prefix=es"
                        )
                        new_embed.set_footer(
                            text = first.name,
                            icon_url = first.avatar_url
                        )

                    await message.edit(
                        content = await self.generate_board(board),
                        embed = new_embed
                    )

                    if (turn == first):
                        turn = second
                        not_turn = first
                    else:
                        turn = first
                        not_turn = second

def setup(bot):
    bot.add_cog(Connect(bot))
