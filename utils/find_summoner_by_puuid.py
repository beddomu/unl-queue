import imp
from urllib.request import urlopen
import os
import json

def find_summoner(puuid):
    try:
        with urlopen("https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{}?api_key={}".format(puuid, os.getenv("RIOT_API_KEY"))) as file:
            account = json.loads(file.read().decode())
    except Exception as e:
        print('error trying to find summoner', e)
    return account