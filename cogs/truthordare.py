import discord
import random
from discord.ext import commands
import redis

class TruthOrDare(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def addTruth(self, ctx, *, truth : str):
        self.bot.r.sadd("truths", truth)
        await ctx.send("truth added!")

    @commands.command()
    async def addDare(self, ctx, *, truth : str):
        self.bot.r.sadd("dares", truth)
        await ctx.send("dare added!")

    @commands.command()
    @commands.is_owner()
    async def truth(self, ctx):
        length = self.bot.r.scard("truths")
        if length == 0:
            await ctx.send("no more truths")
            return
        await ctx.send(self.bot.r.spop("truths").decode())

    @commands.command()
    @commands.is_owner()
    async def dare(self, ctx):
        length = self.bot.r.scard("dares")
        if length == 0:
            await ctx.send("no more dares")
            return
        await ctx.send(self.bot.r.spop("truths").decode())

def setup(bot):
    bot.add_cog(TruthOrDare(bot))
