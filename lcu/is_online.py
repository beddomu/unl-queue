import json
import aiohttp
from pprint import pp, pprint
from utils.find_summoner import find_summoner
from lcu import lockfile

async def is_online(name):
    async with aiohttp.ClientSession() as session:
        account = await find_summoner(name)

        url = f'https://127.0.0.1:{lockfile.port}/lol-chat/v1/friends'
        headers = {'accept': 'application/json',
                    'Authorization': f'Basic {lockfile.auth}', 'Content-Type': 'application/json'}

        r = await session.get(url, headers=headers, verify_ssl=False)
        if r.status == 200:
            friends = await r.json()
            for friend in friends:
                if friend['name'] == account['name']:
                    if friend['availability'] not in ["mobile", "offline"]:
                        return True
                    else:
                        return False