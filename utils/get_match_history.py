from pprint import pp
import aiohttp
import os
import json

async def get_match_history(puuid):
    async with aiohttp.ClientSession() as session:
        try:
            file = await session.get("https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids?start=0&count=20&api_key={}".format(puuid, os.getenv("RIOT_API_KEY")))
            match_history = await file.json()
            pp(match_history[:5])
            return match_history
        except Exception as e:
            print(f'error trying to find puuid')
    