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


dotenv.load_dotenv()
intents = discord.Intents.all()


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='.', intents = intents, application_id = int(os.getenv("APP_ID")))
        

    async def setup_hook(self):
        pass
            
    @tasks.loop(minutes=0.25)
    async def background_task(self):
        pass
        
    async def on_ready(self):
        guild = await self.fetch_guild(1070774301957034086)
        category = await guild.create_category(name="test", position=(1))
        await guild.create_voice_channel("Team Blue🔵", category=category)
        await guild.create_voice_channel("Team Red 🔴", category=category)
        

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
