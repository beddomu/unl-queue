import json
import os
import time
from urllib.request import urlopen
import dotenv


dotenv.load_dotenv()


with open("C:\\DATA\\unlq.json", "r") as file:
    unlq = json.load(file)

for player in unlq['players'].keys():
    print("https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}".format(unlq['players'][player]['name'].replace(" ", "").lower(), str(os.getenv("RIOT_API_KEY"))))

    print(unlq['players'][player]['name'])
    with urlopen("https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}".format(unlq['players'][player]['name'].replace(" ", "").lower(), str(os.getenv("RIOT_API_KEY")))) as file:
        account = json.loads(file.read().decode())
    unlq['players'][player]['points'] = 0
    unlq['players'][player]['last_dodge'] = 0
    unlq['players'][player]['id'] = account['id']
    unlq['players'][player]['accountId'] = account['accountId']
    unlq['players'][player]['puuid'] = account['puuid']
    time.sleep(1)
    
print("Finished")

with open("C:\\DATA\\unlq.json", "w") as file:
    json.dump(unlq, file)