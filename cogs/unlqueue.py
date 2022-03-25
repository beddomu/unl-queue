import asyncio
import json
import os
import random
import aiohttp
import discord
from discord.ext import commands
from discord import Interaction, app_commands
from classes.player import Player
from classes.queue import Queue
from classes.views.match_found import MatchFoundView
from classes.views.matchmaking import MatchmakingView
from classes.views.role_select import RoleSelectView
from classes.role import fill





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
        if interaction.user.id not in self.queue.get_all_ids():
            await interaction.response.send_message(view=RoleSelectView(self.queue), ephemeral=True)
        else:
            await interaction.response.send_message(view=MatchmakingView(self.queue), ephemeral=True)

    @commands.command(name="addfill", aliases=["f"])
    @commands.has_permissions(manage_messages=True)
    async def add_fill_dummy(self, ctx: commands.context.Context, input: int):
        if len(self.queue.players) < 10:
            n = 0
            while n < input:
                player = Player(ctx.author.id, f"Target dummy {n + 1}", fill, ctx.author, False, "beddomu", 50)
                await self.queue.add_player(player)
                n += 1
                
    @commands.command(name="debug", aliases=["c"])
    @commands.has_permissions(manage_messages=True)
    async def debug(self, ctx):
        self.queue.list_players()
        



async def setup(bot: commands.Bot):
    await bot.add_cog(UNLQueue(bot))