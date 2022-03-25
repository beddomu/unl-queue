import asyncio
import json
import os
import random
import aiohttp
import discord
from discord.ext import commands
from discord import app_commands
from classes.player import Player
from classes.queue import Queue
from classes.views.role_select import RoleSelectView





class UNLQueue(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self._bot = bot

    async def cog_load(self):
        self.queue = Queue(5)
        channel = await self._bot.fetch_channel(os.getenv("QUEUE"))
        message = await channel.send("**Initializing...**")
        self.queue.message = message
        await self.queue.new_lobby()
        print("Queue initialized")
    
    @app_commands.command(name="queue", description="Enter this command to view the queue options")
    @app_commands.guilds(int(os.getenv("SERVER_ID")))
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=RoleSelectView(self.queue), ephemeral=True)

    @commands.command(name="addfillrandom", aliases=["r"])
    @commands.has_permissions(manage_messages=True)
    async def add_random_fill(self, ctx: commands.context.Context, input: int):
        if len(self.queue.players) < 10:
            n = 0
            while n < input:
                user = random.choice(self.queue.message.channel.guild.members)
                player = Player(user.id, user.name, self.queue.roles[random.randint(0, 5)], user, True, "beddomu", 60)
                if player not in self.queue.players:
                    await self.queue.add_player(player)
                    await self.queue.update_lobby()
                    n += 1
                
                
                if self.queue.full == True and self.queue.locked != True:
                    #view = MatchFoundView()
                    await self.queue.pop(self.queue)
                    break
    
    @commands.command(name="debug", aliases=["c"])
    @commands.has_permissions(manage_messages=True)
    async def debug(self, ctx):
        self.queue.list_players()
        



async def setup(bot: commands.Bot):
    await bot.add_cog(UNLQueue(bot))