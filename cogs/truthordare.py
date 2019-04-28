import discord
import random
from discord.ext import commands
import redis

class TruthOrDare(commands.Cog):
    def __init__(self, bot, r):
        self.bot = bot
        self.r = r

    @commands.command()
    async def addTruth(self, ctx, *, truth : str):
        self.r.lpush("truths", truth)
        await ctx.send("truth added!")

    @commands.command()
    async def addDare(self, ctx, *, truth : str):
        self.r.lpush("dares", truth)
        await ctx.send("dare added!")

    @commands.command()
    @commands.is_owner()
    async def truth(self, ctx):
        length = self.r.llen("truths")
        if length == 0:
            await ctx.send("no more truths")
            return
        truth = self.r.lindex("truths", random.randrange(length)).decode()
        self.r.lrem("truths", 0, truth)
        await ctx.send(truth)

    @commands.command()
    @commands.is_owner()
    async def dare(self, ctx):
        length = self.r.llen("dares")
        if length == 0:
            await ctx.send("no more dares")
            return
        dare = self.r.lindex("dares", random.randrange(length)).decode()
        self.r.lrem("dares", 0, dare)
        await ctx.send(dare)
