
from urllib.request import urlopen
import os
import json

def get_rank(summoner_id):
        with urlopen("https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{}?api_key={}".format(summoner_id, os.getenv("RIOT_API_KEY"))) as file:
            ranks = json.loads(file.read().decode())
            for rank in ranks:
                if rank['queueType'] == "RANKED_SOLO_5x5":
                    return rank['tier']