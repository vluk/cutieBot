import discord
from discord.ext import commands
import redis

class Storage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def addMeme(self, ctx, name, *, value : str):
        if self.bot.r.hexists("memes", name):
            await ctx.send("already exists!")
        else:
            self.bot.r.hmset("memes", {name : value})
            await ctx.send("added!")

    @commands.command()
    async def meme(self, ctx, name):
        if self.bot.r.hexists("memes", name):
            await ctx.send(self.bot.r.hget("memes", name).decode())
        else:
            await ctx.send("not found!")

    @commands.command()
    @commands.is_owner()
    async def removeMeme(self, ctx, name):
        if self.bot.r.hexists("memes", name):
            self.bot.r.hdel("memes", name)
            await ctx.send("removed!")
        else:
            await ctx.send("doesnt exist!")

    @commands.command()
    async def memes(self, ctx):
        if self.bot.r.hlen("memes") == 0:
            await ctx.send("there arent any memes right now!")
        else:
            meme_list = self.bot.r.hkeys("memes")
            decoded_list = [i.decode() for i in meme_list]
            await ctx.send("```{}```".format("\n".join(decoded_list)))
def setup(bot):
    bot.add_cog(Storage(bot))
