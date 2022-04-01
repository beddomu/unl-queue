import collections
import json
import os
from pprint import pp
import random
import discord
from discord.ext import commands

async def send_leaderboard(bot: commands.Bot):
        channel = await bot.fetch_channel(int(os.getenv("LEADERBOARD")))
        await channel.purge(limit=10)
        with open('C:\\DATA\\unlq.json', 'r') as file:
            unlq = json.load(file)
            dict = {}
        for player in unlq['players']:
            dict[unlq['players'][player]['discord_name']] = unlq['players'][player]['points']
        dict2 = sorted(dict.items(), key=lambda item: item[1], reverse=True)
        embed = discord.Embed(title="UNL Queue leaderboard")
        index = 1
        player_list = []
        lp_list = []
        for x in dict2:
            player = "#{} - {}".format(index, x[0])
            player_list.append(player)
            lp_list.append(str(x[1]))
            index += 1
        player_string = "\n".join(player_list)
        lp_string = "\n".join(lp_list)
        new_dict = {}

        for player in unlq['players']:
            new_dict[player] = {}
            new_dict[player]['summonerIconId'] = unlq['players'][player]['summonerIconId']
            new_dict[player]['name'] = unlq['players'][player]['name']
            new_dict[player]['lp'] = unlq['players'][player]['points']
            new_dict[player]['wins'] = random.randint(0, 10)
            new_dict[player]['losses'] = random.randint(0, 10)
            
        res = collections.OrderedDict(sorted(new_dict.items(), key=lambda t:t[1]["lp"], reverse=True))
        with open('..\\unlqueue.xyz\\json\\leaderboard.json', 'w') as unlq_file:
            json.dump(res, unlq_file)

        embed.add_field(name="Player", value=player_string)
        embed.add_field(name="LP", value=lp_string)
        await channel.send(embed=embed)