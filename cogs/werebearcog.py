import discord
from discord.ext import commands
from discord.ext.commands.core import check

import asyncio

from utils import bitecoin
from utils.bitecoin import add_exp, add_coins

from utils import werebear
from utils.werebear.werebeargame import WerebearGame
from utils.werebear.roles import Stoner, Looker, Stealer, Provocateur, Huntsman, Sleepyhead, Sloshed, Copycat
from utils.werebear.roles import Townsperson
from utils.werebear.roles import Leatherworker
from utils.werebear.roles import Werebear, Stooge

roles = [Stoner, Looker, Stealer, Provocateur, Huntsman, Sleepyhead, Sloshed, Copycat, Townsperson, Leatherworker, Werebear, Stooge]

"""This cog is in development."""

class WerebearCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    @commands.command()
    async def werebear(self, ctx, cosmetics="default"):
        """Starts a Werebear game."""
        game_id = ctx.channel.id
        if game_id in self.games:
            await ctx.send("there's already a game running!")
            return
        game_master = ctx.author

        self.games[game_id] = WerebearGame(self.bot, ctx, game_master)

        starting_embed = discord.Embed(
            color = 0x000000,
            title = "Werebear",
            description = (f"{game_master.mention} is the game master. "
                            "If you want to join, type `?join` to play. "
                            "When everyone is in the game, type `?lock` to lock the game.")
        )

        await ctx.send(embed=starting_embed)
        self.games[game_id].add_player(game_master)

    @commands.command()
    async def join(self, ctx):
        """Joins a user to the Werebear game."""
        game_id = ctx.channel.id
        if not game_id in self.games:
            await ctx.send("no game running!")
            return
        if self.games[game_id].phase != 0:
            await ctx.send("you can't join the game right now!")
            return
        if ctx.author.id in [player.id for player in self.games[game_id].players]:
            await ctx.send("you're already in the game!")
        else:
            self.games[game_id].add_player(ctx.author)
            await ctx.send("added!")

    @commands.command()
    async def lock(self, ctx):
        """Locks the users into the game and starts the selection for cards."""
        game_id = ctx.channel.id
        if not game_id in self.games:
            await ctx.send("no game running!")
            return
        if self.games[game_id].game_master.id != ctx.author.id:
            await ctx.send("you are not the game master!")
            return
        self.games[game_id].lock()
        num_players = len(self.games[game_id].players)
        num_cards = num_players + 3
        await ctx.send("The game is now locked. "
                       f"There are {num_players} players. "
                       f"You need {num_cards} cards to play. "
                       "The available roles are:\n`"
                       "Werebear, Stooge"
                       "Leatherworker, "
                       "Stoner, Looker, Stealer, Provocateur, Huntsman, Sleepyhead, Sloshed, Copycat, "
                       "Townsperson`"
                       "Please select the cards that you want in the game by using `?deck`. "
                       "For example:\n"
                       "`?deck 2 werebears, stooge, stoners, looker, stealer, leatherworker, sleepyhead`")

    @commands.command()
    async def start(self, ctx):
        """Starts the game."""
        game_id = ctx.channel.id
        if not game_id in self.games:
            await ctx.send("no game running!")
            return
        if self.games[game_id].game_master.id != ctx.author.id:
            await ctx.send("you are not the game master!")
            return
        if self.games[game_id].phase != 0:
            await ctx.send("the game has already started!")
            return
        await self.games[game_id].run()

    @commands.command()
    async def killGame(self, ctx):
        """Kills a game in the channel."""
        game_id = ctx.channel.id
        if not game_id in self.games:
            await ctx.send("no game running!")
            return
        if self.games[game_id].game_master.id != ctx.author.id:
            await ctx.send("you are not the game master!")
            return
        del self.games[game_id]
        await ctx.send("deleted!")

    @commands.command()
    async def deck(self, ctx, *, chosen_roles : str):
        """Select a deck for the game."""
        game_id = ctx.channel.id
        if not game_id in self.games:
            await ctx.send("no game running!")
            return
        if self.games[game_id].game_master.id != ctx.author.id:
            await ctx.send("you are not the game master!")
            return
        if self.games[game_id].phase != 1:
            await ctx.send("can't choose deck right now!")
            return
        game_roles = [role for role in roles if role.__name__ in chosen_roles.lower()]
        self.games[game_id].set_roles(game_roles)
        await ctx.send("roles chosen: " + ", ".join([role.__name__ for role in game_roles]))

def setup(bot):
    bot.add_cog(WerebearCog(bot))
