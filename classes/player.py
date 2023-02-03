import discord
from classes.role import Role


class Player:
    def __init__(self, id: int, name: str, role1: Role, user: discord.User, ready: bool, ign: str, rating: int, role2 = None):
        self.id = id
        self.user = user
        self.name = name
        self.role1 = role1
        self.role2 = role2
        self.ready = ready
        self.ign = ign
        self.rating = rating

    def __repr__(self):
        rep = self.name
        return rep
        
    def __lt__(self, other):
        return self.rating < other.rating