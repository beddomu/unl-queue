import asyncio
import json
import os
import random
import time
from discord import Object
import discord
from discord.ext import commands, tasks
from discord import app_commands
import dotenv
from utils.find_summoner import find_summoner
from utils.get_match_history import get_match_history
from utils.report_game import report_game


dotenv.load_dotenv()
intents = discord.Intents.all()


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='.', intents = intents, application_id = int(os.getenv("APP_ID")))
        

    async def setup_hook(self):
        self.background_task.start()
            
    @tasks.loop(minutes=1)
    async def background_task(self):
        with open('C:\\DATA\\unlq.json', 'r') as file:
            unlq = json.load(file)
            
        for lobby in unlq['lobbies'].keys():
            if time.time() > unlq['lobbies'][lobby]['time_created'] + 60 * 60 * 2:
                print(f"Lobby {lobby} expired")
                del unlq['lobbies'][lobby]
                with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
                    json.dump(unlq, unlq_file)
                    unlq_file.close()
            else:
                random_ign = unlq['lobbies'][lobby]['players'][random.randint(0, len(unlq['lobbies'][lobby]['players'])-1)]
                account = find_summoner(random_ign)
                if account:
                    history = get_match_history(account['puuid'])
                    if history:
                        for game in history[:3]:
                            await report_game(self, game[5:])
        
            time.sleep(0.5)
        
    async def on_ready(self):
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
