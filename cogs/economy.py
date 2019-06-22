import discord
from discord.ext import commands

import aiohttp

from utils import bitecoin
from utils.bitecoin import add_coins, add_exp

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pay(self, ctx, user : discord.Member, amount : int):
        """Pays someone a certain amount of money."""
        if amount > 0:
            await add_coins(self.bot.session, ctx, ctx.author, -1 * amount)
            await add_coins(self.bot.session, ctx, user, amount)
            await ctx.send("`" + str(amount) + "` bitecoins paid!")
        else:
            await ctx.send("haha nice try")

    @commands.command()
    async def stats(self, ctx, person : discord.Member = None):
        """Gets your or another player's stats."""
        if person == None:
            person = ctx.message.author
        await add_coins(self.bot.session, ctx, person, 0)
        level = await bitecoin.get_level(self.bot.session, person.id)
        xp = await bitecoin.get_xp(self.bot.session, person.id)
        coins = await bitecoin.get_coins(self.bot.session, person.id)
        embed = discord.Embed(
            title = "Level " + str(level),
            description = "Cumulative Exp: `" + str(xp) + "`",
            colour = person.colour
        )
        embed.set_author(name = person.display_name, icon_url = person.avatar_url)
        expToNext = bitecoin.next_exp(level) - xp
        embed.add_field(name = "Exp to next level", value = "`" + str(expToNext) + "`")
        embed.add_field(name = "bitecoins", value = "`" + str(coins) + "`")

        await ctx.send(embed=embed)

    @commands.command(aliases=["lb"])
    async def leaderboard(self, ctx):
        """Gets the leaderboard, sorted by amount of money."""
        leaderboard_list = await bitecoin.get_leaderboard(self.bot.session)
        leaderboard_string = "```Python\n"
        max_length = max([len(i["name"]) for i in leaderboard_list])
        leaderboard_string += "{0:<6}{1:<{5}}{2:<7}{3:<10}{4:<}\n".format(
            "Rank",
            "Name",
            "Level",
            "XP",
            "Bitecoins",
            max_length + 2
        )
        for i in range(len(leaderboard_list)):
            name = leaderboard_list[i]["name"]
            level = leaderboard_list[i]["level"]
            totalExp = leaderboard_list[i]["xp"]
            coins = leaderboard_list[i]["coins"]
            leaderboard_string +="{0:<6}{1:<{5}}{2:<7}{3:<10}{4:<}\n".format(
                str(i + 1),
                name,
                level,
                totalExp,
                coins,
                max_length + 2
            )
        leaderboard_string += "```"
        await ctx.send(leaderboard_string)

def setup(bot):
    bot.add_cog(Economy(bot))
