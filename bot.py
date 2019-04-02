import discord
from discord.ext import commands

import configparser

prefix = '?'
bot = commands.Bot(command_prefix=prefix)

@bot.command()
async def ping(ctx):
    await ctx.send("pong!")

@bot.event
async def on_ready():
    print("I am combat ready!")

config = configparser.ConfigParser()
config.read('config.ini')
bot.run(config.get('tokens', 'DISCORD_TOKEN_1'))
