from discord.ext import commands

import asyncio

from utils import bitecoin
from utils.bitecoin import add_exp, add_coins

from utils.werebear.roles import Stoner, Looker, Stealer, Provocateur, Huntsman, Sleepyhead, Sloshed, Copycat
from utils.werebear.roles import Townsperson
from utils.werebear.roles import Leatherworker
from utils.werebear.roles import Werebear, Stooge

from random import shuffle

classes = {"Stoner" : Stoner, "Looker" : Looker, "Stealer" : Stealer,
           "Provocateur" : Provocateur, "Huntsman" : Huntsman, "Sleepyhead" : Sleepyhead,
           "Sloshed" : Sloshed, "Copycat" : Copycat, "Townsperson" : Townsperson,
           "Leatherworker" : Leatherworker, "Werebear" : Werebear, "Stooge" : Stooge}

class WerebearGame():
    def __init__(self, bot, ctx, game_master):
        self.bot = bot
        self.ctx = ctx
        self.roles = []
        self.game_master = game_master
        self.phase = 0
        self.players = []
        self.middle_cards = []

    def add_player(self, player):
        self.players[player] = None

    def set_roles(self, role_list):
        self.roles = role_list

    def run(self):
        if self.phase != 1:
            print("woops")
        self.phase = 2

    def lock(self):
        if self.phase != 0:
            print("woops")
        self.phase = 1

    def assign(self, role_list):
        shuffle(self.roles)
        i = 0
        for player in self.players:
            self.players[player] = self.roles[i]
            i += 1
        middle_cards = roles[i:-1]

    def scan_role(self, role):
        matches = []
        for player in self.players:
            if type(self.players[player]) = role:
                matches.append(player)
        return matches

    def swap_mid(self, player, num):
        pass

    def see_mid(self, one, two):
        pass

    def get_player_role(self, player):
        return self.players[player]

    def swap_players(self, one, two):
        self.players[one].change_person(self, person)
        self.final_players[one] = self.players[two]
        self.players[two] = 
        pass
