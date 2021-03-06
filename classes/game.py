from pprint import pprint, pp
from classes.team import Team

class Game:
    def __init__(self, blue_team: Team, red_team: Team, winner: Team):
        self.id = int
        self.teams = [blue_team, red_team]
        self.players = []
        self.blue_team = blue_team
        self.red_team = red_team

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