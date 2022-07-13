import json

with open('C:\\DATA\\unlq.json', 'r') as file:
    unlq = json.load(file)
    
for p in unlq['players']:
    unlq['players'][p]['mmr'] = 0
        

with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
    json.dump(unlq, unlq_file)