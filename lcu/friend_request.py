import json
import aiohttp
from pprint import pp, pprint
from utils.find_summoner import find_summoner
from lcu import lockfile

async def friend_request(name):
    async with aiohttp.ClientSession() as session:
        account = await find_summoner(name)

        url = f'https://127.0.0.1:{lockfile.port}/lol-summoner/v2/summoners/names'
        data = [account['name']]
        headers = {'accept': 'application/json','Authorization': f'Basic {lockfile.auth}', 'Content-Type': 'application/json'}
        r = await session.post(url, headers=headers, data=json.dumps(data), verify_ssl= False)
        file = await r.json()
        summonerId = int(file[0]['summonerId'])
        summonerName = account['name']


        url = f'https://127.0.0.1:{lockfile.port}/lol-chat/v1/friend-requests'
        headers = {'accept': 'application/json',
                    'Authorization': f'Basic {lockfile.auth}', 'Content-Type': 'application/json'}
        data_json = {
            "direction": "both",
            "name": account['name'],
            "gameTag": "EUW"
            }
        data = json.dumps(data_json)
        r = await session.post(url, headers=headers, data=data, verify_ssl=False)
        if r.status == 204:
            print('Friend request was successfully sent to: {}'.format(account['name']))
        else:
            pprint(r.content)