from pprint import pprint
import aiohttp
import json
from lcu import lockfile


class Lobby:
    def __init__(self, name: str, password=None, team_size: int = 5, map_id: int = 11, mutator_id: int = 2):
        self.auth = lockfile.auth
        self.port = lockfile.port
        self.name = name
        self.password = password
        self.team_size = team_size
        self.map_id = map_id
        self.mutator_id = mutator_id
        self.url = 'https://127.0.0.1:{}/lol-lobby/v2/lobby'.format(self.port)
        self.payload = {
            "customGameLobby": {
                "configuration": {
                    "gameMode": "CLASSIC",
                    "gameMutator": "",
                    "gameServerRegion": "EUW",
                    "mapId": self.map_id,
                    "mutators": {
                        "id": self.mutator_id
                    },
                    "spectatorPolicy": "AllAllowed",
                    "teamSize": self.team_size
                },
                "lobbyName": "UNLQ ID: {}".format(self.name),
                "lobbyPassword": "{}".format(password)
            },
            "isCustom": True
        }
        self.headers = {'accept': 'application/json', 'Authorization': 'Basic {}'.format(self.auth), 'Content-Type': 'application/json'}

    async def create(self):
        async with aiohttp.ClientSession() as session:
            r = await session.post(self.url, data=json.dumps(self.payload),headers=self.headers, verify_ssl=False)
            if r.status == 200:
                print("Lobby created successfully")



