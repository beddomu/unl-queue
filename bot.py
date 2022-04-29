import asyncio
import datetime
import json
import os
import random
import time
from discord import Object
import discord
from discord.ext import commands, tasks
from discord import app_commands
import dotenv
import pytz
from utils.find_summoner import find_summoner
from utils.get_match_history import get_match_history
from utils.report_game import report_game


dotenv.load_dotenv()
intents = discord.Intents.all()


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='.', intents = intents, application_id = int(os.getenv("APP_ID")))
        

    async def setup_hook(self):
        pass
            
    @tasks.loop(minutes=0.25)
    async def background_task(self):
        with open('C:\\DATA\\unlq.json', 'r') as file:
            unlq = json.load(file)
        if unlq['dev_mode'] == True:
            now = datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp(), pytz.timezone('Europe/London'))
            if 0 <= now.weekday() <= 4:
                if datetime.time(19) <= now.time() <= datetime.time(22):
                    print("Opening queue...")

                    unlq['dev_mode'] = False

                    with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
                        json.dump(unlq, unlq_file)
                    guild = await self._bot.fetch_guild(int(os.getenv("SERVER_ID")))
                    role = discord.utils.get(guild.roles, id = 676740137815900160)
                    channel = await self._bot.fetch_channel(int(os.getenv("QUEUE")))
                    await channel.set_permissions(role, read_messages=True)
                    channel = await self._bot.fetch_channel(int(os.getenv("LIVE")))
                    await channel.set_permissions(role, read_messages=True)
                    self.queue.devmode = False
                    await self.queue.new_lobby()
        
    async def on_ready(self):
        self.background_task.start()
        for fn in os.listdir("./cogs"):
            if fn.endswith(".py"):
                await bot.load_extension(f'cogs.{fn[:-3]}')
        await self.tree.sync(guild = discord.Object(int(os.getenv("SERVER_ID"))))

bot = MyBot()

@bot.event
async def on_message(message):
    if message.channel.id == int(os.getenv("QUEUE")) and message.author.id != bot.user.id:
        await bot.process_commands(message)
        try:
            await message.delete()
        except:
            pass

asyncio.run(bot.run(os.getenv("TOKEN")))
