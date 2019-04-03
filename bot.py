import discord
from discord.ext import commands

import configparser
import aiohttp

from cogs.administration import Administration
from cogs.query import Query
from cogs.serverutils import ServerUtils
from cogs.economy import Economy
from cogs.mathgames import MathGames

prefix = '?'
bot = commands.Bot(command_prefix=prefix)

async def load_cogs(session):
    bot.add_cog(Administration(bot))
    bot.add_cog(Query(bot, session))
    bot.add_cog(ServerUtils(bot))
    bot.add_cog(Economy(bot, session))
    bot.add_cog(MathGames(bot, session))

@bot.event
async def on_ready():
    session = aiohttp.ClientSession()
    await load_cogs(session)
    print("I am combat ready!")

config = configparser.ConfigParser()
config.read('config.ini')
bot.run(config.get('tokens', 'DISCORD_TOKEN_1'))
