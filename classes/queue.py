from collections import Counter
import os
from pprint import pp
import discord
from discord.ext import commands
from classes.role import Role, top, jungle, middle, bottom, support, fill


class Queue:
    def __init__(self, team_size):
        self.team_size = team_size
        self.message = None
        self.players = []
        self.roles = [top, jungle, middle, bottom, support, fill]
        self.full = bool
        self.locked = False
        self.pop_message = None
        self.spots_open = 10

    async def new_lobby(self):
        channel = await self.message.guild.fetch_channel(os.getenv("QUEUE"))
        await channel.purge(limit=100)
        message = await channel.send("**Initializing...**")
        print(f"New lobby has been created with the id: {message.id}")
        if self.locked != True:
            self.full = False
            self.game = None
            self.message = message
            self.players.clear()
            await self.update_lobby()

    async def add_player(self, player):
        self.players.append(player)
        await self.update_lobby()

    async def remove_player_by_id(self, id):
        for player in self.players:
            if player.id == id:
                self.players.remove(player)
                await self.update_lobby()

    def ready_check(self):
        role_list = []
        index = 0
        i = 0
        for player in self.players:
            role_list.append(player.role.name)
            roles_in_queue = Counter(role_list)
        if role_list:
            for r in roles_in_queue.values():
                if r >= 2:
                    index += 1
                    i += 2
                elif r == 1:
                    i += 1
        self.spots_open = 10 - i
        if self.spots_open == 0:
            self.full = True
        

    def list_players(self):
        for player in self.players:
            print(f'{player.name}: {player.role}')

    def get_all_ids(self):
        list = []
        for player in self.players:
            list.append(player.id)
        return list

    async def update_lobby(self):
        self.ready_check()
        initial_string = f"**Players in queue:**\n`Players needed for full lobby:` *{self.spots_open}*\n---------------------------------------------\n"
        player_string_list = []
        for player in self.players:
            spaces = " -" * (20 - len(player.name))
            if player.ready == True:
                string = f"✅ `{player.name}`{spaces}{player.role.name} {player.role.emoji}"
            else:
                string = f"       `{player.name}`{spaces}{player.role.name} {player.role.emoji}"
            player_string_list.append(string)
        if player_string_list:
            player_string = "\n".join(player_string_list)
        else:
            player_string = "       `none`"
        divider = "\n---------------------------------------------"
        lobby_id_string = f"\n`Lobby id: {int(str(self.message.id)[:-8])}`"
        end_string = initial_string + player_string + divider + lobby_id_string
        await self.message.edit(content=end_string)

    async def pop(self):
        self.locked = True
        channel = await self.message.guild.fetch_channel(os.getenv("QUEUE"))
        await channel.send('Queue popped')
