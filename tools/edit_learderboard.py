import json

with open('C:\\DATA\\unlq.json', 'r') as file:
    unlq = json.load(file)
    
for p in unlq['players']:
    for n in unlq['players'][p]['lp_history']:
        unlq['players'][p]['lp_history'][unlq['players'][p]['lp_history'].index(n)] = int(float(n))

with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
    json.dump(unlq, unlq_file)