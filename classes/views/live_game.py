import json
from pprint import pp
import time
import discord

from classes.views.betting import Betting

class LiveGame(discord.ui.View):
    def __init__(self, lobby_id):
        super().__init__(timeout=None)
        self.value = None
        self.lobby_id = lobby_id

    @discord.ui.button(label='Bugged lobby?', emoji="🧑‍🔧", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id in [301821822502961152, 194932912729227264]:
            with open('C:\\DATA\\unlq.json', 'r') as file:
                unlq = json.load(file)
            the_lobby = None
            for lobby in unlq['lobbies']:
                if unlq['lobbies'][lobby]['game_id'] == interaction.message.id:
                    the_lobby = lobby
                    break
            del unlq['lobbies'][the_lobby]
            with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
                json.dump(unlq, unlq_file)
            guild = interaction.guild
            game_category = discord.utils.get(guild.categories, name=str(self.lobby_id))
            for channel in game_category.voice_channels:
                await channel.delete()
            await game_category.delete()
            await interaction.message.delete()
            self.value = False
            self.stop()
        else:
            await interaction.response.send_message("You're not allowed to do that.", ephemeral = True)
            
    @discord.ui.button(label='Bet on this game', emoji="<:xqcM:828492833462943755>", style=discord.ButtonStyle.blurple)
    async def bet(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open('C:\\DATA\\unlq.json', 'r') as file:
            unlq = json.load(file)
            


        the_lobby = None
        for lobby in unlq['lobbies']:
            if unlq['lobbies'][lobby]['game_id'] == interaction.message.id:
                the_lobby = lobby
                break
        
        if unlq['lobbies'][the_lobby]['time_created'] > time.time() - 60*5:
            if interaction.user.id in unlq['lobbies'][the_lobby]['player_ids']:
                await interaction.response.send_message("You can't bet on a game you are in!", ephemeral=True)
            else:
                if str(the_lobby) not in unlq['players'][str(interaction.user.id)]['bets'].keys():     
                    view = Betting(the_lobby, interaction.user.id)
                    await interaction.response.send_message(view=view, ephemeral=True)
                    #await interaction.response.send_message("Coming soon...", ephemeral=True)
                else:
                    await interaction.response.send_message("You've already placed a bet for this game.", ephemeral=True)
        else:
            await interaction.response.send_message("The betting window for this game has expired.", ephemeral=True)

        with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
            json.dump(unlq, unlq_file)