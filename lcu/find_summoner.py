import urllib
import os
import json

def find_summoner(name):
    summoner_name = name.replace(" ", "").lower()
    account = None
    try:
        with urllib.request.urlopen("https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}".format(summoner_name, "RGAPI-0414a021-91f6-4db1-a814-65a72ad68cf1")) as champ_json:
            account = json.loads(champ_json.read().decode())
    except Exception as e:
        print('error trying to find summoner')
    return account
