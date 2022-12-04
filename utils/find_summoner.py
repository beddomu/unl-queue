import imp
from urllib.request import urlopen
import os
import json
import aiohttp
import asyncio

async def find_summoner(name):
    async with aiohttp.ClientSession() as session:
        summoner_name = name.replace(" ", "").lower()
        account = None
        try:
            async with session.get("https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}".format(summoner_name, os.getenv("RIOT_API_KEY"))) as file:
                account = await file.json()
        except Exception as e:
            print('error trying to find summoner', e)
        return account