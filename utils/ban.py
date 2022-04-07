import json
import time
import datetime


def ban(player_id, seconds):
    banned_until = time.time() + seconds
    with open('C:\\DATA\\unlq.json', 'r') as file:
        unlq = json.load(file)
    unlq['players'][str(player_id)]['banned_until'] = banned_until
    with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
        json.dump(unlq, unlq_file)
    value = datetime.datetime.fromtimestamp(banned_until)
    res = value.strftime('%Y-%m-%d %H:%M:%S')
    return res