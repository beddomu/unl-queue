import json
import os

players = {}


index = 0
kills = 0
deaths = 0
assists = 0
damage = 0
secondsPlayed = 0
wards = 0
time_dead = 0
name = str
skillshots_dodged = 0
skillshots_hit = 0
multi_kill = 0
solo_kills = 0
csd = 0
skillshots_dodged_small_window = 0

input = input("Player: ")

for fn in os.listdir("C:\\DATA\\games"):
    with open(f'C:\\DATA\\games\\{fn}', 'r') as file:
        game = json.load(file)
    
    for player in game['info']['participants']:
        if player['summonerName'] == input:
            name = player['summonerName']
            index += 1
            kills += player['kills']
            deaths += player['deaths']
            assists += player['assists']
            damage += player['totalDamageDealtToChampions']
            secondsPlayed += player['timePlayed']
            wards += player['wardsPlaced']
            time_dead += player['totalTimeSpentDead']
            skillshots_dodged += player['challenges']['skillshotsDodged']
            skillshots_hit += player['challenges']['skillshotsHit']
            skillshots_dodged_small_window += player['challenges']['dodgeSkillShotsSmallWindow']
            multi_kill += player['challenges']['multikills']
            solo_kills += player['challenges']['soloKills']
            try:
                csd += player['challenges']['maxCsAdvantageOnLaneOpponent']
            except:
                pass

minutesPlayed = secondsPlayed/60
print(name)
print(f'Games played: {index}')
print(f'Time spent dead per game (in minutes): {time_dead/index/60}')
print(f'Wards per game: {wards/index}')
print(f'Damage: {damage}')
print(f'Damage per minute: {damage/minutesPlayed}')
print(f'Kills: {kills}')
print(f'Deaths: {deaths}')
print(f'Assists: {assists}')
print(f'KDA: {(kills + assists) / deaths}')
print(f'Skillshots hit: {skillshots_hit}')
print(f'Skillshots dodged (big window): {skillshots_dodged}')
print(f'Skillshots dodged (small window): {skillshots_dodged_small_window}')
print(f'Skillshots hit per game: {skillshots_hit/index}')
print(f'Skillshots dodged per game (big window): {skillshots_dodged/index}')
print(f'Skillshots dodged (small window) per game: {skillshots_dodged_small_window/index}')
print(f'multi_kill_after_flash: {multi_kill}')
print(f'Solo kills: {solo_kills}')
print(f'Solo kills per game: {solo_kills/index}')
print(f'Max CS lead per game: {csd/index}')