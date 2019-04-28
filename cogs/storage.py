import discord
from discord.ext import commands
import redis

class Storage(commands.Cog):
    def __init__(self, bot, r):
        self.bot = bot
        self.r = r

    @commands.command()
    async def addMeme(self, ctx, name, *, value : str):
        if self.r.hexists("memes", name):
            await ctx.send("already exists!")
        else:
            self.r.hmset("memes", {name : value})
            await ctx.send("added!")

    @commands.command()
    async def meme(self, ctx, name):
        if self.r.hexists("memes", name):
            await ctx.send(self.r.hget("memes", name).decode())
        else:
            await ctx.send("not found!")

    @commands.command()
    @commands.is_owner()
    async def removeMeme(self, ctx, name):
        if self.r.hexists("memes", name):
            self.r.hdel("memes", name)
            await ctx.send("removed!")
        else:
            await ctx.send("doesnt exist!")

    @commands.command()
    async def memes(self, ctx):
        if self.r.hlen("memes") == 0:
            await ctx.send("there arent any memes right now!")
        else:
            meme_list = self.r.hkeys("memes")
            decoded_list = [i.decode() for i in meme_list]
            await ctx.send("```{}```".format("\n".join(decoded_list)))
