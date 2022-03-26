import discord

class Report(discord.ui.Modal, title='Report a player'):
    # Our modal classes MUST subclass `discord.ui.Modal`,
    # but the title can be whatever you want.

    # This will be a short input, where the user can enter their name
    # It will also have a placeholder, as denoted by the `placeholder` kwarg.
    # By default, it is required and is a short-style input which is exactly
    # what we want.
    name = discord.ui.TextInput(
        label='Summary',
        placeholder='Enter a short description of the issue...',
    )

    # This is a longer, paragraph style input, where user can submit feedback
    # Unlike the name, it is not required. If filled out, however, it will
    # only accept a maximum of 300 characters, as denoted by the
    # `max_length=300` kwarg.
    feedback = discord.ui.TextInput(
        label='Description',
        style=discord.TextStyle.long,
        placeholder='Give a detailed description of the issue...',
        required=True,
        max_length=300,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your feedback, {self.name.value}!', ephemeral=True)

    async def on_error(self, error: Exception, interaction: discord.Interaction) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_tb(error.__traceback__)