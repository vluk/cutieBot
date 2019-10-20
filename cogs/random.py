import discord
import random
from discord.ext import commands

class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def thanos(self, ctx, *, words : str):
        list_words = words.split()
        i = len(list_words) - 1
        while i >= 0:
            if random.getrandbits(1) == 0:
                del list_words[i]
            i -= 1
        await ctx.send("```\n" + " ".join(list_words) + "```")

    @commands.command()
    async def essaytrim(self, ctx, target : int, *, words : str):
        list_words = words.split()
        while len(list_words) > target:
            del list_words[random.randrange(len(list_words))]
        await ctx.send("```\n" + " ".join(list_words) + "```")


def setup(bot):
    bot.add_cog(Random(bot))
