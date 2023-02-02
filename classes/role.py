class Role:
    def __init__(self, name: str, id: int, emoji: str):
        self.id = id
        self.name = name
        self.emoji = emoji
        
    def __repr__(self):
        rep = self.name
        return rep

top = Role("Top", 0, "<:top:1070777307050016849> ")
jungle = Role("Jungle", 1, "<:jungle:1070777302079782912> ")
middle = Role("Middle", 2, "<:mid:1070777303287726200> ")
bottom = Role("Bottom", 3, "<:bot:1070777298153902110> ")
support = Role("Support", 4, "<:support:1070777306005643334> ")
fill = Role("Fill", 5, "<:fill:1070777299827429519>")