import discord
from discord.ext import commands

import configparser
import aiohttp
import redis

prefix = '?'
help_command = commands.DefaultHelpCommand(dm_help=True)
extensions = (
    "cogs.administration",
    "cogs.query",
    "cogs.serverutils",
    "cogs.economy",
    "cogs.mathgames",
    "cogs.latexgames",
    "cogs.utility",
    "cogs.dictionary",
    "cogs.truthordare",
    "cogs.storage"
)

prefix = '?'

class CutieBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop.create_task(self.__ainit__(self, *args, **kwargs))

    async def __ainit__(self, *args, **kwargs):
        await self.wait_until_ready()
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.r = redis.Redis(
            host="127.0.0.1",
            port="6379"
        )
        for extension in extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                print('extension {} failed to load'.format(extension))
                print(e)

    async def on_ready(self):
        print(self.user.name)
        print("I am combat ready!")


bot = CutieBot(command_prefix=prefix, help_command = help_command)

config = configparser.ConfigParser()
config.read('config.ini')
bot.run(config.get('tokens', 'DISCORD_TOKEN_0'))
