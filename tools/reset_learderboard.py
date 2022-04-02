import json

with open('C:\\DATA\\unlq.json', 'r') as file:
    unlq = json.load(file)
    
for player in unlq['players']:
    unlq['players'][player]['points'] = 0
    unlq['players'][player]['wins'] = 0
    unlq['players'][player]['losses'] = 0

with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
    json.dump(unlq, unlq_file)