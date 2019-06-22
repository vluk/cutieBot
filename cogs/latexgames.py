import asyncio
import discord
from discord.ext import commands
from utils.latex import generate_image
from utils import bitecoin
from utils.bitecoin import add_exp, add_coins
from utils.amc import get_amc, get_aime
import random
import os


letters = {"🇦" : "A", "🇧" : "B", "🇨" : "C", "🇩" : "D", "🇪" : "E"}
numbers = {"0\u20E3" : "0", "1\u20E3" : "1", "2\u20E3" : "2", "3\u20E3" : "3", "4\u20E3" : "4", "5\u20E3" : "5", "6\u20E3" : "6", "7\u20E3" : "7", "8\u20E3" : "8", "9\u20E3" : "9"}

class LatexGames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["slowmaffs"])
    async def amc(self, ctx):
        """Quizzes a random AMC 12 problem."""
        coins = 1500
        exp = 150
        amc = await get_amc(self.bot.session)
        amc_tex = amc["latex"]
        amc_answer = amc["answer"]
        fn = await generate_image("", amc_tex)
        message = await ctx.send(file=discord.File(fn))


        os.system("rm " + fn)

        for i in letters:
            await message.add_reaction(i)

        tried = []

        def check(reaction, user):
            return (
                reaction.message.id == message.id
                and reaction.emoji in letters
                and not user.id in tried
                and user.id != message.author.id
            )

        while True:
            reaction, user = await self.bot.wait_for("reaction_add", check=check)
            print("heyo")
            print(letters[reaction.emoji], amc_answer)
            if letters[reaction.emoji] == amc_answer:
                if await bitecoin.get_coins(self.bot.session, user.id) < coins // 4:
                    await (user.mention + " you're too poor to play!")
                else:
                    bitecoin_string = user.mention+" wins! (+{0} bitecoins, +{1} XP)".format(
                        str(coins),
                        str(exp)
                    )
                    problem_string = "That was problem {0} from the {1} AMC 12{2}".format(
                        str(amc["problem"] + 1),
                        amc["year"],
                        amc["version"]
                    )
                    success_string = "{0}\n{1}".format(bitecoin_string, problem_string)
                    await ctx.send(success_string)
                    await add_coins(self.bot.session, ctx, user, coins)
                    await add_exp(self.bot.session, ctx, user, exp)
                    break
            else:
                if await bitecoin.get_coins(self.bot.session, user.id) < coins // 4:
                    await ctx.send(user.mention + " you're too poor to play!")
                else:
                    tried.append(user.id)
                    await ctx.send(user.mention+" wrong! (-{0} bitecoins)".format(coins // 4))
                    await add_coins(self.bot.session, ctx, user, -1 * (coins // 4))

    @commands.command(aliases=["hardmaffs"])
    async def aime(self, ctx):
        """Quizzes a random AIME problem."""
        coins = 3000
        exp = 300
        aime = await get_aime(self.bot.session)
        aime_tex = aime["latex"]
        aime_answer = aime["answer"]
        fn = await generate_image("", aime_tex)
        message = await ctx.send(file=discord.File(fn))

        os.system("rm " + fn)

        for i in numbers:
            await message.add_reaction(i)

        tried = []
        answers = {}

        def check(reaction, user):
            return (
                reaction.message.id == message.id
                and reaction.emoji in numbers
                and not user.id in tried
                and user.id != message.author.id
            )

        while True:
            # get number response
            reaction, user = await self.bot.wait_for("reaction_add", check=check)
            print("heyo")
            print(numbers[reaction.emoji], aime_answer)
            if not user.id in answers:
                answers[user.id] = ""
            answers[user.id] += numbers[reaction.emoji]
            if len(answers[user.id]) == 3:
                if answers[user.id] == aime_answer:
                    bitecoin_string = user.mention+" wins! (+{0} bitecoins, +{1} XP)".format(
                        str(coins),
                        str(exp)
                    )
                    problem_string = "That was problem {0} from the {1} AIME {2}".format(
                        str(aime["problem"] + 1),
                        aime["year"],
                        aime["version"]
                    )
                    success_string = "{0}\n{1}".format(bitecoin_string, problem_string)
                    await add_coins(self.bot.session, ctx, user, coins)
                    await add_exp(self.bot.session, ctx, user, exp)
                    await ctx.send(success_string)
                    break
                else:
                    await ctx.send(user.mention + " wrong!")
                    tried.append(user.id)

def setup(bot):
    bot.add_cog(LatexGames(bot))
