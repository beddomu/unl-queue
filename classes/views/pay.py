import os
from pprint import pp
import time
import discord
import json

            

class Pay(discord.ui.Modal):
    def __init__(self, sender: discord.User, receiver: discord.Member, title="Receiver", timeout=5 * 60, custom_id="pay"):
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        with open('C:\\DATA\\unlq.json', 'r') as json_file:
            self.unlq = json.load(json_file)
            self.sender = sender
            self.receiver = receiver

        self.pay = discord.ui.TextInput(
            label=f"Amount",
            placeholder= f"Your CQ Points: {self.unlq['players'][str(sender.id)]['unp']}",
            min_length=1,
            max_length=10
        )
        
        
        self.message = discord.ui.TextInput(
            label='Message',
            style=discord.TextStyle.long,
            placeholder='Optional message',
            required=False,
            max_length=300,
        )
        
        self.add_item(self.pay)
        self.add_item(self.message)
        
    async def on_submit(self, interaction: discord.Interaction):
        if self.pay.value.isnumeric():
            amount = int(self.pay.value)
            with open('C:\\DATA\\unlq.json', 'r') as file:
                unlq = json.load(file)
                
            if unlq['players'][str(self.sender.id)]['unp'] >= amount:
                
                if amount > 0:
                    unlq['players'][str(self.sender.id)]['unp'] -= amount
                    
                    try:
                        unlq['players'][str(self.receiver.id)]['unp'] += amount
                        
                        await interaction.response.send_message(f"You sent {self.receiver.mention} {amount} CQ Points.", ephemeral=True)
                        await self.receiver.send(f"{self.sender.name} sent you {amount} CQ Points\nMessage: *{self.message.value}*")
                    except:
                        await interaction.response.send_message(f"This operation requires both parties to have an account. {self.receiver.mention} doesn't have an account linked.", ephemeral=True)
                else:
                    await interaction.response.send_message("The amount needs to be greater than 0.", ephemeral=True)
            else:
                await interaction.response.send_message("You don't have that many CQ Points.", ephemeral=True)
                
            with open('C:\\DATA\\unlq.json', 'w') as json_file:
                json.dump(unlq, json_file, ensure_ascii=False)
        else:
            await interaction.response.send_message("That needs to be a number!", ephemeral=True)
                    
    async def on_error(self, error: Exception, interaction: discord.Interaction) -> None:
        pp(error)
        await interaction.response.send_message('Something went wrong.', ephemeral=True)