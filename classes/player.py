import discord
from classes.role import Role


class Player:
    def __init__(self, id: int, name: str, role: Role, user: discord.User, ready: bool, ign: str, rating: int):
        self.id = id
        self.user = user
        self.name = name
        self.role = role
        self.ready = ready
        self.ign = ign
        self.rating = rating
        
'''    def __lt__(self, other):
        return self.rating < other.rating
    
    def __eq__(self, other):
        return self.rating == other.rating'''