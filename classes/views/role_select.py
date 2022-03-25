import queue
import sys
import typing
import discord
from discord.ext import commands
from classes.player import Player
from classes.views.matchmaking import MatchmakingView
from classes.role import Role, top, jungle, middle, bottom, support, fill

# Defines a custom Select containing colour options
# that the user can choose. The callback function
# of this class is called when the user changes their choice
class RoleSelect(discord.ui.Select):
    def __init__(self, queue):
        self.queue = queue
        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label='Top', value='Top', emoji='<:top:949215554441465866>'),
            discord.SelectOption(label='Jungle', value='Jungle', emoji='<:jungle:949215552591765544>'),
            discord.SelectOption(label='Middle', value='Middle', emoji='<:mid:949215552621129728>'),
            discord.SelectOption(label='Bottom', value='Bottom', emoji='<:bot:949215552507883560>'),
            discord.SelectOption(label='Support', value='Support', emoji='<:support:949215552180719617>')
        ]
        super().__init__(placeholder='Select your role...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        ign = "beddomu"
        rating = 60
        if interaction.user.id not in self.queue.get_all_ids():
            role = getattr(sys.modules[__name__], self.values[0].lower())
            player = Player(interaction.user.id, interaction.user.name, role, interaction.user, False, ign, rating)
            await self.queue.add_player(player)
            view = MatchmakingView(self.queue)
            await interaction.response.edit_message(view=view, content=f"*You can dismiss this window, you will be mentioned once a match has been found.\nIf you want to bring this window up again after closing it, enter the /queue command again.*\n**You are in queue...**\n**`{player.ign}`**\n**{role.name} {role.emoji}**")
        else:
            view = MatchmakingView(self.queue)
            await interaction.response.send_message(view=view, ephemeral=True)

        


class RoleSelectView(discord.ui.View):
    def __init__(self, queue):
        super().__init__()
        self.add_item(RoleSelect(queue))
        
    @discord.ui.button(label="Fill", style=discord.ButtonStyle.secondary, emoji="<:fill:949215552671469578>")
    async def fill_button_callback(self, button: discord.ui.Button ,interaction: discord.Interaction):
        await interaction.response.send_message(view= None, content = f'You are in queue for Fill', ephemeral=True)