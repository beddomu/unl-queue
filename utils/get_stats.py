from functools import total_ordering
import json
import os

def get_stats(puuid):
    index = 0
    kills = 0
    deaths = 0
    assists = 0
    damage = 0
    secondsPlayed = 0
    secondsPlayedNotSupport = 0
    wards = 0
    time_dead = 0
    name = str
    skillshots_dodged = 0
    skillshots_hit = 0
    multi_kill = 0
    solo_kills = 0
    csd = 0
    skillshots_dodged_small_window = 0
    minions_killed = 0

    for fn in os.listdir("C:\\DATA\\games"):
        with open(f'C:\\DATA\\games\\{fn}', 'r') as file:
            game = json.load(file)
        
        for player in game['info']['participants']:
            if player['puuid'] == puuid:
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
                if player['individualPosition'] not in  ["UTILITY", "SUPPORT"]:
                    secondsPlayedNotSupport += player['timePlayed']
                try:
                    csd += player['challenges']['maxCsAdvantageOnLaneOpponent']
                except:
                    pass

    minutesPlayed = secondsPlayed/60
    s = ""
    s += f'**{name}**\n'
    s += f'Games played: {index}\n'
    s += f'Average time spent dead (in minutes): {round(time_dead/index/60, 2)}\n'
    s += f'Average wards placed: {wards/index}\n'
    s += f'Damage: {damage}\n'
    s += f'Damage per minute: {round(damage/minutesPlayed, 1)}\n'
    s += f'Kills: {kills}\n'
    s += f'Deaths: {deaths}\n'
    s += f'Assists: {assists}\n'
    s += f'KDA: {round((kills + assists) / deaths, 2)}\n'
    s += f'Skillshots hit: {skillshots_hit}\n'
    s += f'Skillshots dodged (big window): {skillshots_dodged}\n'
    s += f'Skillshots dodged (small window): {skillshots_dodged_small_window}\n'
    s += f'Average skillshots hit: {round(skillshots_hit/index, 1)}\n'
    s += f'Average skillshots dodged (big window): {round(skillshots_dodged/index, 1)}\n'
    s += f'Average skillshots dodged (small window): {round(skillshots_dodged_small_window/index)}\n'
    s += f'Multi kills: {multi_kill}\n'
    s += f'Solo kills: {solo_kills}\n'
    s += f'Average solo kills: {round(solo_kills/index, 1)}\n'
    s += f'Average Max CS lead: {round(csd/index)}\n'
    return s