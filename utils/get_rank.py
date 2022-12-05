
import os
import json
import aiohttp

async def get_rank(summoner_id):
    async with aiohttp.ClientSession() as session:
        file = await session.get("https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{}?api_key={}".format(summoner_id, os.getenv("RIOT_API_KEY")))
        ranks = await file.json()
        for rank in ranks:
            if rank['queueType'] == "RANKED_SOLO_5x5":
                return rank['tier']