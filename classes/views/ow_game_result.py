import json
import os
from pprint import pp
import queue
import sys
import typing
import discord
from discord.ext import commands
from classes.player import Player
from classes.views.match_found import MatchFoundView
from classes.views.matchmaking import MatchmakingView
from classes.role import Role, top, jungle, middle, bottom, support, fill
from utils.update_games import update_games
from utils.update_leaderboard import update_leaderboard

# Defines a custom Select containing colour options
# that the user can choose. The callback function
# of this class is called when the user changes their choice

class GameResult(discord.ui.Select):
    def __init__(self, id, bot):
        self.queue = queue
        self.bot = bot
        with open('C:\\DATA\\unlq.json', 'r') as json_file:
            self.unlq =  json.load(json_file)
        # Set the options that will be presented inside the dropdown
        options = []
        for lobby in self.unlq['owlobbies'].keys():
            if id in self.unlq['owlobbies'][lobby]['player_ids']['1']:
                option = discord.SelectOption(label=f'Lobby ID: {lobby}', value=int(lobby), emoji=None)
                options.append(option)
        for lobby in self.unlq['owlobbies'].keys():
            pp(lobby)
            if id in self.unlq['owlobbies'][lobby]['player_ids']['2']:
                option = discord.SelectOption(label=f'Lobby ID: {lobby}', value=int(lobby), emoji=None)
                options.append(option)
        super().__init__(placeholder='Select lobby ID...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        view = GameResultSide(self.values[0], self.bot)
        await interaction.response.edit_message(content=f"Who won this game?\n*Lobby ID: {self.values[0]}*", view=view)

class GameResultView(discord.ui.View):
    def __init__(self, id, bot):
        super().__init__()
        self.add_item(GameResult(id, bot))
        
class GameResultSide(discord.ui.View):
    def __init__(self, lobby, bot):
        self.bot = bot
        self.lobby = lobby
        super().__init__()
        with open('C:\\DATA\\unlq.json', 'r') as json_file:
            self.unlq = json.load(json_file)
        

    @discord.ui.button(label='Team 1', style=discord.ButtonStyle.primary)
    async def bet_on_1(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open('C:\\DATA\\unlq.json', 'r') as json_file:
            self.unlq = json.load(json_file)
        if self.unlq['owlobbies'][self.lobby]:
            await interaction.response.edit_message(content="Game result reported successfully", view=None)
            #bets
            for player in self.unlq['players'].keys():
                if str(self.lobby) in self.unlq['players'][player]['bets'].keys():
                    if "1" in self.unlq['players'][player]['bets'][str(self.lobby)].keys():
                        self.unlq['players'][player]['unp'] += self.unlq['players'][player]['bets'][str(self.lobby)]['1']*2
                        user = await self.bot.fetch_user(int(player))
                        await user.send(f"You made {self.unlq['players'][player]['bets'][str(self.lobby)]['1']*2} CQ Points betting on team 1.")
                        print(f"{self.unlq['players'][player]['discord_name']} made {self.unlq['players'][player]['bets'][str(self.lobby)]['1']*2} CQ Points betting on team 1.")

            for p in self.unlq['owlobbies'][self.lobby]['player_ids']['1']:
                self.unlq['players'][str(p)]['unp'] += 200
                
                if self.unlq['players'][str(p)]['mmr'] < 1000-75:
                    self.unlq['players'][str(p)]['mmr'] += 75
                else:
                    self.unlq['players'][str(p)]['mmr'] = 1000
                if "wins" in self.unlq['players'][str(p)].keys():
                    self.unlq['players'][str(p)]['wins'] += 1
                else:
                    self.unlq['players'][str(p)]['wins'] = 1
                blue = self.unlq['owlobbies'][str(self.lobby)]['1']
                red = self.unlq['owlobbies'][str(self.lobby)]['2']
                mmr = int(self.unlq['players'][str(p)]['mmr']/400)
                self.unlq['players'][str(p)]['points'] += int(15+mmr + (red-blue)*0.06)
                self.unlq['players'][str(p)]['lp_history'].append(f'+{int(15+mmr + (red-blue)*0.06)}')
                embed = discord.Embed(
                    title=f'+{int(15+mmr+(red-blue)*0.06)}')
                embed.set_footer(text=f'Lobby ID: {self.lobby}')
                embed.color = discord.colour.Color.green()
                embed.set_author(name="Champions Queue", icon_url=self.bot.user.avatar.url)
                user = await self.bot.fetch_user(int(p))
                embed.description = "{}'s current LP: {}".format(self.unlq['players'][str(p)]['name'], self.unlq['players'][str(p)]['points'])
                try:
                    await user.send(embed=embed)
                except:
                    print(f"Cannot send dm to: {user.name}")
                pp('{} gained {} LP'.format(self.unlq['players'][str(p)]['name'], int(15+mmr+(red-blue)*0.06)))
                
            for p in self.unlq['owlobbies'][self.lobby]['player_ids']['Red']:
                self.unlq['players'][str(p)]['unp'] += 200
                if self.unlq['players'][str(p)]['mmr'] > -1000+100:
                    self.unlq['players'][str(p)]['mmr'] -= 100
                else:
                    self.unlq['players'][str(p)]['mmr'] = -1000
                if "losses" in self.unlq['players'][str(p)].keys():
                    self.unlq['players'][str(p)]['losses'] += 1
                else:
                    self.unlq['players'][str(p)]['losses'] = 1
                blue = self.unlq['owlobbies'][str(self.lobby)]['1']
                red = self.unlq['owlobbies'][str(self.lobby)]['2']
                mmr = int(self.unlq['players'][str(p)]['mmr']/400)
                if self.unlq['players'][str(p)]['points'] >= int(15-mmr-(red-blue)*0.06):
                    self.unlq['players'][str(p)]['points'] -= int(15-mmr-(red-blue)*0.06)
                    self.unlq['players'][str(p)]['lp_history'].append(f'-{int(15-mmr-(red-blue)*0.06)}')
                    embed = discord.Embed(title=f'-{int(15-mmr-(red-blue)*0.06)}')
                    embed.set_footer(text=f'Lobby ID: {self.lobby}')
                    embed.color = discord.colour.Color.red()
                    embed.set_author(name="Champions Queue", icon_url=self.bot.user.avatar.url)
                    user = await self.bot.fetch_user(int(p))
                    embed.description = "{}'s current LP: {}".format(
                        self.unlq['players'][str(p)]['name'], self.unlq['players'][str(p)]['points'])
                    try:
                        await user.send(embed=embed)
                    except:
                        print(f"Cannot send dm to: {user.name}")
                    pp('{} lost {} LP'.format(self.unlq['players'][str(p)]['name'], int(15-mmr-(red-blue)*0.06)))

                else:
                    pp('{} is now at 0 LP'.format(self.unlq['players'][str(p)]['name']))
                    self.unlq['players'][str(p)]['points'] = 0
                    self.unlq['players'][str(p)]['lp_history'].append(f"-{self.unlq['players'][str(p)]['points']}")
                    embed = discord.Embed(title=f"-{self.unlq['players'][str(p)]['points']}")
                    embed.set_footer(text=f'Lobby ID: {self.lobby}')
                    embed.color = discord.colour.Color.red()
                    embed.set_author(name="Champions Queue", icon_url=self.bot.user.avatar.url)
                    user = await self.bot.fetch_user(int(p))
                    embed.description = "{}'s current LP: {} ._.".format(self.unlq['players'][str(p)]['name'], self.unlq['players'][str(p)]['points'])
                    try:
                        await user.send(embed=embed)
                    except:
                        print(
                            f"Cannot send dm to: {user.name}")
            channel = await self.bot.fetch_channel(int(os.getenv("LIVE")))
            try:
                message = await channel.fetch_message(self.unlq['owlobbies'][str(self.lobby)]['game_id'])
                await message.delete()
            except:
                pass

            with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
                json.dump(self.unlq, unlq_file)
                        
            update_games()
            await update_leaderboard()
            guild = interaction.guild
            try:
                game_category = discord.utils.get(guild.categories, name=self.lobby)
            except:
                print("Game category doesn't exist")
            queue_voice = discord.utils.get(guild.voice_channels, id=959880784116854794)
            for channel in game_category.voice_channels:
                for member in channel.members:
                    try:
                        await member.move_to(queue_voice)
                    except:
                        print(f'{self.unlq["players"][player]["discord_name"]} is not in the queue voice channel.')
                try:
                    await channel.delete()
                except:
                    print("Voice channel doesn't exist")
            try:
                await game_category.delete()
            except:
                print("Game category doesn't exist")
            del self.unlq['owlobbies'][str(self.lobby)]
            with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
                json.dump(self.unlq, unlq_file)
                unlq_file.close()
        else:
            await interaction.response.edit_message(content="This game was already reported.", view=None)

    @discord.ui.button(label='Team 1', style=discord.ButtonStyle.red)
    async def bet_on_red(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open('C:\\DATA\\unlq.json', 'r') as json_file:
            self.unlq = json.load(json_file)
        if self.unlq['owlobbies'][self.lobby]:
            await interaction.response.edit_message(content="Game result reported successfully", view=None)
            
            #bets
            for player in self.unlq['players'].keys():
                if str(self.lobby) in self.unlq['players'][player]['bets'].keys():
                    if "red" in self.unlq['players'][player]['bets'][str(self.lobby)].keys():
                        self.unlq['players'][player]['unp'] += self.unlq['players'][player]['bets'][str(self.lobby)]['red']*2
                        user = await self.bot.fetch_user(int(player))
                        await user.send(f"You made {self.unlq['players'][player]['bets'][str(self.lobby)]['red']*2} CQ Points betting on team red.")
                        print(f"{self.unlq['players'][player]['discord_name']} made {self.unlq['players'][player]['bets'][str(self.lobby)]['red']*2} CQ Points betting on team red.")
                        
            for p in self.unlq['owlobbies'][self.lobby]['player_ids']['Red']:
                self.unlq['players'][str(p)]['unp'] += 200
                if self.unlq['players'][str(p)]['mmr'] < 1000-75:
                    self.unlq['players'][str(p)]['mmr'] += 75
                else:
                    self.unlq['players'][str(p)]['mmr'] = 1000
                if "wins" in self.unlq['players'][str(p)].keys():
                    self.unlq['players'][str(p)]['wins'] += 1
                else:
                    self.unlq['players'][str(p)]['wins'] = 1
                blue = self.unlq['owlobbies'][str(self.lobby)]['1']
                red = self.unlq['owlobbies'][str(self.lobby)]['2']
                mmr = int(self.unlq['players'][str(p)]['mmr']/400)
                self.unlq['players'][str(p)]['points'] += int(15+mmr+(blue-red)*0.06)
                self.unlq['players'][str(p)]['lp_history'].append(f'+{int(15+mmr+(blue-red)*0.06)}')
                embed = discord.Embed(title=f'+{int(15+mmr+(blue-red)*0.06)}')
                embed.set_footer(text=f'Lobby ID: {self.lobby}')
                embed.color = discord.colour.Color.green()
                embed.set_author(name="Champions Queue", icon_url=self.bot.user.avatar.url)
                user = await self.bot.fetch_user(int(p))
                embed.description = "{}'s current LP: {}".format(
                    self.unlq['players'][str(p)]['name'], self.unlq['players'][str(p)]['points'])
                try:
                    await user.send(embed=embed)
                except:
                    print(f"Cannot send dm to: {user.name}")
                pp('{} gained {} LP'.format(self.unlq['players'][str(p)]['name'], int(15+mmr+(blue-red)*0.06)))
                
                
            for p in self.unlq['owlobbies'][self.lobby]['player_ids']['Blue']:
                self.unlq['players'][str(p)]['unp'] += 200
                if self.unlq['players'][str(p)]['mmr'] > -1000+100:
                    self.unlq['players'][str(p)]['mmr'] -= 100
                else:
                    self.unlq['players'][str(p)]['mmr'] = -1000
                if "losses" in self.unlq['players'][str(p)].keys():
                    self.unlq['players'][str(p)]['losses'] += 1
                else:
                    self.unlq['players'][str(p)]['losses'] = 1
                blue = self.unlq['owlobbies'][str(self.lobby)]['1']
                red = self.unlq['owlobbies'][str(self.lobby)]['2']
                mmr = int(self.unlq['players'][str(p)]['mmr']/400)
                if self.unlq['players'][str(p)]['points'] >= int(15-mmr-(red-blue)*0.06):
                    self.unlq['players'][str(p)]['points'] -= int(15-mmr-(red-blue)*0.06)
                    self.unlq['players'][str(p)]['lp_history'].append(f'-{int(15-mmr-(red-blue)*0.06)}')
                    embed = discord.Embed(title=f'-{int(15-mmr-(red-blue)*0.06)}')
                    embed.set_footer(text=f'Lobby ID: {self.lobby}')
                    embed.color = discord.colour.Color.red()
                    embed.set_author(name="Champions Queue", icon_url=self.bot.user.avatar.url)
                    user = await self.bot.fetch_user(int(p))
                    embed.description = "{}'s current LP: {}".format(self.unlq['players'][str(p)]['name'], self.unlq['players'][str(p)]['points'])
                    try:
                        await user.send(embed=embed)
                    except:
                        print(f"Cannot send dm to: {user.name}")
                    pp('{} lost {} LP'.format(self.unlq['players'][str(p)]['name'], int(15-mmr-(red-blue)*0.06)))
                    with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
                        json.dump(self.unlq, unlq_file)
                        unlq_file.close()

                else:
                    pp('{} lost a game at 0 LP'.format(self.unlq['players'][str(p)]['name']))
                    self.unlq['players'][str(p)]['points'] = 0
                    self.unlq['players'][str(p)]['lp_history'].append(f"-{self.unlq['players'][str(p)]['points']}")
                    embed = discord.Embed(title=f"-{self.unlq['players'][str(p)]['points']}")
                    embed.set_footer(text=f'Lobby ID: {self.lobby}')
                    embed.color = discord.colour.Color.red()
                    embed.set_author(name="Champions Queue", icon_url=self.bot.user.avatar.url)
                    user = await self.bot.fetch_user(int(p))
                    embed.description = "{}'s current LP: {} ._.".format(self.unlq['players'][str(p)]['name'], self.unlq['players'][str(p)]['points'])
                    try:
                        await user.send(embed=embed)
                    except:
                        print(
                            f"Cannot send dm to: {user.name}")
                        
            channel = await self.bot.fetch_channel(int(os.getenv("LIVE")))
            try:
                message = await channel.fetch_message(self.unlq['owlobbies'][str(self.lobby)]['game_id'])
                await message.delete()
            except:
                pass

            with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
                json.dump(self.unlq, unlq_file)
                        
            update_games()
            await update_leaderboard()
            guild = interaction.guild
            try:
                game_category = discord.utils.get(guild.categories, name=self.lobby)
            except:
                print("Game category doesn't exist")
            queue_voice = discord.utils.get(guild.voice_channels, id=959880784116854794)
            try:
                for channel in game_category.voice_channels:
                    for member in channel.members:
                        try:
                            await member.move_to(queue_voice)
                        except:
                            print(f'{self.unlq["players"][player]["discord_name"]} is not in the queue voice channel.')
                
                    await channel.delete()
            except:
                print("Voice channel doesn't exist")
            try:
                await game_category.delete()
            except:
                print("Game category doesn't exist")
            del self.unlq['owlobbies'][str(self.lobby)]
            with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
                json.dump(self.unlq, unlq_file)
                unlq_file.close()
        else:
            await interaction.response.edit_message(content="This game was already reported.", view=None)