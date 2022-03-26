import os
from pprint import pp
import discord
import urllib
import json

class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(content="This account was successfully linked.", view=None, embed=None)
        self.value = True
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(content="You canceled this operation.", view=None, embed=None)
        self.value = False
        self.stop()
            

class LinkAccount(discord.ui.Modal):
    def __init__(self, queue, title="Link your EUW account", timeout=5 * 60, custom_id = "linkaccount"):
        super().__init__(title = title, timeout=timeout, custom_id=custom_id)  # 5 minutes
        self.queue = queue

        self.name = discord.ui.TextInput(
            label="Summoner name",
            min_length=3,
            max_length=50,
        )
        self.add_item(self.name)
        
    async def callback(self, interaction: discord.Interaction):
        
        with open('C:\\DATA\\unlq.json', 'r') as json_file:
            unlq_json = json.load(json_file)

        account_name = self.name.value.replace(" ", "").lower()
        account = None
        with urllib.request.urlopen("https://ddragon.leagueoflegends.com/api/versions.json") as version_json:
            version = json.loads(version_json.read().decode())
        try:
            with urllib.request.urlopen("https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}".format(account_name, os.getenv("RIOT_API_KEY"))) as champ_json:
                account = json.loads(champ_json.read().decode())
        except Exception as e:
            await interaction.response.send_message(content="Account not found. Try again or ask <@!301821822502961152> for help", ephemeral=True)
            pp(e)
        if account:
            embed = discord.Embed(
                title=account['name'], description='Level {}'.format(account['summonerLevel']))
            embed.set_thumbnail(
                url="https://ddragon.leagueoflegends.com/cdn/{}/img/profileicon/{}.png".format(version[0], account['profileIconId']))
            #embed.set_footer(text="`Summoner id: {}`".format(account['id']))
            embed.set_author(name=interaction.user.name)
            view = Confirm()
            await interaction.response.send_message(content="Is this your account?", view=view, embed=embed, ephemeral=True)

            await view.wait()

            if view.value is None:
                print('Timed out...')
            elif view.value:
                if not str(interaction.user.id) in unlq_json['players'].keys():
                    unlq_json['players'][str(interaction.user.id)] = {}
                    unlq_json['players'][str(interaction.user.id)]['discord_name'] = interaction.user.name
                    unlq_json['players'][str(interaction.user.id)]['points'] = 0
                    unlq_json['players'][str(interaction.user.id)]['last_dodge'] = 0
                    unlq_json['players'][str(interaction.user.id)]['id'] = account['id']
                    unlq_json['players'][str(interaction.user.id)]['accountId'] = account['accountId']
                    unlq_json['players'][str(interaction.user.id)]['puuid'] = account['puuid']
                    unlq_json['players'][str(interaction.user.id)]['rating'] = 60
                    channel = await self.queue.message.guild.fetch_channel(int(os.getenv("CHAT")))
                    await channel.send("{} linked a new account with the IGN: {}".format(interaction.user.name, account['name']))
                    

                unlq_json['players'][str(interaction.user.id)]["name"] = account['name']
                
                

                with open('C:\\DATA\\unlq.json', 'w') as json_file:
                    json.dump(unlq_json, json_file, ensure_ascii=False)

