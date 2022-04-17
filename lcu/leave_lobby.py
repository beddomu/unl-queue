from time import sleep
import time
from async_timeout import timeout
from lcu import lockfile
import requests
from pprint import pp, pprint


def leave_lobby(timeout_in_seconds: int = 30):
    member_joined = False
    time_all_invited = time.time()
    pp("waiting for someone to join...")
    while member_joined == False:

        url = f'https://127.0.0.1:{lockfile.port}/lol-lobby/v2/lobby'

        headers = {'accept': 'application/json',
                   'Authorization': f'Basic {lockfile.auth}', 'Content-Type': 'application/json'}

        r = requests.get(url, headers=headers, verify=False)

        file = r.json()
        if len(file['members']) > 1:
            member_joined = True
            print("Leaving the lobby now...")
            url = f'https://127.0.0.1:{lockfile.port}/lol-lobby/v2/lobby'
            requests.delete(url=url, headers=headers, verify=False)
            break
        sleep(1)
