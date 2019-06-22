import discord
from discord.ext import commands
import datetime
import redis

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Pings the bot."""
        msg = await ctx.send("pong!")
        time_elapsed = msg.created_at - ctx.message.created_at
        await ctx.send("that took {0} seconds".format(str(time_elapsed.total_seconds())))

def setup(bot):
    bot.add_cog(Utility(bot))
