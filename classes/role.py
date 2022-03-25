class Role:
    def __init__(self, name: str, id: int, emoji: str):
        self.id = id
        self.name = name
        self.emoji = emoji

top = Role("Top", 0, "<:top:949215554441465866>")
jungle = Role("Jungle", 1, "<:jungle:949215552591765544>")
middle = Role("Middle", 2, "<:mid:949215552621129728>")
bottom = Role("Bottom", 3, "<:bot:949215552507883560>")
support = Role("Support", 4, "<:support:949215552180719617>")
fill = Role("Fill", 5, "<:fill:949215552671469578>")