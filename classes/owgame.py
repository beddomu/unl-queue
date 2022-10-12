from pprint import pprint, pp
from classes.team import Team

class Game:
    def __init__(self, team1: Team, team2: Team, winner: Team):
        self.id = int
        self.teams = [team1, team2]
        self.players = []
        self.team1 = team1
        self.team2 = team2

    def get_player_mentions(self):
        list = []
        for player in self.players:
            list.append(player.user.mention)
        return list

    def get_players(self):
        list = []
        for team in self.teams:
            for player in team.players:
                list.append(player)
        return list

    def players_ready_check(self):
        for player in self.players:
            if player.ready != True:
                return False
        return True