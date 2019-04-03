import discord
from discord.ext import commands

import aiohttp
import urllib
import bs4

import random

import datetime
import time
import pytz

class Query(commands.Cog):
    def __init__(self, bot, session):
        self.bot = bot
        self.session = session

    @commands.command()
    async def tblr(self, ctx, *tags):
        tag = "+".join(tags)
        key = "EPqVE8md4LNeVHPRzmmwRBk1pRUpeuy70qdEv455o6ymvPA9pS"
        url = "http://api.tumblr.com/v2/tagged?tag={0}&api_key={1}".format(tag, key)
        async with self.session.get(url) as resp:
            post_dict = await resp.json()
            pic_dict = [i for i in post_dict["response"] if i["type"] == "photo"]
            rand = int(random.random() * len(pic_dict))
            await ctx.send(pic_dict[rand]["photos"][0]["original_size"]["url"])

    @commands.command()
    async def sunrise(self, ctx):
        url = "https://api.sunrise-sunset.org/json?lat=37.540135&lng=-122.236916&formatted=0"
        async with self.session.get(url) as resp:
            sunrise_json = await resp.json()
            sunrise_timestamp = sunrise_json["results"]["sunrise"]
            print(sunrise_timestamp)
            sunrise_datetime = datetime.datetime.strptime(sunrise_timestamp, "%Y-%m-%dT%H:%M:%S+00:00")
            sunrise_datetime = sunrise_datetime.replace(tzinfo=pytz.timezone('UTC'))
            sunrise_datetime = sunrise_datetime.astimezone(pytz.timezone("US/Pacific"))

            hour = sunrise_datetime.hour
            minute = sunrise_datetime.minute

            time_string = None
            if hour > 12:
                time_string = str(hour % 12) + ":" + "{0:02}".format(minute) + " PM"
            else:
                time_string = str(hour) + ":" + "{0:02d}".format(minute) + " AM"

            embed = discord.Embed(
                title = time_string,
                description = "Sunrise in Redwood City, California", 
                colour = ctx.author.colour
            )

            await ctx.send(embed=embed)

    @commands.command()
    async def sunset(self, ctx):
        url = "https://api.sunrise-sunset.org/json?lat=37.540135&lng=-122.236916&formatted=0"
        async with self.session.get(url) as resp:
            sunset_json = await resp.json()
            sunset_timestamp = sunset_json["results"]["sunset"]
            print(sunset_timestamp)
            sunset_datetime = datetime.datetime.strptime(sunset_timestamp, "%Y-%m-%dT%H:%M:%S+00:00")
            sunset_datetime = sunset_datetime.replace(tzinfo=pytz.timezone('UTC'))
            sunset_datetime = sunset_datetime.astimezone(pytz.timezone("US/Pacific"))

            hour = sunset_datetime.hour
            minute = sunset_datetime.minute

            time_string = None
            if hour > 12:
                time_string = str(hour % 12) + ":" + "{0:02}".format(minute) + " PM"
            else:
                time_string = str(hour) + ":" + "{0:02d}".format(minute) + " AM"

            embed = discord.Embed(
                title = time_string,
                description = "Sunset in Redwood City, California", 
                colour = ctx.author.colour
            )

            await ctx.send(embed=embed)

    @commands.command()
    async def imdb(self, ctx, *title_words):
        title = " ".join(title_words)
        url = "http://www.omdbapi.com/?apikey=a858832&t=" + title
        async with self.session.get(url) as resp:
            movie_info = await resp.json()
            embed = discord.Embed(
                color = 0xF5C518,
                title = movie_info["Title"],
                description = movie_info["Plot"])
            embed.set_thumbnail(url=movie_info["Poster"])
            embed.add_field(name="Rated", value=movie_info["Rated"])
            embed.add_field(name="Year", value=movie_info["Year"])
            embed.add_field(name="Score", value=(movie_info["imdbRating"] + "/10"))
            embed.add_field(name="Director", value=movie_info["Director"])
            embed.add_field(name="Genres", value=movie_info["Genre"])
            embed.set_footer(text="Info from IMDb")
            await ctx.send(embed=embed)

    @commands.command()
    async def dog(self, ctx):
        url = "https://dog.ceo/api/breeds/image/random"
        async with self.session.get(url) as resp:
            dict_dog = await resp.json()
            await ctx.send(dict_dog["message"])

    async def get_imgur(self, term):
        url = "https://api.imgur.com/3/gallery/r/{0}".format(urllib.parse.quote(term, safe=''))
        headers = {'Authorization': 'Client-ID 17fb67c0bd45585'}
        async with self.session.get(url, headers=headers) as response:
            response_json = await response.json()
            response_data = response_json["data"]
            image_data = response_data[int(random.random() * len(response_data))]
            if image_data["nsfw"]:
                image_data = "no nsfw allowed"
            return image_data["link"]

    @commands.command(aliases=["r", "imgur"])
    async def reddit(self, ctx, *, term : str):
        image_data = await self.get_imgur(term)
        await ctx.send(image_data)

    async def get_good_tord(self):
        url = "http://www.riseofsigma.com/best-truth-or-dare-questions/"
        async with self.session.get(url) as resp:
            raw_html = await resp.text()
            soup = bs4.BeautifulSoup(raw_html, "html.parser")
            truths = soup.findAll("pre")[0].string.split("\r\n\r\n")
            dares = soup.findAll("pre")[1].string.split("\r\n\r\n")
            return((truths, dares))

    @commands.command()
    async def goodTruth(self, ctx):
        truths = (await self.get_good_tord())[0]
        truth = truths[int(random.random() * len(truths))]
        await ctx.send(truth)

    @commands.command()
    async def goodDare(self, ctx):
        dares = (await self.get_good_tord())[1]
        dare = dares[int(random.random() * len(dares))]
        await ctx.send(dare)
