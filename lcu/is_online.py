from time import sleep
import json
import requests
from pprint import pp, pprint
from utils.find_summoner import find_summoner
from lcu import lockfile

def is_online(name):
    
    account = find_summoner(name)

    url = f'https://127.0.0.1:{lockfile.port}/lol-chat/v1/friends'
    headers = {'accept': 'application/json',
                'Authorization': f'Basic {lockfile.auth}', 'Content-Type': 'application/json'}

    r = requests.get(url, headers=headers, verify=True)
    if r.status_code == 200:
        friends = r.json()
        for friend in friends:
            if friend['name'] == account['name']:
                if friend['availability'] not in ["mobile", "offline"]:
                    return True
                else:
                    return False