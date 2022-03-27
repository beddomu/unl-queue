import urllib
import os
import json

def get_match_history(puuid):
    try:
        with urllib.request.urlopen("https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids?api_key={}".format(puuid, os.getenv("RIOT_API_KEY"))) as file:
            match_history = json.loads(file.read().decode())
            return match_history
    except Exception as e:
        print('error trying to find puuid')
    