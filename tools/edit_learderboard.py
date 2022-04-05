import json

with open('C:\\DATA\\unlq.json', 'r') as file:
    unlq = json.load(file)
    
for p in unlq['players']:
    if 'last_dodge' in unlq['players'][p].keys():
        del unlq['players'][p]['last_dodge']
    else:
        print(unlq['players'][p]['discord_name'])
        

with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
    json.dump(unlq, unlq_file)