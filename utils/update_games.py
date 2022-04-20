import os
import json

def update_games():
    games = []
    for fn in os.listdir("C:\\DATA\\games"):
            with open(f'C:\\DATA\\games\\{fn}', 'r') as file:
                game = json.load(file)
            games.insert(0, game)
            
    with open('..\\unlqueue.xyz\\games\\games.json') as file:
        json.dump(games, file)