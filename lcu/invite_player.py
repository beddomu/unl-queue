from time import sleep
import json
import requests
from pprint import pp, pprint
from lcu.is_online import is_online
from utils.find_summoner import find_summoner
from lcu import lockfile

def invite_player(name):
    
    account = find_summoner(name)

    url = f'https://127.0.0.1:{lockfile.port}/lol-summoner/v2/summoners/names'
    data = [account['name']]
    headers = {'accept': 'application/json','Authorization': f'Basic {lockfile.auth}', 'Content-Type': 'application/json'}
    r = requests.post(url, headers=headers, data=json.dumps(data), verify=True)
    file = r.json()
    summonerId = int(file[0]['summonerId'])
    summonerName = account['name']


    url = f'https://127.0.0.1:{lockfile.port}/lol-lobby/v2/lobby/invitations'
    headers = {'accept': 'application/json',
                'Authorization': f'Basic {lockfile.auth}', 'Content-Type': 'application/json'}
    data_json = [
        {
            "invitationType": "lobby",
            "state": "Pending",
            "timestamp": "",
            "toSummonerId": summonerId,
            "toSummonerName": summonerName
        }
    ]
    data = json.dumps(data_json)
    if is_online(account['name']):
        r = requests.post(url, headers=headers, data=data, verify=False)
        if r.status_code == 200:
            print('{} was successfully invited to the lobby'.format(account['name']))
        elif r.status_code == 400:
            print(f"{account['name']} was already invited")
        else:
            pprint(r.content)
    else:
        print(f"{account['name']} is offline")