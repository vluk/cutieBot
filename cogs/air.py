import discord
import asyncio
from discord.ext import commands
from utils.air_conversion import aqi_from_pm

import urllib
import aiohttp
from datetime import datetime
import json

import random

import math

quality_codes = {
    0 : ("Good", 0x859900),
    1 : ("Moderate", 0xb58900),
    2 : ("Unhealthy for Sensitive Groups", 0xcb4b16),
    3 : ("Unhealthy", 0xdc322f),
    4 : ("Very Unhealthy", 0xd33682),
    5 : ("Very Unhealthy", 0xd33682),
    6 : ("Hazaredous", 0x800000)
}

public_token = "pk.eyJ1Ijoidmx1ayIsImEiOiJjazI4ZjJ2dHMyZGtvM2NtbGJoY3hpa2M2In0.zsKK-95asNT-KZMLet9nOA"

class Air(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stations = json.loads(self.bot.r.get("stations"))
        self.headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "accept" : "application/json",
            "accept-encoding" : "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7",
            "sec-fetch-mode" : "cors",
            "sec-fetch-site" : "same-origin"
        }

    async def geocode(self, text):
        url_text = urllib.parse.quote(text, safe='')
        proximity = "-120.%2C37.5"
        url = "https://api.mapbox.com/geocoding/v5/mapbox.places/{0}.json?limit=15&proximity={1}&language=en-US&access_token={2}".format(url_text, proximity, public_token)
        async with self.bot.session.get(url) as resp:
            feature_collection = await resp.json()
            features = feature_collection["features"]
            feature = features[0]
            address = ", ".join(feature["place_name_en-US"].split(", ")[:2])
            coordinates = feature["center"]
            lon = coordinates[0]
            lat = coordinates[1]
            return address, lat, lon

    def coord_dist(self, lat1, lon1, lat2, lon2):
        R = 3959
        thet1 = math.radians(lat1)
        thet2 = math.radians(lat2)
        deltthet = math.radians(lat2-lat1)
        deltgamm = math.radians(lon2-lon1)

        a = (math.sin(deltthet/2) * math.sin(deltthet/2)
            + math.cos(thet1) * math.cos(thet2) * math.sin(deltgamm/2) * math.sin(deltgamm/2))

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        d = R * c
        return d

    async def get_closest_station_id(self, lat, lon):
        closest_id = self.stations[0]["ID"]
        closest_dist = self.coord_dist(lat, lon, self.stations[0]["Lat"], self.stations[0]["Lon"])

        for station in self.stations:
            if station["Lat"] != None and station["Lon"] != None:
                dist = self.coord_dist(lat, lon, station["Lat"], station["Lon"])
                if closest_dist > dist:
                    closest_id = station["ID"]
                    closest_dist = dist

        return closest_id, closest_dist

    async def get_station_info(self, station_id):
        url = "https://www.purpleair.com/data.json"

        params = {
            "show" : station_id
        }
        async with self.bot.session.get(url, params = params, headers = self.headers) as resp:
            if resp.status == 429:
                return (await resp.text())
            station_data = await resp.json()
            fields = station_data["fields"]
            data = station_data["data"]
            station = {fields[i] : data[0][i] for i in range(len(fields))}
            print(station)
            return station

    @commands.command()
    async def airmap(self, ctx):
        rand = str(random.randint(0, 32))
        await ctx.send("https://files.airnowtech.org/airnow/today/cur_aqi_sanfrancisco_ca.jpg?t=" + rand)

    @commands.command()
    async def air(self, ctx, *, address : str = "Belmont Library"):

        addresss, lat, lon = await self.geocode(address)

        station_id, distance = await self.get_closest_station_id(lat, lon)

        station = await self.get_station_info(station_id)
        if isinstance(station, str):
            await ctx.send(station)
            return

        aqi = aqi_from_pm(station["pm"])
        code = quality_codes[min(5, aqi//50)]
        embed = discord.Embed(
            title = aqi,
            colour = code[1],
            description = "Air Quality at {0}".format(station["Label"]),
            timestamp = datetime.utcnow()
        )
        embed.set_footer(text="{0:.2f} miles from {1}".format(distance, address))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Air(bot))
