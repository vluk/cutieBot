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
from cogs.dictionary import Dictionary
from cogs.connect import Connect

prefix = '?'
help_command = commands.DefaultHelpCommand(dm_help=True)
bot = commands.Bot(command_prefix=prefix, help_command = help_command)

async def setup():
    session = aiohttp.ClientSession()
    bot.add_cog(Administration(bot))
    bot.add_cog(Query(bot, session))
    bot.add_cog(ServerUtils(bot))
    bot.add_cog(Economy(bot, session))
    bot.add_cog(MathGames(bot, session))
    bot.add_cog(Dictionary(bot, session))
    bot.add_cog(Utility(bot))
    bot.add_cog(Connect(bot, session))

async def process_commands(bot, message):
    ctx = await bot.get_context(message)
    await bot.invoke(ctx)

@bot.event
async def on_message(message):
    await process_commands(bot, message)

@bot.event
async def on_ready():
    await setup()
    print("I am combat ready!")

config = configparser.ConfigParser()
config.read('config.ini')
bot.run(config.get('tokens', 'DISCORD_TOKEN_0'))
