import asyncio
import datetime
import json
import os
import random
import time
import datetime
import discord
import pytz
from discord.ext import commands, tasks
from discord import Interaction, TextChannel, app_commands
from classes.player import Player
from classes.queue import Queue
from classes.views.matchmaking import MatchmakingView
from classes.views.role_select import RoleSelectView
from classes.role import fill
from classes.views.report import Report
from classes.views.link import LinkAccount
from utils.ban import ban
from utils.find_summoner import find_summoner
from utils.get_match_history import get_match_history
from utils.get_stats import get_stats
from utils.is_player_gold_plus import is_player_gold_plus
from utils.report_game import report_game
from utils.unban import unban
from utils.update_games import update_games
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
        with open('C:\\DATA\\unlq.json', 'r') as file:
            unlq = json.load(file)
        if str(interaction.user.id) in unlq['players']:
            if interaction.user.id not in self.queue.get_all_ids():
                if unlq['players'][str(interaction.user.id)]['banned_until'] < time.time():
                    #if is_player_gold_plus(unlq['players'][str(interaction.user.id)]['id']) or interaction.user.id in [301821822502961152, 300052305540153354]:
                    if True:
                        await interaction.response.send_message(view=RoleSelectView(self.queue), ephemeral=True)
                    else:
                        await interaction.response.send_message(f"You need to be ranked Gold 4 or above in Ranked Solo/Duo to play UNL Queue.", ephemeral=True)
                else:
                    banned_until = unlq['players'][str(interaction.user.id)]['banned_until']
                    value = datetime.datetime.fromtimestamp(banned_until, pytz.timezone('Europe/London'))
                    res = value.strftime('%d %B %I:%M %p')
                    await interaction.response.send_message(f"You are restricted from playing UNL Queue until {res} UK time.", ephemeral=True)
            else:
                await interaction.response.send_message(view=MatchmakingView(self.queue), ephemeral=True)
        else:
            await interaction.response.send_message("You need to link an account first! Try using **/link**", ephemeral=True)


    @app_commands.command(name="report", description="Enter this command to report a player")
    @app_commands.guilds(int(os.getenv("SERVER_ID")))
    async def report_player(self, interaction: discord.Interaction):
        await interaction.response.send_modal(Report(self._bot))
        
    @app_commands.command(name="me", description="Enter this command to view information about your UNL Queue profile")
    @app_commands.guilds(int(os.getenv("SERVER_ID")))
    async def me_command(self, interaction: discord.Interaction):
        with open('..\\unlqueue.xyz\\json\\leaderboard.json', 'r') as json_file:
            leaderboard = json.load(json_file)
        with open('C:\\DATA\\unlq.json', 'r') as json_file:
            unlq = json.load(json_file)
        index = 0
        
        un_points = 0
        for p in unlq['players']:
            if interaction.user.id == int(p):
                un_points = unlq['players'][p]['unp']
                break
        else:
            await interaction.response.send_message(content="Couldn't find your info, sorry <:Sadge:798976650926096395>", ephemeral=True)
        
        for p in leaderboard.keys():
            index += 1
            if interaction.user.id == int(p):
                me = ""
                me += f"**{interaction.user.name}**\n"
                me += f"IGN: {leaderboard[p]['name']}\n"
                me += f"Rank: {index}/{len(leaderboard.keys())}\n"
                me += f"LP: {leaderboard[p]['lp']}\n"
                me += f"Wins: {leaderboard[p]['wins']}\n"
                me += f"Losses: {leaderboard[p]['losses']}\n"
                me += f"UN Points: {int(un_points)}\n"
                
                await interaction.response.send_message(content=me, ephemeral=True)
                break
        
    @app_commands.command(name="link", description="Enter this command to link your EUW account")
    @app_commands.guilds(int(os.getenv("SERVER_ID")))
    async def link_account(self, interaction: discord.Interaction):
        await interaction.response.send_modal(LinkAccount())
        
    @app_commands.command(name="stats", description="Enter this command to see your UNL Queue stats")
    @app_commands.guilds(int(os.getenv("SERVER_ID")))
    async def stats(self, interaction: discord.Interaction):
        with open('C:\\DATA\\unlq.json', 'r') as json_file:
            unlq = json.load(json_file)
        for p in unlq['players']:
            if interaction.user.id == int(p):
                await interaction.response.send_message(content=get_stats(unlq['players'][p]['puuid']), ephemeral=True)
                break
        else:
            await interaction.response.send_message(content="Couldn't find your stats, sorry <:Sadge:798976650926096395>", ephemeral=True)

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
    async def add_fill(self, ctx: commands.context.Context, input: int):
            n = 0
            while n < input:
                if len(self.queue.players) < 10:
                    user = random.choice(self.queue.message.channel.guild.members)
                    with open('C:\\DATA\\unlq.json', 'r') as json_file:
                        unlq_json =  json.load(json_file)
                    if str(user.id) in unlq_json['players'].keys() and user.id not in [301821822502961152]:
                        player = Player(user.id, user.name, fill, user, False, "beddomu", unlq_json['players'][str(user.id)]['rating'])
                        if player not in self.queue.players:
                            self.queue.players.append(player)
                            n += 1
                else:
                    break
            else:
                await self.queue.update_lobby()
                
    @commands.command(name="debug", aliases=["c"])
    @commands.has_permissions(manage_messages=True)
    async def debug(self, ctx):
        self.queue.list_players()
        
    @commands.command(name="devmode", aliases=["dev"])
    @commands.has_permissions(manage_messages=True)
    async def dev(self, ctx):
        with open('C:\\DATA\\unlq.json', 'r') as file:
            unlq = json.load(file)
            
        unlq['dev_mode'] = True

        with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
            json.dump(unlq, unlq_file)
        guild = await self._bot.fetch_guild(int(os.getenv("SERVER_ID")))
        role = discord.utils.get(guild.roles, id = 676740137815900160)
        channel = await self._bot.fetch_channel(int(os.getenv("QUEUE")))
        await channel.set_permissions(role, read_messages=False)
        channel = await self._bot.fetch_channel(int(os.getenv("LIVE")))
        await channel.set_permissions(role, read_messages=False)
        self.queue.devmode = True
        
    @commands.command(name="public", aliases=["p"])
    @commands.has_permissions(manage_messages=True)
    async def public(self, ctx):
        with open('C:\\DATA\\unlq.json', 'r') as file:
            unlq = json.load(file)
            
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
        
    @app_commands.command(name="cash_out", description="Enter this command to convert all your UN points into LP")
    @app_commands.guilds(int(os.getenv("SERVER_ID")))
    async def cash_out(self, interaction: discord.Interaction):
        with open('C:\\DATA\\unlq.json', 'r') as json_file:
            unlq = json.load(json_file)
        for p in unlq['players']:
            if interaction.user.id == int(p):
                if unlq['players'][p]['unp'] > 500:
                    unlq['players'][p]['points'] += int(unlq['players'][p]['unp']/500)
                    await interaction.response.send_message(content=f"You exchanged {unlq['players'][p]['unp']} UN Points for {int(unlq['players'][p]['unp']/500)} LP.\nCurrent LP: {unlq['players'][p]['points']}", ephemeral=True)
                    unlq['players'][p]['unp'] = 0
                    break
                else:
                    await interaction.response.send_message("You don't have enough UN Points to exchange. Minimum required: 500")
        else:
            await interaction.response.send_message(content="Couldn't find your profile, sorry <:Sadge:798976650926096395>. Have you linked your account?", ephemeral=True)

        with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
            json.dump(unlq, unlq_file)
        
    @commands.command(name="leaderboard", aliases=["l"])
    @commands.has_permissions(manage_messages=True)
    async def leaderboard(self, ctx):
        update_games()
        await update_leaderboard()
        
    @commands.command(name="reset", aliases=["n"])
    @commands.has_permissions(manage_messages=True)
    async def newlobbymessage(self, ctx: commands.context.Context):
        self.queue.locked = False
        await self.queue.reset_lobby()

    @commands.command(name="delete", aliases=["d"])
    @commands.has_permissions(manage_messages=True)
    async def delete_lobby(self, ctx: commands.context.Context, lobby_id):
        guild = ctx.guild
        with open('C:\\DATA\\unlq.json', 'r') as unlq_file:
            unlq_json = json.load(unlq_file)
        try:
            game_category = discord.utils.get(
                guild.categories, name=lobby_id)
        except:
            print("Game category doesn't exist")
        queue_voice = discord.utils.get(guild.voice_channels, id=959880784116854794)
        for channel in game_category.voice_channels:
            for member in channel.members:
                try:
                    await member.move_to(queue_voice)
                except:
                    print(
                        f'{member.name} is not in the queue voice channel.')
            try:
                await channel.delete()
            except:
                print("Voice channel doesn't exist")
        try:
            await game_category.delete()
        except:
            print("Game category doesn't exist")
        del unlq_json['lobbies'][str(lobby_id)]
        with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
            json.dump(unlq_json, unlq_file)
            unlq_file.close()
    
    @commands.command(name="ban", aliases=["b"])
    @commands.has_permissions(manage_messages=True)
    async def ban_player(self, ctx, member: discord.Member, seconds):
        ban(member.id, seconds)
    
    @commands.command(name="unban", aliases=["ub"])
    @commands.has_permissions(manage_messages=True)
    async def unban_player(self, ctx, member: discord.Member):
        unban(member.id)
    
    @commands.command(name="unban_all", aliases=["uba"])
    @commands.has_permissions(manage_messages=True)
    async def unban_all(self, ctx):
        with open('C:\\DATA\\unlq.json', 'r') as file:
            unlq = json.load(file)
            
        for p in unlq['players']:
            unlq['players'][p]['banned_until'] = 0
                
        with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
            json.dump(unlq, unlq_file)
            
    @commands.command(name="add_points", aliases=["ap"])
    @commands.has_permissions(manage_messages=True)
    async def unban_player(self, ctx, member: discord.Member, points):
        with open('C:\\DATA\\unlq.json', 'r') as file:
            unlq = json.load(file)
        unlq['players'][str(member.id)]['unp'] += int(points)
        with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
            json.dump(unlq, unlq_file)
            
    @commands.command(name="remove_points", aliases=["subtract_points, rp, sp"])
    @commands.has_permissions(manage_messages=True)
    async def unban_player(self, ctx, member: discord.Member, points):
        with open('C:\\DATA\\unlq.json', 'r') as file:
            unlq = json.load(file)
        unlq['players'][str(member.id)]['unp'] -= int(points)
        with open('C:\\DATA\\unlq.json', 'w') as unlq_file:
            json.dump(unlq, unlq_file)   
            
            
    
        



async def setup(bot: commands.Bot):
    await bot.add_cog(UNLQueue(bot))