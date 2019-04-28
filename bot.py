import discord
from discord.ext import commands

import configparser
import aiohttp
import redis

from cogs.administration import Administration
from cogs.query import Query
from cogs.serverutils import ServerUtils
from cogs.economy import Economy
from cogs.mathgames import MathGames
from cogs.latexgames import LatexGames
from cogs.utility import Utility
from cogs.dictionary import Dictionary
from cogs.truthordare import TruthOrDare
from cogs.storage import Storage

prefix = '?'
help_command = commands.DefaultHelpCommand(dm_help=True)
bot = commands.Bot(command_prefix=prefix, help_command = help_command)

def setup():
    r = redis.Redis(
        host="127.0.0.1",
        port="6379"
    )
    session = aiohttp.ClientSession()
    bot.add_cog(Administration(bot))
    bot.add_cog(Query(bot, session))
    bot.add_cog(ServerUtils(bot))
    bot.add_cog(Economy(bot, session))
    bot.add_cog(MathGames(bot, session))
    bot.add_cog(Dictionary(bot, session))
    bot.add_cog(Utility(bot))
    bot.add_cog(LatexGames(bot, session))
    bot.add_cog(TruthOrDare(bot, r))
    bot.add_cog(Storage(bot, r))

@bot.event
async def on_ready():
    setup()
    print("I am combat ready!")

config = configparser.ConfigParser()
config.read('config.ini')
bot.run(config.get('tokens', 'DISCORD_TOKEN_1'))
