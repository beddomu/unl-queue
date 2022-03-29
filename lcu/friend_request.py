from time import sleep
import json
import requests
from pprint import pp, pprint
from utils.find_summoner import find_summoner
from lcu import lockfile

def friend_request(name):
    
    account = find_summoner(name)

    url = f'https://127.0.0.1:{lockfile.port}/lol-summoner/v2/summoners/names'
    data = [account['name']]
    headers = {'accept': 'application/json','Authorization': f'Basic {lockfile.auth}', 'Content-Type': 'application/json'}
    r = requests.post(url, headers=headers, data=json.dumps(data), verify=True)
    file = r.json()
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
    r = requests.post(url, headers=headers, data=data, verify=True)
    if r.status_code == 204:
        print('Friend request was sucessfully sent to: {}'.format(account['name']))
    else:
        pprint(r.content)