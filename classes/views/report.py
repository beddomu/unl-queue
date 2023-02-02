import discord
from discord.ext import commands

class Report(discord.ui.Modal):
    def __init__(self, bot: commands.Bot, title = 'Report a player', timeout = 300, custom_id = "report"):
        super().__init__(timeout = timeout, custom_id = custom_id, title=title)
        self.bot = bot

    name = discord.ui.TextInput(
        label="Player you're reporting",
        placeholder="Summoner or Discord name"
    )

    feedback = discord.ui.TextInput(
        label='Description',
        style=discord.TextStyle.long,
        placeholder='Enter a detailed description of the issue, including game/lobby IDs of games involved...',
        required=True,
        max_length=600,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your feedback, {interaction.user.display_name}!', ephemeral=True)
        embed = discord.Embed(title="Champions Queue player report")
        embed.add_field(name = "----------------------------------", value = f'**{self.name.value}**' + "\n\n" + self.feedback.value)
        embed.set_author(name = self.bot.user.name, icon_url= self.bot.user.avatar.url)
        embed.set_footer(text = f"From: {interaction.user.name}")
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/76/76402.png")
        moderator = await self.bot.fetch_user(301821822502961152)
        await moderator.send(embed=embed)

    async def on_error(self, error: Exception, interaction: discord.Interaction) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

