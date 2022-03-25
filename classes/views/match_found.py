import discord


class MatchFoundView(discord.ui.View):
    def __init__(self, queue, timeout = None):
        super().__init__(timeout = 3)
        self.queue = queue

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def accept_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        #print(f'{interaction.user.name} pressed accept')
        if self.queue.check_player(interaction.user):
            for player in self.queue.players:
                if player.user == interaction.user and player:
                    player.ready = True

            await self.queue.update_lobby()
            if self.queue.players_ready_check():
                self.stop()
                await interaction.message.delete()
                await self.queue.initiate_game()
                await self.queue.new_lobby()

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.danger)
    async def decline_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.queue.check_player(interaction.user):
            await self.queue.pop_message.edit(view=None, content=f'{interaction.user.mention} declined the queue. The remaining players have been put back in queue', delete_after=15)
            self.queue.locked = False
            self.queue.full = False
            self.queue.remove_player(interaction.user.id)
            self.queue.unready_all_players()
            await self.queue.update_lobby()
            self.stop()



    async def on_timeout(self):
        await self.queue.on_queue_timeout()