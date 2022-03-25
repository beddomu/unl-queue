from collections import Counter
#import json
import os
from pprint import pp
import random
from time import sleep
import discord
from discord.ext import commands
from classes.game import Game
from classes.image.image import make_image
from classes.role import Role, top, jungle, middle, bottom, support, fill
from classes.team import Team
from classes.views.match_found import MatchFoundView
#from lcu.create_lobby import Lobby
#from lcu.invite_player import invite_player
#from lcu.leave_lobby import leave_lobby
from utils.tinyurl import shorten_url


class Queue:
    def __init__(self, team_size):
        self.team_size = team_size
        self.message = None
        self.players = []
        self.roles = [top, jungle, middle, bottom, support]
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

    def ready_check(self):
        role_list = []
        fill_list = []
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
        #player_mentions = game.get_player_mentions()
        view = MatchFoundView(queue)
        #" ".join(player_mentions) + 
        channel = await self.message.guild.fetch_channel(os.getenv("QUEUE"))
        self.pop_message = await channel.send("\n**MATCH FOUND**\n*You have 60 seconds to accept.*", view=view)

    def make_teams(self):
        #with open('C:\\DATA\\unlq.json', 'r') as file:
        #    unlq = json.load(file)
        team_blue = Team(5, "Blue")
        team_red = Team(5, "Red")
        game = Game(team_blue, team_red, None)

        role_list = []
        fill_list = []
        for player in self.players:
            if player.role != fill:
                role_list.append(player.role.name)
                roles_in_queue = Counter(role_list)
            else:
                fill_list.append(player)

        for role in roles_in_queue.values():
            while role < 2 and len(fill_list) >= 0:
                role_list.players.append(fill_list.pop(
                    random.randint(0, (len(fill_list)-1))))
                
        print("balancing teams")
                
        topq = []
        for p in self.players:
            if p.role.name == "Top":
                topq.append(p)
        team_blue.add_player(topq.pop(random.randint(0, 1)))
        team_red.add_player(topq[0])
        
        jgq = []
        for p in self.players:
            if p.role.name == "Jungle":
                jgq.append(p)
        if game.blue_team > game.red_team:
            game.red_team.add_player(max(jgq))
            game.blue_team.add_player(min(jgq))
        else:
            game.red_team.add_player(min(jgq))
            game.blue_team.add_player(max(jgq))
            
        midq = []
        for p in self.players:
            if p.role.name == "Middle":
                midq.append(p)
        if game.blue_team > game.red_team:
            game.red_team.add_player(max(midq))
            game.blue_team.add_player(min(midq))
        else:
            game.red_team.add_player(min(midq))
            game.blue_team.add_player(max(midq))
        
        adcq = []
        for p in self.players:
            if p.role.name == "Bottom":
                adcq.append(p)
        if game.blue_team > game.red_team:
            game.red_team.add_player(max(adcq))
            game.blue_team.add_player(min(adcq))
        else:
            game.red_team.add_player(min(adcq))
            game.blue_team.add_player(max(adcq))

        suppq = []
        for p in self.players:
            if p.role.name == "Support":
                suppq.append(p)
        if game.blue_team > game.red_team:
            game.red_team.add_player(max(suppq))
            game.blue_team.add_player(min(suppq))
        else:
            game.red_team.add_player(min(suppq))
            game.blue_team.add_player(max(suppq))
        
        print(f"Final Team blue rating: {team_blue.rating}")
        print(f"Final Team red rating: {team_red.rating}")
        
        self.game = game
        make_image(game)
        return game


    async def on_queue_timeout(self):
        self.locked = False
        self.game = None
        ready_list = []
        not_ready_list = []
        for p in self.players:
            if p.ready != True:
                not_ready_list.append(p)
            elif p.ready == True:
                ready_list.append(p)
        if self.locked != True:
            self.full = False
            self.game = None
            self.players.clear()
        for player in ready_list:
            await self.add_player(player)
        not_ready_mentions = []
        for player in not_ready_list:
            not_ready_mentions.append(player.user.mention)
        try:
            if len(ready_list) > 0:
                await self.pop_message.edit(view=None, content="{} missed ready check. All the remaining players have been put back in queue".format(", ".join(not_ready_mentions)), delete_after=10)
            else:
                await self.pop_message.edit(view=None, content="Queue expired", delete_after=10)
        except:
            print("error")
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
        #lobby = Lobby(name=int(str(self.message.id)[:-8]), team_size=5)
        #lobby.create()
        sleep(1)
        embed = discord.Embed(color=discord.colour.Colour.brand_red())
        user = await self.message.guild.fetch_member(948863727032217641)
        embed.set_author(name="UNL Queue", icon_url=user.avatar.url)
        embed.set_footer(text=f'Lobby id: {int(str(self.message.id)[:-8])}')
        file = discord.File('classes\\image\\res.png', filename='res.png')
        embed.set_image(url=('attachment://res.png'))
        #embed.set_image(url="https://static.wikia.nocookie.net/leagueoflegends/images/5/53/Summoner%27s_Rift_Update_Map.png/revision/latest/scale-to-width-down/1000?cb=20170223053555.png")

        players = []
        for team in self.game.teams:
            team_players_list = []
            ign_list = []
            for player in team.players:
                if player.ign:
                    #invite_player(player.ign)
                    ign_list.append(player.ign.replace(" ", ""))
                players.append(player)
                team_players_list.append(
                    player.role.emoji + player.user.mention)
            multiopgg = "https://www.op.gg/multisearch/euw?summoners={}".format(
                ",".join(ign_list))
            short_multiopgg = "\nMulti opgg: {}".format(shorten_url(multiopgg))
            team_players_string = "\n".join(
                team_players_list) + short_multiopgg
            embed.add_field(name=f'Team {team.side}',
                            value=team_players_string)
        #leave_lobby()
        channel = await self.message.guild.fetch_channel(os.getenv("LIVE"))
        live_game_messsage = await channel.send(embed=embed, file=file)
        #with open('C:\\DATA\\unlq.json', 'r') as unlq_file:
            #unlq_json =  json.load(unlq_file)
        #unlq_json['lobbies'][int(str(self.message.id)[:-8])] = {}
        #unlq_json['lobbies'][int(str(self.message.id)[:-8])]['game_id'] = live_game_messsage.id
        #unlq_json['lobbies'][int(str(self.message.id)[:-8])]['blue_team'] = self.game.blue_team.rating
        #unlq_json['lobbies'][int(str(self.message.id)[:-8])]['red_team'] = self.game.red_team.rating
        #with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
            #json.dump(unlq_json, unlq_file)
            #unlq_file.close()
        #for p in players:
            #await p.user.send(embed=embed)
        self.locked = False