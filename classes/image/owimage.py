from io import BytesIO
import requests
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageFont

def make_image(game):
    back = Image.open('classes\\image\\owimg.png')
    coords = [
        (100, 100),
        (275, 100),
        (450, 100),
        (625, 100),
        (800, 100),
        (100, 500),
        (275, 500),
        (450, 500),
        (625, 500),
        (800, 500)
    ]
    index = 0
    for team in game.teams:
        for player in team.players:
            if player.user.avatar:
                avatar = requests.get(player.user.avatar.url)
                fore = Image.open(BytesIO(avatar.content))
            else:
                fore = Image.open('classes\\image\\blank.png')
            fore.thumbnail((90, 90),Image.ANTIALIAS)
            mask = Image.open('classes\\image\\mask.png').convert('L').resize(fore.size)
            back.paste(fore, coords[index], mask=mask)
            name_tag_font = ImageFont.truetype("arial.ttf", 20)
            name_tag_text = player.name
            W, H = coords[index]
            back_editable = ImageDraw.Draw(back)
            w, h = back_editable.textsize(name_tag_text)
            back_editable.text(((W-w+50),(H-h+100)), name_tag_text, font=name_tag_font)
            index += 1
            
    back.save(fp=('classes\\image\\res.png'))