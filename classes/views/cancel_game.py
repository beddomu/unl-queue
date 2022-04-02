import json
import discord

class Cancel(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

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
            await interaction.message.delete()
            self.value = False
            self.stop()
        else:
            await interaction.response.send_message("You're not allowed to do that.", ephemeral = True)