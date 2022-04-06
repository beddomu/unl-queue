
import asyncio
import os
from pprint import pp
import discord
from discord.ext import commands
import random
import dotenv

dotenv.load_dotenv()

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

intents = discord.Intents.all()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='.', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} connected to discord')

@bot.command(name="test")
async def move(ctx):
    guild = bot.get_guild(603515060119404584)
    role = discord.utils.get(guild.roles, id = 676740137815900160)
    member = guild.get_member(301821822502961152)
    permissions = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        role: discord.PermissionOverwrite(view_channel=False),
        member: discord.PermissionOverwrite(view_channel=True),
        bot.user: discord.PermissionOverwrite(view_channel=True)
    }
    unlq_channel = discord.utils.get(guild.categories, id=953292613115605012)
    category = await guild.create_category(name="<game id>", position=(unlq_channel.position - 1), overwrites=permissions)
    await guild.create_voice_channel("Team Blue🔵", category=category, overwrites= permissions)
    await guild.create_voice_channel("Team Red 🔴", category=category, overwrites= permissions)
    #voice = discord.utils.get(ctx.guild.voice_channels, name="yo")
    #await guild.create_role(name="Team Blue", color=discord.colour.Color.blue)
    #role = discord.utils.get(guild.roles, name = "Team Blue")
    #await member.add_roles(role)
    
@bot.command(name="delete")
async def delete(ctx):
    guild = bot.get_guild(603515060119404584)
    category = discord.utils.get(guild.categories, name = "<game id>")
    for channel in category.voice_channels:
        await channel.delete()
    await category.delete()

asyncio.run(bot.run(os.getenv("TOKEN")))