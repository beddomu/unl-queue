import urllib
import os
import json

def find_summoner(name):
    summoner_name = name.replace(" ", "").lower()
    account = None
    try:
        with urllib.request.urlopen("https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}".format(summoner_name, os.getenv("RIOT_API_KEY"))) as file:
            account = json.loads(file.read().decode())
    except Exception as e:
        print('error trying to find summoner')
    return account