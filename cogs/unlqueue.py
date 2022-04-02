import asyncio
import json
import os
import random
import discord
from discord.ext import commands
from discord import Interaction, TextChannel, app_commands
from classes.player import Player
from classes.queue import Queue
from classes.views.match_found import MatchFoundView
from classes.views.matchmaking import MatchmakingView
from classes.views.role_select import RoleSelectView
from classes.role import fill
from classes.views.report import Report
from classes.views.link import LinkAccount
from utils.update_leaderboard import update_leaderboard



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
    async def queue_command(self, interaction: discord.Interaction):
        if interaction.user.id not in self.queue.get_all_ids():
            try:
                await interaction.response.send_message(view=RoleSelectView(self.queue), ephemeral=True)
            except:
                print("error at 37 in unlqueue.py")
        else:
            try:
                await interaction.response.send_message(view=MatchmakingView(self.queue), ephemeral=True)
            except:
                print("error at 42 in unlqueue.py")

    @app_commands.command(name="report", description="Enter this command to report a player")
    @app_commands.guilds(int(os.getenv("SERVER_ID")))
    async def report_player(self, interaction: discord.Interaction):
        await interaction.response.send_modal(Report(self._bot))
        
    @app_commands.command(name="link", description="Enter this command to link your EUW account")
    @app_commands.guilds(int(os.getenv("SERVER_ID")))
    async def link_account(self, interaction: discord.Interaction):
        await interaction.response.send_modal(LinkAccount())


    @commands.command(name="addfillrandom", aliases=["r"])
    @commands.has_permissions(manage_messages=True)
    async def add_random_fill(self, ctx: commands.context.Context, input: int):
            n = 0
            while n < input:
                if len(self.queue.players) < 10:
                    user = random.choice(self.queue.message.channel.guild.members)
                    with open('C:\\DATA\\unlq.json', 'r') as json_file:
                        unlq_json =  json.load(json_file)
                    if str(user.id) in unlq_json['players'].keys() and user.id not in [301821822502961152]:
                        player = Player(user.id, user.name, fill, user, True, "beddomu", unlq_json['players'][str(user.id)]['rating'])
                        if player not in self.queue.players:
                            self.queue.players.append(player)
                            n += 1
                else:
                    break
            else:
                await self.queue.update_lobby()
                    
    @commands.command(name="addfill", aliases=["f"])
    @commands.has_permissions(manage_messages=True)
    async def add_fill_dummy(self, ctx: commands.context.Context, input: int):
            n = 0
            while n < input:
                if len(self.queue.players) < 10:
                    player = Player(948863727032217641, f"Target dummy {n + 1}", fill, ctx.author, False, None, 50)
                    await self.queue.add_player(player)
                    n += 1
                else:
                    break
                
    @commands.command(name="debug", aliases=["c"])
    @commands.has_permissions(manage_messages=True)
    async def debug(self, ctx):
        self.queue.list_players()
        
    @commands.command(name="develop", aliases=["dev"])
    @commands.has_permissions(manage_messages=True)
    async def dev(self, ctx):
        guild = await self._bot.fetch_guild(int(os.getenv("SERVER_ID")))
        role = discord.utils.get(guild.roles, id = 676740137815900160)
        channel = await self._bot.fetch_channel(int(os.getenv("QUEUE")))
        await channel.set_permissions(role, read_messages=False)
        channel = await self._bot.fetch_channel(int(os.getenv("LIVE")))
        await channel.set_permissions(role, read_messages=False)
        
    @commands.command(name="public", aliases=["p"])
    @commands.has_permissions(manage_messages=True)
    async def public(self, ctx):
        guild = await self._bot.fetch_guild(int(os.getenv("SERVER_ID")))
        role = discord.utils.get(guild.roles, id = 676740137815900160)
        channel = await self._bot.fetch_channel(int(os.getenv("QUEUE")))
        await channel.set_permissions(role, read_messages=True)
        channel = await self._bot.fetch_channel(int(os.getenv("LIVE")))
        await channel.set_permissions(role, read_messages=True)
        
    @commands.command(name="leaderboard", aliases=["l"])
    @commands.has_permissions(manage_messages=True)
    async def leaderboard(self, ctx):
        await update_leaderboard()
        
    @commands.command(name="reset", aliases=["n"])
    @commands.has_permissions(manage_messages=True)
    async def newlobbymessage(self, ctx: commands.context.Context):
        self.queue.locked = False
        await self.queue.reset_lobby()
        channel = await self._bot.fetch_channel(int(os.getenv("CHAT")))
        #await channel.send("The lobby was reset. Queue up again here: https://discord.com/channels/603515060119404584/953616729911726100")
        



async def setup(bot: commands.Bot):
    await bot.add_cog(UNLQueue(bot))