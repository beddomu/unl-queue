import json
import os
import discord
from discord.ext import commands
from pprint import pp

import urllib

from utils.send_leaderboard import send_leaderboard


async def report_game(bot: commands.Bot, game_id):
        with open('C:\\DATA\\unlq.json', 'r') as unlq_file:
            unlq_json =  json.load(unlq_file)
        
        if int(game_id) not in unlq_json['games']:
            try:
                with urllib.request.urlopen("https://europe.api.riotgames.com/lol/match/v5/matches/EUW1_{}?api_key={}".format(game_id, os.getenv("RIOT_API_KEY"))) as game_json:
                    game = json.loads(game_json.read().decode())
                    lobby_id = game['info']['gameName']
                    if lobby_id[9:] in unlq_json['lobbies'].keys():
                        channel = await bot.fetch_channel(int(os.getenv("LIVE")))
                        try:
                            message = await channel.fetch_message(unlq_json['lobbies'][str(lobby_id[9:])]['game_id'])
                            await message.delete()
                        except:
                            pass
                        unlq_json['games'].append(game['info']['gameId'])
                        with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
                            json.dump(unlq_json, unlq_file)
                            unlq_file.close()
                        with open(f'C:\\DATA\\games\\{str(game_id)}.json', 'w') as game_file:
                            json.dump(game, game_file)
                            game_file.close()

                        #points
                        if game['info']:
                            for p in game['info']['participants']:
                                if p['win'] == True:                                    
                                    if p['teamId'] == 100:                               
                                        #print('{} won'.format(p['summonerName']))
                                        with open('C:\\DATA\\unlq.json', 'r') as unlq_file:
                                            unlq_json =  json.load(unlq_file)
                                        for player in unlq_json['players'].keys():
                                            if unlq_json['players'][player]['puuid'] == p['puuid']:
                                                blue = unlq_json['lobbies'][str(lobby_id[9:])]['blue_team']
                                                red = unlq_json['lobbies'][str(lobby_id[9:])]['red_team']
                                                unlq_json['players'][player]['points'] += int(15+(red-blue)*0.06)
                                                embed = discord.Embed(title=f'+{int(15+(red-blue)*0.06)}')
                                                embed.set_footer(text=f'game id: {game_id}')
                                                embed.color = discord.colour.Color.green()
                                                embed.set_author(name="UNL Queue", icon_url=bot.user.avatar.url)
                                                user = await bot.fetch_user(int(player))
                                                embed.description = "{}'s current LP: {}".format(unlq_json['players'][player]['name'], unlq_json['players'][player]['points'])
                                                await user.send(embed=embed)
                                                pp('{} gained {} LP'.format(p['summonerName'], int(15+(red-blue)*0.06)))
                                                with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
                                                    json.dump(unlq_json, unlq_file)
                                                    unlq_file.close()
                                    else:
                                        with open('C:\\DATA\\unlq.json', 'r') as unlq_file:
                                            unlq_json =  json.load(unlq_file)
                                        for player in unlq_json['players'].keys():
                                            if unlq_json['players'][player]['puuid'] == p['puuid']:
                                                blue = unlq_json['lobbies'][str(lobby_id[9:])]['blue_team']
                                                red = unlq_json['lobbies'][str(lobby_id[9:])]['red_team']
                                                unlq_json['players'][player]['points'] += int(15+(blue-red)*0.06)
                                                embed = discord.Embed(title=f'+{int(15+(blue-red)*0.06)}')
                                                embed.set_footer(text=f'game id: {game_id}')
                                                embed.color = discord.colour.Color.green()
                                                embed.set_author(name="UNL Queue", icon_url=bot.user.avatar.url)
                                                user = await bot.fetch_user(int(player))
                                                embed.description = "{}'s current LP: {}".format(unlq_json['players'][player]['name'], unlq_json['players'][player]['points'])
                                                await user.send(embed=embed)
                                                pp('{} gained {} LP'.format(p['summonerName'], int(15+(blue-red)*0.06)))
                                                with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
                                                    json.dump(unlq_json, unlq_file)
                                                    unlq_file.close()
                                else:
                                    #print('{} lost'.format(p['summonerName']))
                                    if p['teamId'] == 100:
                                        with open('C:\\DATA\\unlq.json', 'r') as unlq_file:
                                            unlq_json =  json.load(unlq_file)
                                        for player in unlq_json['players'].keys():
                                            if unlq_json['players'][player]['puuid'] == p['puuid']:
                                                blue = unlq_json['lobbies'][str(lobby_id[9:])]['blue_team']
                                                red = unlq_json['lobbies'][str(lobby_id[9:])]['red_team']
                                                if unlq_json['players'][player]['points'] > int(12+(red-blue)*0.06):
                                                    unlq_json['players'][player]['points'] -= int(12+(red-blue)*0.06)
                                                    embed = discord.Embed(title=f'-{int(12+(red-blue)*0.06)}')
                                                    embed.set_footer(text=f'game id: {game_id}')
                                                    embed.color = discord.colour.Color.red()
                                                    embed.set_author(name="UNL Queue", icon_url=bot.user.avatar.url)
                                                    user = await bot.fetch_user(int(player))
                                                    embed.description = "{}'s current LP: {}".format(unlq_json['players'][player]['name'], unlq_json['players'][player]['points'])
                                                    await user.send(embed=embed)
                                                    pp('{} lost {} LP'.format(p['summonerName'], int(12+(red-blue)*0.06)))
                                                    with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
                                                        json.dump(unlq_json, unlq_file)
                                                        unlq_file.close()

                                                else:
                                                    unlq_json['players'][player]['points'] = 0
                                                    with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
                                                        json.dump(unlq_json, unlq_file)
                                                        unlq_file.close()
                                    else:
                                        with open('C:\\DATA\\unlq.json', 'r') as unlq_file:
                                            unlq_json =  json.load(unlq_file)
                                        
                                        for player in unlq_json['players'].keys():
                                            if unlq_json['players'][player]['puuid'] == p['puuid']:
                                                blue = unlq_json['lobbies'][str(lobby_id[9:])]['blue_team']
                                                red = unlq_json['lobbies'][str(lobby_id[9:])]['red_team']
                                                if unlq_json['players'][player]['points'] > int(12+(blue-red)*0.06):
                                                    await user.send(embed=embed)
                                                    unlq_json['players'][player]['points'] -= int(12+(blue-red)*0.06)
                                                    embed = discord.Embed(title=f'-{int(12+(blue-red)*0.06)}')
                                                    embed.set_footer(text=f'game id: {game_id}')
                                                    embed.color = discord.colour.Color.red()
                                                    embed.set_author(name="UNL Queue", icon_url=bot.user.avatar.url)
                                                    user = await bot.fetch_user(int(player))
                                                    embed.description = "{}'s current LP: {}".format(unlq_json['players'][player]['name'], unlq_json['players'][player]['points'])
                                                    pp('{} lost {} LP'.format(p['summonerName'], int(12+(blue-red)*0.06)))
                                                    with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
                                                        json.dump(unlq_json, unlq_file)
                                                        unlq_file.close()
                                                
                                                else:
                                                    pp('{} lost a game at 0 LP'.format(p['summonerName']))
                                                    unlq_json['players'][player]['points'] = 0
                                                    embed = discord.Embed(title='-0')
                                                    embed.set_footer(text=f'game id: {game_id}')
                                                    embed.color = discord.colour.Color.red()
                                                    embed.set_author(name="UNL Queue", icon_url=bot.user.avatar.url)
                                                    user = await bot.fetch_user(int(player))
                                                    embed.description = "{}'s current LP: {} ._.".format(unlq_json['players'][player]['name'], unlq_json['players'][player]['points'])
                                                    await user.send(embed=embed)
                                                    with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
                                                        json.dump(unlq_json, unlq_file)
                                                        unlq_file.close()
                                    
                            channel = await bot.fetch_channel(int(os.getenv("LEADERBOARD")))
                            await send_leaderboard(bot)
                        del unlq_json['lobbies'][str(lobby_id[9:])]
                        with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
                            json.dump(unlq_json, unlq_file)
                            unlq_file.close()
                        
            except urllib.error.HTTPError as e:
                print('HTTPError: {}'.format(e.code))
                pp("Game not found.")
            except urllib.error.URLError as e:
                print('URLError: {}'.format(e.reason))
                pp("Game not found.")