from io import BytesIO
import requests
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageFont

def make_image(game):
    back = Image.open('image\\img.png')
    coords = [
        (150, 100),
        (250, 300),
        (430, 330),
        (620, 510),
        (700, 600),
        (300, 50),
        (430, 150),
        (530, 250),
        (720, 430),
        (820, 500)
    ]
    index = 0
    for team in game.teams:
        for player in team.players:
            if player.user.avatar:
                avatar = requests.get(player.user.avatar.url)
                fore = Image.open(BytesIO(avatar.content))
            else:
                fore = Image.open('image\\blank.png')
            fore.thumbnail((90, 90),Image.ANTIALIAS)
            mask = Image.open('image\\mask.png').convert('L').resize(fore.size)
            back.paste(fore, coords[index], mask=mask)
            name_tag_font = ImageFont.truetype("arial.ttf", 20)
            name_tag_text = player.name
            W, H = coords[index]
            back_editable = ImageDraw.Draw(back)
            w, h = back_editable.textsize(name_tag_text)
            back_editable.text(((W-w+50),(H-h+100)), name_tag_text, font=name_tag_font)
            index += 1
            
    back.save(fp=('image\\res.png'))