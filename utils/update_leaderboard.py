import collections
import json
import os
from pprint import pp
import random
import discord
from discord.ext import commands
from git import Repo

async def update_leaderboard():
        with open('C:\\DATA\\unlq.json', 'r') as file:
            unlq = json.load(file)

        dict = {}

        for player in unlq['players']:
            dict[player] = {}
            dict[player]['summonerIconId'] = unlq['players'][player]['summonerIconId']
            dict[player]['name'] = unlq['players'][player]['name']
            dict[player]['lp'] = unlq['players'][player]['points']
            dict[player]['wins'] = unlq['players'][player]['wins']
            dict[player]['losses'] = unlq['players'][player]['losses']
            
        res = collections.OrderedDict(sorted(dict.items(), key=lambda t:t[1]["lp"], reverse=True))
        with open('..\\unlqueue.xyz\\json\\leaderboard.json', 'w') as unlq_file:
            json.dump(res, unlq_file)
            
            
repo_dir = '..\\unlqueue.xyz'
repo = Repo(repo_dir)
file_list = [
    'json\\leaderboard.json'
]
commit_message = 'Updating leaderboard'
repo.index.add(file_list)
repo.index.commit(commit_message)
origin = repo.remote('origin')
origin.push()