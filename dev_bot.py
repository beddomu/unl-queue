
import asyncio
import discord
from discord.ext import commands
import random

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

intents = discord.Intents.all()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='.', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.id}) connected to discord')

@bot.command(name="test")
async def move(ctx):
    guild = bot.get_guild(804695469195264030)
    member = guild.get_member(301821822502961152)
    role = discord.utils.get(guild.roles, id = 870268342655664158)
    category = 
    await guild.create_voice_channel("test", category=category)
    #await voice.set_permissions(role, view_channel=False)
    #voice = discord.utils.get(ctx.guild.voice_channels, name="yo")
    #await guild.create_role(name="Team Blue", color=discord.colour.Color.blue)
    #role = discord.utils.get(guild.roles, name = "Team Blue")
    #await member.add_roles(role)
    

asyncio.run(bot.run("OTUxNjUwOTQwMTMyMzk3MDU2.YiqkAA.MQ6snojxbck9QqAHOKrbAKRL0CQ"))