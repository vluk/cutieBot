import discord
from discord.ext import commands

import configparser

import aiohttp
import json
from urllib import request, parse

config = configparser.ConfigParser()
config.read('config.ini')
BITEAPI_KEY = config.get('keys', 'BITEAPI_KEY')

async def get_list(session, user_id):
    url = "http://jennythepython.pythonanywhere.com/playerCoins/" + user_id
    async with session.get(url) as resp:
        info = await resp.json()
        return info

async def get_leaderboard(session):
    async with session.get("https://jennythepython.pythonanywhere.com/leaderboard") as resp:
        leaderboard = (await resp.json())["leaderboard"]
        return leaderboard

async def get_coins(session, user_id):
    info = await get_list(session, str(user_id))
    return info["coins"]

async def get_level(session, user_id):
    info = await get_list(session, str(user_id))
    return info["level"]

async def get_xp(session, user_id):
    info = await get_list(session, str(user_id))
    return info["xp"]

async def check_coins(session, user_id):
    return (await get_list(session, str(user_id)))["message"] != "unknown player"

async def post_coins(session, name, user_id, dcoins, dxp, level):
    payload = {"name" : name, "apiKey" : BITEAPI_KEY, "dcoins" : dcoins, "dxp" : dxp, "level" : level}
    url = 'http://jennythepython.pythonanywhere.com/playerCoins/'+ str(user_id)
    async with session.post(url, data=payload) as resp:
        print(await resp.text())

def next_exp(level):
    total = 0
    for i in range(level + 1):
        total += 100 * int(3 ** (i / 10))
    return total

async def add_exp(session, ctx, user, amount):
    exp = 0
    level = 0
    if await check_coins(session, user.id):
        exp = await get_xp(session, user.id)
        level = await get_level(session, user.id)
    exp += amount
    while exp > next_exp(level):
        level += 1
        link = "https://api.giphy.com/v1/gifs/search?q=bunny&api_key=INJuIdbai3pyu6J4Kk0HFikfDanmbZMM&limit=100"
        async with session.get(url) as resp:
            congrats_link_objects = (await resp.json())["data"]
            congrats_link_object = congrats_link_objects[int(random.random() * len(congrats_link_objects))]
            congrats_link = congrats_link_objects["images"]["fixed_height"]["url"]
            congrats_link = congrats_link.replace("\\/", "/")
            print(congratsLink)
            embed = discord.Embed(
                title = "Level Up!",
                description = "Congrats! You are now level `" + str(level) + "`!"
            )
            embed.set_thumbnail(url = congratsLink)
            embed.set_author(name = user.name, icon_url = user.avatar_url)

            await ctx.send(embed = embed)
    await post_coins(session, user.name, user.id, 0, amount, level)

async def add_coins(session, ctx, user, amount):
    await post_coins(session, user.name, user.id, amount, 0, await get_level(session, user.id))
