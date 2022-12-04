from pprint import pp, pprint
import requests
import json
import lockfile


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
                        "id": self.mutator_id,
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

    def create(self):
        r = requests.post(self.url, data=json.dumps(self.payload),headers=self.headers)
        if r.status_code == 200:
            print("Lobby created successfully")
        else:
            pp(r.json())

lobby = Lobby('test', None, 5, 11, 6)
lobby.create()
