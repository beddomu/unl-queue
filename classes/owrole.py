class Role:
    def __init__(self, name: str, id: int, emoji: str):
        self.id = id
        self.name = name
        self.emoji = emoji
        
    def __repr__(self):
        rep = self.name
        return rep

dps = Role("DPS", 0, "<:OW2dps:1029808066058797157>")
tank = Role("Tank", 1, "<:OW2tank:1029808067673587722>")
support = Role("Support", 2, "<:OW2support:1029808069330346124>")
fill = Role("Fill", 3, "<:OW2:1029808843338821632>")