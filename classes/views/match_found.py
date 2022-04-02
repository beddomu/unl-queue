import json
from pprint import pp
from time import time
import discord

from utils.ban import ban


class MatchFoundView(discord.ui.View):
    def __init__(self, queue, timeout = None):
        super().__init__(timeout = 60)
        self.queue = queue

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def accept_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        #print(f'{interaction.user.name} pressed accept')
        
        await interaction.response.defer()
        if self.queue.check_player(interaction.user) and self.queue.locked == True:
            for player in self.queue.players:
                if player.user == interaction.user and player:
                    player.ready = True

            await self.queue.update_lobby()
            if self.queue.players_ready_check() and self.queue.initiated == False:
                self.stop()
                await self.queue.initiate_game()
                last_game_players = self.queue.game.get_players()
                last_queue_players = self.queue.players
                players = []
                for player in last_queue_players:
                    if player not in last_game_players:
                        players.append(player)
                await self.queue.new_lobby(players)

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.danger)
    async def decline_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.queue.check_player(interaction.user):
            await self.queue.pop_message.edit(view=None, content=f'{interaction.user.mention} declined the queue. The remaining players have been put back in queue', delete_after=5)
            self.queue.locked = False
            self.queue.full = False
            list = self.queue.players
            for player in list:
                if interaction.user.id == player.user.id:
                    print(player.name + " declined the queue")
                    ban(player.user.id, 60*3)
                    await interaction.response.send_message("You have been timed out from queueing for 3 minutes.", ephemeral=True)
                    self.queue.players.remove(player)
            self.queue.unready_all_players()
            await self.queue.update_lobby()
            self.stop()



    async def on_timeout(self):
        await self.queue.on_queue_timeout()