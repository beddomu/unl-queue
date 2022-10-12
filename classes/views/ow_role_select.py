import json
from pprint import pp
import sys
import typing
import discord
from discord.ext import commands
from classes.player import Player
from classes.views.match_found import MatchFoundView
from classes.views.matchmaking import MatchmakingView
from classes.owrole import Role, dps, tank, support, fill

# Defines a custom Select containing colour options
# that the user can choose. The callback function
# of this class is called when the user changes their choice
class RoleSelect(discord.ui.Select):
    def __init__(self, owqueue):
        self.queue = owqueue
        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label='DPS', value='DPS', emoji='<:OW2dps:1029808066058797157>'),
            discord.SelectOption(label='Tank', value='Tank', emoji='<:OW2tank:1029808067673587722>'),
            discord.SelectOption(label='Support', value='Support', emoji='<:OW2support:1029808069330346124>')
        ]
        super().__init__(placeholder='Select your role...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if len(self.queue.players) == 9 and interaction.user.id not in self.queue.get_all_ids():
            await interaction.response.edit_message(content="Game is about to begin...", view=None)
        ign = None
        with open('C:\\DATA\\unlq.json', 'r') as json_file:
            unlq_json =  json.load(json_file)
        if self.queue.spots_open > 0:
            for p in unlq_json['players'].keys():
                if p == str(interaction.user.id):
                    ign = unlq_json['players'][p]['name']
                    rating = int(unlq_json['players'][p]['rating'] + (unlq_json['players'][p]['mmr'] / 1000*30))
                    role = getattr(sys.modules[__name__], self.values[0].lower())
                    player = Player(interaction.user.id, interaction.user.name, role, interaction.user, False, ign, rating)
                    await self.queue.add_player(player)
                    if self.queue.full != True:
                        view = MatchmakingView(self.queue)
                        await interaction.response.edit_message(view=view, content=f"*You can dismiss this window, you will be mentioned once a match has been found.\nIf you want to bring this window up again after closing it, enter the /queue command again.*\n**You are in queue...**\n**`{player.ign}`**\n**{role.name} {role.emoji}**")
        else:
            await interaction.response.edit_message(content="Lobby is already full", view=None)

class RoleSelectView(discord.ui.View):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.add_item(RoleSelect(queue))
        
    @discord.ui.button(label="Fill", style=discord.ButtonStyle.secondary, emoji="<:OW2:1029808843338821632>")
    async def fill_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if len(self.queue.players) == 9 and interaction.user.id not in self.queue.get_all_ids():
            await interaction.response.edit_message(content="Game is about to begin...", view=None)
            self.queue.full = True
        ign = None
        with open('C:\\DATA\\unlq.json', 'r') as json_file:
            unlq_json =  json.load(json_file)
        if self.queue.spots_open > 0:
            for p in unlq_json['players'].keys():
                if p == str(interaction.user.id):
                    ign = unlq_json['players'][p]['name']
                    rating = int(unlq_json['players'][p]['rating'] + (unlq_json['players'][p]['mmr'] / 1000*30))
                    role = fill
                    player = Player(interaction.user.id, interaction.user.name, role, interaction.user, False, ign, rating)
                    await self.queue.add_player(player)
                    if self.queue.full != True:
                        view = MatchmakingView(self.queue)
                        await interaction.response.edit_message(view=view, content=f"*You can dismiss this window, you will be mentioned once a match has been found.\nIf you want to bring this window up again after closing it, enter the /queue command again.*\n**You are in queue...**\n**`{player.ign}`**\n**{role.name} {role.emoji}**")
        else:
            await interaction.response.edit_message(content="Lobby is already full", view=None)