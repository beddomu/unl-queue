import json
import os
import discord
from discord.ext import commands
from pprint import pp
import dotenv
import urllib
from utils.find_summoner import find_summoner

from utils.update_leaderboard import update_leaderboard


async def report_game(bot: commands.Bot, game_id, guild: discord.Guild):
    with open('C:\\DATA\\unlq.json', 'r') as unlq_file:
        unlq_json = json.load(unlq_file)

    if int(game_id) not in unlq_json['games']:

        with urllib.request.urlopen("https://europe.api.riotgames.com/lol/match/v5/matches/EUW1_{}?api_key={}".format(game_id, os.getenv("RIOT_API_KEY"))) as game_json:
            game = json.loads(game_json.read().decode())
            lobby_id = game['info']['gameName']
            if lobby_id[9:] in unlq_json['lobbies'].keys():
                channel = await bot.fetch_channel(int(os.getenv("LIVE")))
                message = await channel.fetch_message(unlq_json['lobbies'][str(lobby_id[9:])]['game_id'])
                await message.delete()
                unlq_json['games'].append(game['info']['gameId'])
                with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
                    json.dump(unlq_json, unlq_file)
                    unlq_file.close()
                with open(f'C:\\DATA\\games\\{str(game_id)}.json', 'w') as game_file:
                    json.dump(game, game_file)
                    game_file.close()
                
                # bets
                if game['info']['teams'][0]['win'] == True:
                    for player in unlq_json['players'].keys():
                            if str(lobby_id[9:]) in unlq_json['players'][player]['bets'].keys():
                                if "blue" in unlq_json['players'][player]['bets'][str(lobby_id[9:])].keys():
                                    unlq_json['players'][player]['unp'] += unlq_json['players'][player]['bets'][str(lobby_id[9:])]['blue']*2
                                    user = await bot.fetch_user(int(player))
                                    await user.send(f"You made {unlq_json['players'][player]['bets'][str(lobby_id[9:])]['blue']*2} UN Points betting on team blue.")
                                    print(f"{unlq_json['players'][player]['discord_name']} made {unlq_json['players'][player]['bets'][str(lobby_id[9:])]['blue']*2} UN Points betting on team blue.")
                                    del unlq_json['players'][player]['bets'][str(lobby_id[9:])]
                elif game['info']['teams'][1]['win'] == True:
                    for player in unlq_json['players'].keys():
                            if str(lobby_id[9:]) in unlq_json['players'][player]['bets'].keys():
                                if "red" in unlq_json['players'][player]['bets'][str(lobby_id[9:])].keys():
                                    unlq_json['players'][player]['unp'] += unlq_json['players'][player]['bets'][str(lobby_id[9:])]['red']*2
                                    user = await bot.fetch_user(int(player))
                                    await user.send(f"You made {unlq_json['players'][player]['bets'][str(lobby_id[9:])]['red']*2} UN Points betting on team red.")
                                    print(f"{unlq_json['players'][player]['discord_name']} made {unlq_json['players'][player]['bets'][str(lobby_id[9:])]['red']*2} UN Points betting on team red.")
                                    del unlq_json['players'][player]['bets'][str(lobby_id[9:])]
                with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
                    json.dump(unlq_json, unlq_file)
                    

                # lp
                if game['info']:
                    
                    #update icon
                    for p in game['info']['participants']:
                        with open('C:\\DATA\\unlq.json', 'r') as unlq_file:
                            unlq_json = json.load(unlq_file)
                        for player in unlq_json['players'].keys():
                            if unlq_json['players'][player]['puuid'] == p['puuid']:
                                account = find_summoner(p['name'])
                                unlq_json['players'][player]['summonerIconId'] = account['profileIconId']
                    with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
                        json.dump(unlq_json, unlq_file)
                        
                        if p['win'] == True:
                            if p['teamId'] == 100:
                                with open('C:\\DATA\\unlq.json', 'r') as unlq_file:
                                    unlq_json = json.load(unlq_file)
                                for player in unlq_json['players'].keys():
                                    if unlq_json['players'][player]['puuid'] == p['puuid']:
                                        if unlq_json['players'][player]['mmr'] < 1000-75:
                                            unlq_json['players'][player]['mmr'] += 75
                                        else:
                                            unlq_json['players'][player]['mmr'] = 1000
                                        if "wins" in unlq_json['players'][player].keys():
                                            unlq_json['players'][player]['wins'] += 1
                                        else:
                                            unlq_json['players'][player]['wins'] = 1
                                        blue = unlq_json['lobbies'][str(
                                            lobby_id[9:])]['blue_team']
                                        red = unlq_json['lobbies'][str(
                                            lobby_id[9:])]['red_team']
                                        mmr = int(unlq_json['players'][player]['mmr']/200)
                                        unlq_json['players'][player]['points'] += int(
                                            15+mmr + (red-blue)*0.06)
                                        unlq_json['players'][player]['lp_history'].append(f'+{int(15+mmr + (red-blue)*0.06)}')
                                        embed = discord.Embed(
                                            title=f'+{int(15+mmr+(red-blue)*0.06)}')
                                        embed.set_footer(
                                            text=f'game id: {game_id}')
                                        embed.color = discord.colour.Color.green()
                                        embed.set_author(
                                            name="UNL Queue", icon_url=bot.user.avatar.url)
                                        user = await bot.fetch_user(int(player))
                                        embed.description = "{}'s current LP: {}".format(
                                            unlq_json['players'][player]['name'], unlq_json['players'][player]['points'])
                                        try:
                                            await user.send(embed=embed)
                                        except:
                                            print(
                                                f"Cannot send dm to: {user.name}")
                                        pp('{} gained {} LP'.format(
                                            p['summonerName'], int(15+mmr+(red-blue)*0.06)))
                                        with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
                                            json.dump(unlq_json, unlq_file)
                                            unlq_file.close()
                            else:
                                with open('C:\\DATA\\unlq.json', 'r') as unlq_file:
                                    unlq_json = json.load(unlq_file)
                                for player in unlq_json['players'].keys():
                                    if unlq_json['players'][player]['puuid'] == p['puuid']:
                                        if unlq_json['players'][player]['mmr'] < 1000-75:
                                            unlq_json['players'][player]['mmr'] += 75
                                        else:
                                            unlq_json['players'][player]['mmr'] = 1000
                                        if "wins" in unlq_json['players'][player].keys():
                                            unlq_json['players'][player]['wins'] += 1
                                        else:
                                            unlq_json['players'][player]['wins'] = 1
                                        blue = unlq_json['lobbies'][str(
                                            lobby_id[9:])]['blue_team']
                                        red = unlq_json['lobbies'][str(
                                            lobby_id[9:])]['red_team']
                                        mmr = int(unlq_json['players'][player]['mmr']/200)
                                        unlq_json['players'][player]['points'] += int(
                                            15+mmr+(blue-red)*0.06)
                                        unlq_json['players'][player]['lp_history'].append(f'+{int(15+mmr+(blue-red)*0.06)}')
                                        embed = discord.Embed(
                                            title=f'+{int(15+mmr+(blue-red)*0.06)}')
                                        embed.set_footer(
                                            text=f'game id: {game_id}')
                                        embed.color = discord.colour.Color.green()
                                        embed.set_author(
                                            name="UNL Queue", icon_url=bot.user.avatar.url)
                                        user = await bot.fetch_user(int(player))
                                        embed.description = "{}'s current LP: {}".format(
                                            unlq_json['players'][player]['name'], unlq_json['players'][player]['points'])
                                        try:
                                            await user.send(embed=embed)
                                        except:
                                            print(
                                                f"Cannot send dm to: {user.name}")
                                        pp('{} gained {} LP'.format(
                                            p['summonerName'], int(15+mmr+(blue-red)*0.06)))
                                        with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
                                            json.dump(unlq_json, unlq_file)
                                            unlq_file.close()
                        elif p['summonerName']:
                            if p['teamId'] == 100:
                                with open('C:\\DATA\\unlq.json', 'r') as unlq_file:
                                    unlq_json = json.load(unlq_file)
                                for player in unlq_json['players'].keys():
                                    if unlq_json['players'][player]['puuid'] == p['puuid']:
                                        if unlq_json['players'][player]['mmr'] > -1000+100:
                                            unlq_json['players'][player]['mmr'] -= 100
                                        else:
                                            unlq_json['players'][player]['mmr'] = -1000
                                        if "losses" in unlq_json['players'][player].keys():
                                            unlq_json['players'][player]['losses'] += 1
                                        else:
                                            unlq_json['players'][player]['losses'] = 1
                                        blue = unlq_json['lobbies'][str(
                                            lobby_id[9:])]['blue_team']
                                        red = unlq_json['lobbies'][str(
                                            lobby_id[9:])]['red_team']
                                        mmr = int(unlq_json['players'][player]['mmr']/200)
                                        if unlq_json['players'][player]['points'] >= int(15-mmr-(red-blue)*0.06):
                                            unlq_json['players'][player]['points'] -= int(15-mmr-(red-blue)*0.06)
                                            unlq_json['players'][player]['lp_history'].append(f'-{int(15-mmr-(red-blue)*0.06)}')
                                            embed = discord.Embed(title=f'-{int(15-mmr-(red-blue)*0.06)}')
                                            embed.set_footer(
                                                text=f'game id: {game_id}')
                                            embed.color = discord.colour.Color.red()
                                            embed.set_author(
                                                name="UNL Queue", icon_url=bot.user.avatar.url)
                                            user = await bot.fetch_user(int(player))
                                            embed.description = "{}'s current LP: {}".format(
                                                unlq_json['players'][player]['name'], unlq_json['players'][player]['points'])
                                            try:
                                                await user.send(embed=embed)
                                            except:
                                                print(
                                                    f"Cannot send dm to: {user.name}")
                                            pp('{} lost {} LP'.format(
                                                p['summonerName'], int(15-mmr-(red-blue)*0.06)))
                                            with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
                                                json.dump(unlq_json, unlq_file)
                                                unlq_file.close()

                                        else:
                                            pp('{} lost a game at 0 LP'.format(
                                                p['summonerName']))
                                            unlq_json['players'][player]['points'] = 0
                                            unlq_json['players'][player]['lp_history'].append(f"-{unlq_json['players'][player]['points']}")
                                            embed = discord.Embed(title=f"-{unlq_json['players'][player]['points']}")
                                            embed.set_footer(text=f'game id: {game_id}')
                                            embed.color = discord.colour.Color.red()
                                            embed.set_author(
                                                name="UNL Queue", icon_url=bot.user.avatar.url)
                                            user = await bot.fetch_user(int(player))
                                            embed.description = "{}'s current LP: {} ._.".format(
                                                unlq_json['players'][player]['name'], unlq_json['players'][player]['points'])
                                            try:
                                                await user.send(embed=embed)
                                            except:
                                                print(
                                                    f"Cannot send dm to: {user.name}")
                                            with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
                                                json.dump(unlq_json, unlq_file)
                                                unlq_file.close()
                            else:
                                with open('C:\\DATA\\unlq.json', 'r') as unlq_file:
                                    unlq_json = json.load(unlq_file)
                                for player in unlq_json['players'].keys():
                                    if unlq_json['players'][player]['puuid'] == p['puuid']:
                                        member = guild.get_member(int(player))

                                        if unlq_json['players'][player]['mmr'] > -1000+100:
                                            unlq_json['players'][player]['mmr'] -= 100
                                        else:
                                            unlq_json['players'][player]['mmr'] = -1000
                                        if "losses" in unlq_json['players'][player].keys():
                                            unlq_json['players'][player]['losses'] += 1
                                        else:
                                            unlq_json['players'][player]['losses'] = 1
                                        blue = unlq_json['lobbies'][str(
                                            lobby_id[9:])]['blue_team']
                                        red = unlq_json['lobbies'][str(
                                            lobby_id[9:])]['red_team']
                                        mmr = int(unlq_json['players'][player]['mmr']/200)
                                        if unlq_json['players'][player]['points'] >= int(15-mmr-(blue-red)*0.06):
                                            unlq_json['players'][player]['points'] -= int(15-mmr-(blue-red)*0.06)
                                            unlq_json['players'][player]['lp_history'].append(f'-{int(15-mmr-(blue-red)*0.06)}')
                                            embed = discord.Embed(title=f'-{int(15-mmr-(blue-red)*0.06)}')
                                            embed.set_footer(
                                                text=f'game id: {game_id}')
                                            embed.color = discord.colour.Color.red()
                                            embed.set_author(
                                                name="UNL Queue", icon_url=bot.user.avatar.url)
                                            user = await bot.fetch_user(int(player))
                                            embed.description = "{}'s current LP: {}".format(
                                                unlq_json['players'][player]['name'], unlq_json['players'][player]['points'])
                                            try:
                                                await user.send(embed=embed)
                                            except:
                                                print(
                                                    f"Cannot send dm to: {user.name}")
                                            pp('{} lost {} LP'.format(
                                                p['summonerName'], int(15-mmr-(blue-red)*0.06)))
                                            with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
                                                json.dump(unlq_json, unlq_file)
                                                unlq_file.close()

                                        else:
                                            pp('{} lost a game at 0 LP'.format(
                                                p['summonerName']))
                                            unlq_json['players'][player]['points'] = 0
                                            unlq_json['players'][player]['lp_history'].append(f"-{unlq_json['players'][player]['points']}")
                                            embed = discord.Embed(title=f"-{unlq_json['players'][player]['points']}")
                                            embed.set_footer(
                                                text=f'game id: {game_id}')
                                            embed.color = discord.colour.Color.red()
                                            embed.set_author(
                                                name="UNL Queue", icon_url=bot.user.avatar.url)
                                            user = await bot.fetch_user(int(player))
                                            embed.description = "{}'s current LP: {} ._.".format(
                                                unlq_json['players'][player]['name'], unlq_json['players'][player]['points'])
                                            try:
                                                await user.send(embed=embed)
                                            except:
                                                print(
                                                    f"Cannot send dm to: {user.name}")
                                            with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
                                                json.dump(unlq_json, unlq_file)
                                                unlq_file.close()
                    await update_leaderboard()
                    try:
                        game_category = discord.utils.get(
                            guild.categories, name=lobby_id[9:])
                    except:
                        print("Game category doesn't exist")
                    queue_voice = discord.utils.get(guild.voice_channels, id=959880784116854794)
                    for channel in game_category.voice_channels:
                        for member in channel.members:
                            try:
                                await member.move_to(queue_voice)
                            except:
                                print(
                                    f'{unlq_json["players"][player]["discord_name"]} is not in the queue voice channel.')
                        try:
                            await channel.delete()
                        except:
                            print("Voice channel doesn't exist")
                    try:
                        await game_category.delete()
                    except:
                        print("Game category doesn't exist")
                del unlq_json['lobbies'][str(lobby_id[9:])]
                with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
                    json.dump(unlq_json, unlq_file)
                    unlq_file.close()
