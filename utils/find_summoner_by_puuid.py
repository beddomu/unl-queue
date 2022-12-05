import aiohttp
import os

async def find_summoner(puuid):
    async with aiohttp.ClientSession() as session:
        try:
            file = await session.get("https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{}?api_key={}".format(puuid, os.getenv("RIOT_API_KEY")))
            account = await file.json()
        except Exception as e:
            print('error trying to find summoner', e)
        return account