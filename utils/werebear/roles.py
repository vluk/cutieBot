import asyncio
import discord

class Player():
    def __init__(self, ctx, game, user):
        self.ctx = ctx
        self.user = user 
        self.game = game
        self.descrption = ""
        self.initial_role = None
        self.final_role = None

    async def inform_role(self):
        embed = discord.Embed(
            title = f"You are the {self.initial_role.__name__}!",
            description = description
        )
        await self.user.send(embed = embed)

    async def do_action(self):
        await initial_role.role_action(self)

class Stoner():
    description = (
        "You are on the Villager team, so you win if one of the werebears get killed."
    )
    team = 0
    async def role_action(player):
        stoners = player.game.get_stoners()
        embed = None
        if len(stoners) == 1:
            embed = discord.Embed(
                title = "You open your eyes.",
                descrption = "There are no other Stoners."
            )
        else:
            stoners_string = ", ".join([stoner.display_name for stoner in stoners])
            embed = discord.Embed(
                title = "You open your eyes.",
                description = f"The Stoners are *{stoners_string}*."
            )
        await player.user.send(embed=embed)


class Looker():
    description = (
        "You are on the Villager team, so you win if one of the werebears get killed."
    )
    team = 0
    async def role_action(player):
        embed = discord.Embed(
            title = "You open your eyes.",
            descrption = (
                "You can choose to look at another player's card or two cards from the center."
                "Choose by saying either `player` or `center`."
        )

        await player.user.send(embed=embed)

        def check(m):
            return (m.author.id == player.user.id
                    and type(m) == discord.DMChannel
                    and m.content in ["player", "center"])

        choice = await bot.wait_for("message", check=check)
        if choice == "player":
            await player.user.send("choose a player")
            def player_check(m):
                return (m.author.id == player.user.id
                        and type(m) == discord.DMChannel
                        and m.content in [game_player.user.display_name for game_player in player.game.players])
            choice = await bot.wait_for("message", check=check)
        else:
            await player.user.send("choose which card from the center you dont wanna see")
            def player_check(m):
                return (m.author.id == player.user.id
                        and type(m) == discord.DMChannel
                        and m.content in ["1", "2", "3"])
            choice = await bot.wait_for("message", check=check)
                
        


class Stealer(Role):
    async def do_role(self):
        await self.inform_role()
        pass
    async def do_action():
        pass

class Provocateur(Role):
    async def do_role(self):
        await self.inform_role()
        pass
    async def do_action():
        pass

class Huntsman(Role):
    async def do_role(self):
        await self.inform_role()
        pass

class Sleepyhead(Role):
    async def do_role():
        await inform_role()
        pass
    async def do_action():
        
        pass

class Sloshed(Role):
    async def do_role():
        await inform_role()
        pass
    async def do_action():
        pass

class Copycat(Role):
    async def do_role():
        await inform_role()
        pass
    async def do_action():
        pass

class Townsperson(Role):
    async def do_role():
        await inform_role()
        pass

class Leatherworker(Role):
    async def do_role():
        await inform_role()
        pass

class Werebear(Role):
    async def do_role():
        await inform_role()
        pass

class Stooge(Role):
    async def do_role():
        await inform_role()
        pass
