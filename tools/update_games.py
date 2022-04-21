import collections
import os
import json


games = {}
for fn in os.listdir("C:\\DATA\\games"):
        with open(f'C:\\DATA\\games\\{fn}', 'r') as file:
            game_file = json.load(file)
            games[fn] = {}
            games[fn]["game_id"] = game_file['info']['gameId']
            games[fn]["game_end"] = game_file['info']['gameEndTimestamp']

res = collections.OrderedDict(sorted(games.items(), key=lambda t:t[1]["game_end"], reverse=True))
        
with open('..\\unlqueue.xyz\\games\\games.json' , 'w') as file:
    json.dump(res, file)