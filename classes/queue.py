from collections import Counter
import json
#import json
import os
from pprint import pp
import random
import time
import discord
from discord.ext import commands
import urllib
from classes.game import Game
from classes.image.image import make_image
from classes.role import Role, top, jungle, middle, bottom, support, fill
from classes.team import Team
from classes.views.live_game import LiveGame
from classes.views.match_found import MatchFoundView
from lcu.create_lobby import Lobby
from lcu.invite_player import invite_player
from lcu.leave_lobby import leave_lobby
from utils.ban import ban
from utils.tinyurl import shorten_url


class Queue:
    def __init__(self, team_size):
        self.team_size = team_size
        self.message: discord.Message = None
        self.players = []
        self.roles = [top, jungle, middle, bottom, support]
        self.full = bool
        self.locked = False
        self.initiated = False
        self.pop_message: discord.Message = None
        self.spots_open = 10
        with open('C:\\DATA\\unlq.json', 'r') as file:
            unlq = json.load(file)
        self.devmode = unlq['dev_mode']

    async def reset_lobby(self):
        channel = await self.message.guild.fetch_channel(os.getenv("QUEUE"))
        await channel.purge(limit=100)
        message = await channel.send("**Initializing...**")
        print(f"New League Of Legends lobby has been created with the id: {message.id}")
        self.locked = False
        self.full = False
        self.game = None
        self.initiated = False
        self.pop_message = None
        self.message = message
        channel = await self.message.guild.fetch_channel(int(os.getenv("CHAT")))
        if self.devmode == False:
            await channel.send(f"{' '.join(self.get_player_mentions())}\nThe lobby was reset. Queue up again here: https://discord.com/channels/603515060119404584/953616729911726100")
        self.players.clear()
        self.spots_open = 10
        await self.update_lobby()

    async def new_lobby(self, players=None):
        channel = await self.message.guild.fetch_channel(os.getenv("QUEUE"))
        await channel.purge(limit=100)
        message = await channel.send("**Initializing...**")
        print(f"New League Of Legends lobby has been created with the id: {message.id}")
        self.locked = False
        self.full = False
        self.game = None
        self.initiated = False
        self.message = message
        self.players.clear()
        if players:
            self.players = players
        self.unready_all_players()
        channel = await self.message.guild.fetch_channel(int(os.getenv("CHAT")))
        if self.devmode == False:
            await channel.send("League Of Legends queue is live! Queue up here: https://discord.com/channels/603515060119404584/953616729911726100")
        await self.update_lobby()

    async def add_player(self, player):
        self.players.append(player)
        print(f"{player} is now in queue as: {player.role}")
        await self.update_lobby()
        if self.full == True and self.locked != True:
            view = MatchFoundView(self)
            await self.pop(view)

    def list_players(self):
        for player in self.players:
            print(f'{player}: {player.role}')

    def get_all_ids(self):
        list = []
        for player in self.players:
            list.append(player.id)
        return list

    async def update_lobby(self):
        self.ready_check()
        initial_string = f"**League Of Legends**\n`Players needed for full lobby:` *{self.spots_open}*\n---------------------------------------------"
        player_string_list = []

        top_list = []
        jungle_list = []
        mid_list = []
        bot_list = []
        supp_list = []
        fill_list = []

        for player in self.players:
            if player.role == top:
                top_list.append(player)
            elif player.role == jungle:
                jungle_list.append(player)
            elif player.role == middle:
                mid_list.append(player)
            elif player.role == bottom:
                bot_list.append(player)
            elif player.role == support:
                supp_list.append(player)
            else:
                fill_list.append(player)

        for player in self.players:
            if player.ready == True:
                string = f"✅ `{player.name}`"
            else:
                string = f"       `{player.name}`"
            player_string_list.append(string)
        if player_string_list:
            player_string = "\n" + "\n".join(player_string_list)
        else:
            player_string = "       `none`"

        role_list = f"\nTop        <:top:985153368563539988>: {len(top_list)}/2\nJungle   <:jungle:985153365212295249>: {len(jungle_list)}/2\nMiddle   <:mid:985153366801915924> : {len(mid_list)}/2\nBottom  <:bot:985153363274522694>: {len(bot_list)}/2\nSupport <:support:985153369779896391>: {len(supp_list)}/2\nFill           <:fill:985153779148140584>: {len(fill_list)}"

        divider = "\n---------------------------------------------"
        lobby_id_string = f"\n`Lobby id: {int(str(self.message.id)[:-8])}`"
        end_string = initial_string +  role_list + divider + lobby_id_string
        await self.message.edit(content=end_string)
        
    async def update_queue_pop(self):
        player_string_list = []
        for player in self.game_players:
            if player.ready == True:
                string = f"✅ `{player.name}`"
            else:
                string = f"       `{player.name}`"
            player_string_list.append(string)
        if player_string_list:
            player_string = "\n" + "\n".join(player_string_list)
            await self.pop_message.edit(content=" ".join(self.player_mentions) + "\n**MATCH FOUND**\n*You have 60 seconds to accept.*" + player_string)

        

    def ready_check(self):
        role_list = []
        fill_list = []
        if self.full != True:
            index = 0
            i = 0
            for player in self.players:
                if player.role != fill:
                    role_list.append(player.role.name)
                    roles_in_queue = Counter(role_list)
                else:
                    fill_list.append(player)
            if role_list:
                for r in roles_in_queue.values():
                    if r >= 2:
                        index += 1
                        i += 2
                    elif r == 1:
                        i += 1
            self.spots_open = 10 - i - len(fill_list)
            if self.spots_open == 0:
                self.full = True

    async def pop(self, queue):
        self.locked = True
        game = self.make_teams()
        self.game = game
        self.player_mentions = game.get_player_mentions()
        random.shuffle(self.player_mentions)
        view = MatchFoundView(self)
        channel = await self.message.guild.fetch_channel(os.getenv("QUEUE"))
        player_string_list = []
        self.game_players = self.game.players
        random.shuffle(self.game_players)
        for player in self.game_players:
            print(player.name)
            if player.ready == True:
                string = f"✅ `{player.name}`"
            else:
                string = f"       `{player.name}`"
            player_string_list.append(string)
        if player_string_list:
            player_string = "\n" + "\n".join(player_string_list)
            self.pop_message = await channel.send(" ".join(self.player_mentions) + "\n**MATCH FOUND**\n*You have 60 seconds to accept.*" + player_string, view=view)
        else:
            print("NOPE")
            
    def make_teams(self):
        with open('C:\\DATA\\unlq.json', 'r') as file:
            unlq = json.load(file)
        team_blue = Team(5, "Blue")
        team_red = Team(5, "Red")
        game = Game(team_blue, team_red, None)
        self.top_list = []
        self.jungle_list = []
        self.mid_list = []
        self.bot_list = []
        self.supp_list = []
        self.fill_list = []
        role_lists = [
            self.top_list,
            self.jungle_list,
            self.mid_list,
            self.bot_list,
            self.supp_list
        ]

        for player in self.players:
            if player.role == top:
                self.top_list.append(player)
            elif player.role == jungle:
                self.jungle_list.append(player)
            elif player.role == middle:
                self.mid_list.append(player)
            elif player.role == bottom:
                self.bot_list.append(player)
            elif player.role == support:
                self.supp_list.append(player)
            else:
                self.fill_list.append(player)
        for role in role_lists:
            while len(role) < 2 and len(self.fill_list) >= 0:
                role.append(self.fill_list.pop(
                    random.randint(0, (len(self.fill_list)-1))))

        print("balancing teams...")

        topq = [self.top_list[0], self.top_list[1]]
        team_blue.add_player(topq.pop(random.randint(0, 1)))
        team_red.add_player(topq[0])

        jgq = [self.jungle_list[0], self.jungle_list[1]]
        better_player = jgq.index(max(jgq))
        options = [jgq.pop(better_player), jgq[0]]
        if game.blue_team > game.red_team:
            game.red_team.add_player(options[0])
            game.blue_team.add_player(options[1])
        elif game.red_team > game.blue_team:
            game.red_team.add_player(options[1])
            game.blue_team.add_player(options[0])
        else:
            game.blue_team.add_player(self.jungle_list[0])
            game.red_team.add_player(self.jungle_list[1])

        midq = [self.mid_list[0], self.mid_list[1]]
        better_player = midq.index(max(midq))
        options = [midq.pop(better_player), midq[0]]
        if game.blue_team > game.red_team:
            game.red_team.add_player(options[0])
            game.blue_team.add_player(options[1])
        elif game.red_team > game.blue_team:
            game.red_team.add_player(options[1])
            game.blue_team.add_player(options[0])
        else:
            game.blue_team.add_player(self.mid_list[0])
            game.red_team.add_player(self.mid_list[1])

        adcq = [self.bot_list[0], self.bot_list[1]]
        better_player = adcq.index(max(adcq))
        options = [adcq.pop(better_player), adcq[0]]
        if game.blue_team > game.red_team:
            game.red_team.add_player(options[0])
            game.blue_team.add_player(options[1])
        elif game.red_team > game.blue_team:
            game.red_team.add_player(options[1])
            game.blue_team.add_player(options[0])
        else:
            game.blue_team.add_player(self.bot_list[0])
            game.red_team.add_player(self.bot_list[1])

        suppq = [self.supp_list[0], self.supp_list[1]]
        better_player = suppq.index(max(suppq))
        options = [suppq.pop(better_player), suppq[0]]
        if game.blue_team > game.red_team:
            game.red_team.add_player(options[0])
            game.blue_team.add_player(options[1])
        elif game.red_team > game.blue_team:
            game.red_team.add_player(options[1])
            game.blue_team.add_player(options[0])
        else:
            game.blue_team.add_player(self.supp_list[0])
            game.red_team.add_player(self.supp_list[1])

        print(f"Final Team blue rating: {team_blue.rating}")
        print(f"Final Team red rating: {team_red.rating}")

        game.players = game.blue_team.players + game.red_team.players
        
        self.game = game
        make_image(game)
        return game

    async def on_queue_timeout(self):
        ready_list = []
        not_ready_list = []
        self.locked = False
        for p in self.game.players:
            if p.ready != True:
                not_ready_list.append(p)
            elif p.ready == True:
                ready_list.append(p)
        if self.locked != True:
            self.full = False
            self.game = None
            self.players.clear()
        for player in ready_list:
            self.players.append(player)
        not_ready_mentions = []
        for player in not_ready_list:
            not_ready_mentions.append(player.user.mention)
            ban(player.user.id, 60*30)
        if len(ready_list) > 0:
            await self.pop_message.edit(view=None, content="{} missed ready check. All the remaining players have been put back in queue".format(", ".join(not_ready_mentions)), delete_after=10)
        else:
            await self.pop_message.edit(view=None, content="Queue expired", delete_after=10)
        
        self.game = None
        self.unready_all_players()
        await self.update_lobby()
        self.full = False

    def unready_all_players(self):
        for player in self.players:
            player.ready = False

    def check_player(self, user):
        for player in self.players:
            if player.user == user:
                if player.ready != True:
                    return True

    def players_ready_check(self):
        for player in self.players:
            if player.ready != True:
                return False
        return True

    async def initiate_game(self):
        self.initiated = True
        lobby = Lobby(name=int(str(self.message.id)[:-8]), team_size=5, mutator_id=6)
        lobby.create()
        time.sleep(1)
        embed = discord.Embed(color=discord.colour.Colour.brand_red())
        user = await self.message.guild.fetch_member(948863727032217641)
        embed.set_author(name="UNL Queue", icon_url=user.avatar.url)
        embed.set_footer(text=f'Lobby ID: {int(str(self.message.id)[:-8])}')
        file = discord.File('classes\\image\\res.png', filename='res.png')
        embed.set_image(url=('attachment://res.png'))
        players = []
        guild = self.message.guild
        role = discord.utils.get(guild.roles, id=676740137815900160)
        member = guild.get_member(301821822502961152)
        permissions = {
            role: discord.PermissionOverwrite(view_channel=True),
            member: discord.PermissionOverwrite(view_channel=True)
        }
        unlq_category = discord.utils.get(
            guild.categories, id=953292613115605012)
        category = await guild.create_category(name=f"{int(str(self.message.id)[:-8])}", position=(unlq_category.position - 1), overwrites=permissions)
        await guild.create_voice_channel("Team Blue🔵", category=category, overwrites=permissions)
        await guild.create_voice_channel("Team Red 🔴", category=category, overwrites=permissions)
        for team in self.game.teams:
            team_players_list = []
            ign_list = []
            for player in team.players:
                member = guild.get_member(player.id)
                if team.side == "Blue":
                    voice = discord.utils.get(
                        category.voice_channels, name="Team Blue🔵")
                else:
                    voice = discord.utils.get(
                        category.voice_channels, name="Team Red 🔴")
                try:
                    await member.move_to(voice)
                except:
                    print(f'{player.name} is not in a voice channel.')
                invite_player(player.ign)
                ign_list.append(player.ign.replace(" ", ""))
                players.append(player)
                team_players_list.append(
                    player.role.emoji + player.user.mention)
            multiopgg = "https://www.op.gg/multisearch/euw?summoners={}".format(
                ",".join(ign_list))
            team_players_string = "\n".join(team_players_list)
            embed.add_field(name=f'Team {team.side} ({team.rating})', value=team_players_string)
        leave_lobby()
        
        channel = await self.message.guild.fetch_channel(os.getenv("LIVE"))
        view = LiveGame(str(self.message.id)[:-8])
        live_game_messsage = await channel.send(view=view, embed=embed, file=file)
        with open('C:\\DATA\\unlq.json', 'r') as unlq_file:
            unlq_json = json.load(unlq_file)
        unlq_json['lobbies'][int(str(self.message.id)[:-8])] = {}
        unlq_json['lobbies'][int(str(self.message.id)[:-8])
                             ]['game_id'] = live_game_messsage.id
        unlq_json['lobbies'][int(str(self.message.id)[:-8])
                             ]['blue_team'] = self.game.blue_team.rating
        unlq_json['lobbies'][int(str(self.message.id)[:-8])
                             ]['red_team'] = self.game.red_team.rating
        unlq_json['lobbies'][int(str(self.message.id)[:-8])]['players'] = {}
        unlq_json['lobbies'][int(str(self.message.id)[:-8])]['player_ids'] = {}
        unlq_json['lobbies'][int(str(self.message.id)[:-8])
                             ]['time_created'] = int(time.time())
        unlq_json['lobbies'][int(str(self.message.id)[:-8])]['players']['Blue'] = []
        unlq_json['lobbies'][int(str(self.message.id)[:-8])]['players']['Red'] = []
        unlq_json['lobbies'][int(str(self.message.id)[:-8])]['player_ids']['Blue'] = []
        unlq_json['lobbies'][int(str(self.message.id)[:-8])]['player_ids']['Red'] = []
        for team in self.game.teams:
            for player in team.players:
                unlq_json['lobbies'][int(str(self.message.id)[:-8])]['players'][team.side].append(player.ign)
                unlq_json['lobbies'][int(str(self.message.id)[:-8])]['player_ids'][team.side].append(player.user.id)

        await self.pop_message.delete()
        await self.new_lobby()
        
        with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
            json.dump(unlq_json, unlq_file)
            unlq_file.close()
        self.locked = False
        
    def get_player_mentions(self):
        list = []
        for p in self.players:
            list.append(p.user.mention)
        return list
