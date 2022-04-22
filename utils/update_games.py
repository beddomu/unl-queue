import os
import json
import collections

def update_games():
    games = {}
    i = 0
    for fn in os.listdir("C:\\DATA\\games"):
        with open(f'C:\\DATA\\games\\{fn}', 'r') as file:
            game = json.load(file)
            games[fn] = {}
            games[fn]["game_id"] = game['info']['gameId']
            games[fn]["game_end"] = game['info']['gameEndTimestamp']
            

        parsed = {}
        parsed['players'] = []
        parsed['teams'] = []
        parsed['index'] = i
        parsed['gameId'] = game['info']['gameId']
        parsed['gameId'] = game['info']['gameId']
        parsed['gameEndTimestamp'] = game['info']['gameEndTimestamp']
        for participant in game['info']['participants']:
            player = {}
            player['teamId'] = participant['teamId']
            player['summonerName'] = participant['summonerName']
            player['championId'] = participant['championId']
            player['summoner1Id'] = participant['summoner1Id']
            player['summoner2Id'] = participant['summoner2Id']
            player['kills'] = participant['kills']
            player['deaths'] = participant['deaths']
            player['assists'] = participant['assists']
            player['kda'] = participant['challenges']['kda']
            player['item0'] = participant['item0']
            player['item1'] = participant['item1']
            player['item2'] = participant['item2']
            player['item3'] = participant['item3']
            player['item4'] = participant['item4']
            player['item5'] = participant['item5']
            player['totalDamageDealtToChampions'] = participant['totalDamageDealtToChampions']
            player['visionScore'] = participant['visionScore']
            player['individualPosition'] = participant['individualPosition']
            
            parsed['players'].append(player)
            
        
        
        for t in game['info']['teams']:
            team = {}
            team['win'] = game['info']['teams'][game['info']['teams'].index(t)]['win']
            team['teamId'] = game['info']['teams'][game['info']['teams'].index(t)]['teamId']
            
            parsed['teams'].append(team)
        
        with open(f'..\\unlqueue.xyz\\games\\{fn}', 'w') as web_game:
            json.dump(parsed, web_game)
        i += 1

    res = collections.OrderedDict(sorted(games.items(), key=lambda t:t[1]["game_end"], reverse=True))
            
    with open('..\\unlqueue.xyz\\games\\games.json' , 'w') as file:
        json.dump(res, file)