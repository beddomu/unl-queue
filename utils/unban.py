import json


def unban(player_id):
    banned_until = 0
    with open('C:\\DATA\\unlq.json', 'r') as file:
        unlq = json.load(file)
    unlq['players'][str(player_id)]['banned_until'] = banned_until
    with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
        json.dump(unlq, unlq_file)      