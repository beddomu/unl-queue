from time import sleep
import time
from async_timeout import timeout
from lcu import lockfile
import requests
from pprint import pp, pprint


def leave_lobby(timeout_in_seconds: int = 60*5):
    member_joined = False
    timeout = time.time() + timeout_in_seconds
    while member_joined == False or time.time() > timeout:

        url = f'https://127.0.0.1:{lockfile.port}/lol-lobby/v2/lobby'

        headers = {'accept': 'application/json',
                   'Authorization': f'Basic {lockfile.auth}', 'Content-Type': 'application/json'}

        r = requests.get(url, headers=headers, verify=True)

        pp("waiting for someone to join...")

        file = r.json()
        if len(file['members']) > 1 or time.time() > timeout:
            member_joined = True
            print("SOMEONE JOINED! Leaving the lobby now.")
            url = f'https://127.0.0.1:{lockfile.port}/lol-lobby/v2/lobby'
            requests.delete(url=url, headers=headers)
            break
        sleep(1)
