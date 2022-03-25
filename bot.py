import asyncio
import os
from discord import Object
import discord
from discord.ext import commands, tasks
from discord import app_commands
import dotenv


dotenv.load_dotenv()
intents = discord.Intents.all()


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='.', intents = intents, application_id = int(os.getenv("APP_ID")))
        

    async def setup_hook(self):
        self.background_task.start()
            
    @tasks.loop(minutes=10)
    async def background_task(self):
        print('Running background task...')
        
    async def on_ready(self):
        print('ready')
        for fn in os.listdir("./cogs"):
            if fn.endswith(".py"):
                await bot.load_extension(f'cogs.{fn[:-3]}')
        await self.tree.sync(guild = discord.Object(int(os.getenv("SERVER_ID"))))

bot = MyBot()

asyncio.run(bot.run(os.getenv("TOKEN")))
