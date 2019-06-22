import asyncio
import discord
from discord.ext import commands
from utils import bitecoin
from utils.bitecoin import add_exp, add_coins
import random

letters = {"🇦" : "A", "🇧" : "B", "🇨" : "C", "🇩" : "D", "🇪" : "E"}
numbers = {"0\u20E3" : "0", "1\u20E3" : "1", "2\u20E3" : "2", "3\u20E3" : "3", "4\u20E3" : "4", "5\u20E3" : "5", "6\u20E3" : "6", "7\u20E3" : "7", "8\u20E3" : "8", "9\u20E3" : "9"}

class MathGames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def quiz(self, ctx):
        """Generates and sends a single simple math problem."""
        exp = 5
        coins = 50
        timeout = 7.5
        operator_tuple = (" * ", " + ", " - ")
        # generate problem
        info = [[str(int(random.random() * 10) + 1) for k in range(4)],
            [operator_tuple[int(random.random() * 3)] for k in range(3)]]
        length = random.randint(2,4) * 2 - 1
        expression_string = ""
        if (int(random.random() * 3) == 0):
            expression_string += "-"
        for i in range(length):
            expression_string += info[i % 2][i // 2]

        answer = str(eval(expression_string))

        def check(message):
            return message.channel.id == ctx.message.channel.id and message.content == answer

        question_message = await ctx.send(expression_string)

        print(answer)

        try:
            msg = await self.bot.wait_for("message", timeout = timeout, check=check)
            seconds = (msg.created_at - question_message.created_at).total_seconds()
            await ctx.send(msg.author.mention + " wins! That took " + str(seconds) + " seconds. (+{0} exp, +{1} bitecoins!)".format(str(exp), str(coins)))
            return {"user" : msg.author, "channel" : ctx.message.channel, "exp" : exp, "coins" : coins}
        except asyncio.TimeoutError:
            return 0

    @commands.command(aliases=["quickmaffs"])
    async def mathquiz(self, ctx):
        """Wrapper for quiz function."""
        result = await self.quiz(ctx)
        if result != 0:
            await add_exp(self.bot.session, ctx, result["user"], result["exp"])
            await add_coins(self.bot.session, ctx, result["user"], result["coins"])
        else:
            await ctx.send("too slow")

    @commands.command(aliases=["maffstream"])
    async def quizstream(self, ctx):
        """Wrapper for quiz function, but automatically refreshing."""
        # stores rewards and gives at end
        rewards = {}
        while True:
            result = await self.quiz(ctx)

            if result != 0:
                if not result["user"].id in rewards:
                    rewards[result["user"].id] = {"coins" : 0, "exp" : 0}
                rewards[result["user"].id]["coins"] += result["coins"]
                rewards[result["user"].id]["exp"] += result["exp"]
            else:
                await ctx.send("too slow")
                break

        for i in rewards:
            await add_exp(self.bot.session, ctx, self.bot.get_user(i), rewards[i]["exp"])
            await add_coins(self.bot.session, ctx, self.bot.get_user(i), rewards[i]["coins"])

def setup(bot):
    bot.add_cog(MathGames(bot))
