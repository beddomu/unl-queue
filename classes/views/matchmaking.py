import discord
class MatchmakingView(discord.ui.View):
    def __init__(self, queue):
        super().__init__(timeout=None)
        self.queue = queue

    @discord.ui.button(label="Matchmaking...", style=discord.ButtonStyle.gray, emoji="<a:loadingbuffering:949327277311803522>", disabled=True)
    async def matchmaking_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(label="Leave queue", style = discord.ButtonStyle.red)
    async def leavequeue_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.queue.locked == True:
            await interaction.response.edit_message(content="*You can't leave queue when a match has been found.\nYou can choose to decline the queue, or to wait for everyone to accept*")
        
        else:
            #view = RoleSelectView()
            await interaction.response.edit_message(content='You left the queue.', view=None)
            await self.queue.remove_player_by_id(interaction.user.id)
        await self.queue.update_lobby()