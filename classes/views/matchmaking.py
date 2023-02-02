import datetime
import json
from pprint import pp
import sys
import time
import discord
import pytz
from classes.player import Player
from classes.role import Role, top, jungle, middle, bottom, support, fill

from utils.is_player_gold_plus import is_player_gold_plus

class LeftQueue(discord.ui.View):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        
    @discord.ui.button(label="Queue again", style=discord.ButtonStyle.green)
    async def queue_again_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open('C:\\DATA\\unlq.json', 'r') as file:
            unlq = json.load(file)
            if str(interaction.user.id) in unlq['players']:
                if interaction.user.id not in self.queue.get_all_ids() and str(interaction.user.id) not in unlq['in_queue'].keys():
                    if unlq['players'][str(interaction.user.id)]['banned_until'] < time.time():
                        if await is_player_gold_plus(unlq['players'][str(interaction.user.id)]['id']) or interaction.user.id in [301821822502961152, 300052305540153354, 178867201753743360]:
                        #if True:
                            if interaction.user.id not in self.queue.get_all_ids() and str(interaction.user.id) not in unlq['in_queue'].keys():
                                if len(self.queue.players) == 9 and interaction.user.id not in self.queue.get_all_ids():
                                    await interaction.response.edit_message(content="Game is about to begin...", view=None)
                                if self.queue.spots_open > 0:
                                    for p in unlq['players'].keys():
                                        if p == str(interaction.user.id):
                                            ign = unlq['players'][p]['name']
                                            rating = int(unlq['players'][p]['rating'] + (unlq['players'][p]['mmr'] / 1000*20))
                                            role = getattr(sys.modules[__name__], unlq['players'][p]['role1'].lower())
                                            player = Player(interaction.user.id, interaction.user.name, role, interaction.user, False, ign, rating)
                                            await self.queue.add_player(player)
                                            if self.queue.full != True:
                                                view = MatchmakingView(self.queue)
                                                await interaction.response.edit_message(view=view, content=f"*You can dismiss this window, you will be mentioned once a match has been found.\nIf you want to bring this window up again after closing it, enter the /queue command again.*\n**You are in queue...**\n**`{player.ign}`**\n**{role.name} {role.emoji}**")
                                else:
                                    await interaction.response.edit_message(content="Lobby is already full.", view=None)
                            else:
                                await interaction.response.edit_message(content="You are already in queue.", view=None)
                        else:
                            await interaction.response.edit_message(f"You need to be ranked Gold 4 or above in Ranked Solo/Duo to play Champions Queue.")
                    else:
                        banned_until = unlq['players'][str(interaction.user.id)]['banned_until']
                        value = datetime.datetime.fromtimestamp(banned_until, pytz.timezone('Europe/London'))
                        res = value.strftime('%d %B %I:%M %p')
                        await interaction.response.edit_message(f"You are restricted from playing Champions Queue until {res} UK time.")
                else:
                    for p in unlq['players'].keys():
                        if p == str(interaction.user.id):
                            ign = unlq['players'][p]['name']
                            rating = int(unlq['players'][p]['rating'] + (unlq['players'][p]['mmr'] / 1000*20))
                            role = getattr(sys.modules[__name__], unlq['players'][p]['role1'].lower())
                            player = Player(interaction.user.id, interaction.user.name, role, interaction.user, False, ign, rating)
                    await interaction.response.edit_message(view=MatchmakingView(self.queue), content=f"*You can dismiss this window, you will be mentioned once a match has been found.\nIf you want to bring this window up again after closing it, enter the /queue command again.*\n**You are in queue...**\n**`{player.ign}`**\n**{role.name} {role.emoji}**")
            else:
                await interaction.response.edit_message("You need to link an account first! Try using **/link**")

class MatchmakingView(discord.ui.View):
    def __init__(self, queue):
        super().__init__(timeout=None)
        self.queue = queue

    @discord.ui.button(label="Matchmaking...", style=discord.ButtonStyle.gray, emoji="<a:loadingbuffering:949327277311803522>", disabled=True)
    async def matchmaking_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(label="Leave queue", style = discord.ButtonStyle.red)
    async def leavequeue_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open('C:\\DATA\\unlq.json', 'r') as file:
            unlq = json.load(file)
        if str(interaction.user.id) in unlq['in_queue'].keys():
            del unlq['in_queue'][str(interaction.user.id)]
            with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
                json.dump(unlq, unlq_file)
        if self.queue.locked != True:
            list = self.queue.players
            for player in list:
                if interaction.user.id == player.user.id:
                    print(player.name + " left the queue")
                    self.queue.players.remove(player)
                    await self.queue.update_lobby()
                    await interaction.response.edit_message(content='You left the queue.', view=LeftQueue(self.queue))