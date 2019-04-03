import discord
from discord.ext import commands

import configparser
import aiohttp

from cogs.administration import Administration
from cogs.query import Query
from cogs.serverutils import ServerUtils
from cogs.economy import Economy
from cogs.mathgames import MathGames
from cogs.utility import Utility

prefix = '?'
help_command = commands.DefaultHelpCommand(dm_help=True)
bot = commands.Bot(command_prefix=prefix, help_command = help_command)

async def setup(session):
    bot.add_cog(Administration(bot))
    bot.add_cog(Query(bot, session))
    bot.add_cog(ServerUtils(bot))
    bot.add_cog(Economy(bot, session))
    bot.add_cog(MathGames(bot, session))
    bot.add_cog(Utility(bot))

@bot.event
async def on_ready():
    session = aiohttp.ClientSession()
    await setup(session)
    print("I am combat ready!")

config = configparser.ConfigParser()
config.read('config.ini')
bot.run(config.get('tokens', 'DISCORD_TOKEN_0'))
