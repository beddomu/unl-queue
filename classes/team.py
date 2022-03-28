from pprint import pprint
from classes.role import Role
from classes.player import Player

class Team:
    def __init__(self, player_limit: int, side: str):
        self.player_limit = player_limit
        self.players = []
        self.roles = []
        self.side = side
        self.rating = 0
        
    def __lt__(self, other):
        return self.rating < other.rating
                

    def add_player(self, obj):
        if isinstance(obj, Player):
            self.players.append(obj)
            self.rating += obj.rating
            

    def list_players(self):
        for player in self.players:
            print(player.name)

    def add_role(self, role):
        if isinstance(role, Role):
            self.roles.append(role)