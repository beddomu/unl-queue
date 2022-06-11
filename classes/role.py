class Role:
    def __init__(self, name: str, id: int, emoji: str):
        self.id = id
        self.name = name
        self.emoji = emoji
        
    def __repr__(self):
        rep = self.name
        return rep

top = Role("Top", 0, "<:top:985153368563539988>")
jungle = Role("Jungle", 1, "<:jungle:985153365212295249>")
middle = Role("Middle", 2, "<:mid:985153366801915924>")
bottom = Role("Bottom", 3, "<:bot:985153363274522694>")
support = Role("Support", 4, "<:support:985153369779896391>")
fill = Role("Fill", 5, "<:fill:985153779148140584>")