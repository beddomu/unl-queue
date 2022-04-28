from pprint import pp
import urllib
import os
import json

def get_match_history(puuid):
    try:
        with urllib.request.urlopen("https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids?start=0&count=20&api_key={}".format(puuid, os.getenv("RIOT_API_KEY"))) as file:
            match_history = json.loads(file.read().decode())
            pp(match_history[:5])
            return match_history
    except Exception as e:
        print('error trying to find puuid')
    