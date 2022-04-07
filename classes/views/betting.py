import os
from pprint import pp
import time
import discord
import json

            

class BetModal(discord.ui.Modal):
    def __init__(self, lobby_id, user_id, team: str, title="Bet amount", timeout=5 * 60, custom_id="betamount"):
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        with open('C:\\DATA\\unlq.json', 'r') as json_file:
            self.unlq = json.load(json_file)
            self.lobby_id = lobby_id
            self.user_id = user_id
            self.team = team

        self.bet = discord.ui.TextInput(
            label=f"{team.capitalize()} team",
            placeholder= f"Your UN Points: {self.unlq['players'][str(user_id)]['unp']}",
            min_length=2,
            max_length=3
        )
        self.add_item(self.bet)
        
    async def on_submit(self, interaction: discord.Interaction):
        if self.bet.value.isnumeric():
            if self.unlq['lobbies'][self.lobby_id]['time_created'] > time.time() - 60*5:
                if self.unlq['players'][str(self.user_id)]['unp'] > int(self.bet.value):
                    your_bet = int(self.bet.value)
                else:
                    your_bet = self.unlq['players'][str(self.user_id)]['unp']
                if str(self.lobby_id) not in self.unlq['players'][str(self.user_id)]['bets'].keys():
                    self.unlq['players'][str(self.user_id)]['bets'][str(self.lobby_id)] = {}
                    self.unlq['players'][str(self.user_id)]['bets'][str(self.lobby_id)][self.team] = your_bet
                    self.unlq['players'][str(self.user_id)]['unp'] -= your_bet
                    print(f"{interaction.user.name} bet {your_bet} UN Points on team {self.team}")
                    await interaction.response.send_message(f"You bet {your_bet} UN Points on the {self.team.capitalize()} team in lobby ID: {self.lobby_id}", ephemeral=True)
                else:
                    await interaction.response.send_message("You've already placed a bet for this game.", ephemeral=True)
            else:
                await interaction.response.send_message("The betting window for this game has expired.", ephemeral=True)
        else:
            await interaction.response.send_message("Your bet needs to be a number!", ephemeral=True)
            
        with open('C:\\DATA\\unlq.json', 'w') as json_file:
            json.dump(self.unlq, json_file, ensure_ascii=False)
                    
    async def on_error(self, error: Exception, interaction: discord.Interaction) -> None:
        pp(error)
        await interaction.response.send_message('Something went wrong.', ephemeral=True)


class Betting(discord.ui.View):
    def __init__(self, lobby_id, user_id):
        super().__init__()
        with open('C:\\DATA\\unlq.json', 'r') as json_file:
            self.unlq = json.load(json_file)
        self.lobby_id = lobby_id
        self.user_id = user_id

    @discord.ui.button(label='Blue team', style=discord.ButtonStyle.primary)
    async def bet_on_blue(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open('C:\\DATA\\unlq.json', 'r') as json_file:
            self.unlq = json.load(json_file)
        modal = BetModal(self.lobby_id, self.user_id, "blue")
        if self.unlq['players'][str(self.user_id)]['unp'] < 10:
            await interaction.response.send_message("You don't have enough UN Points to bet.", ephemeral=True)
        else:
            if str(self.lobby_id) not in self.unlq['players'][str(self.user_id)]['bets'].keys():
                await interaction.response.send_modal(modal)
            else:
                await interaction.response.send_message("You've already placed a bet for this game.", ephemeral=True)

    @discord.ui.button(label='Red team', style=discord.ButtonStyle.red)
    async def bet_on_red(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open('C:\\DATA\\unlq.json', 'r') as json_file:
            self.unlq = json.load(json_file)
        modal = BetModal(self.lobby_id, self.user_id, "red")
        if self.unlq['players'][str(self.user_id)]['unp'] < 10:
            await interaction.response.send_message("You don't have enough UN Points to bet.", ephemeral=True)
        else:
            if str(self.lobby_id) not in self.unlq['players'][str(self.user_id)]['bets'].keys():
                await interaction.response.send_modal(modal)
            else:
                await interaction.response.send_message("You've already placed a bet for this game.", ephemeral=True)