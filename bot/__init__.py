import discord
from discord import app_commands


def init_client(guild_id: int) -> discord.Client:
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    tree = app_commands.CommandTree(client)

    @tree.command(
        name="hello",
        description="A greeting",
        guild=discord.Object(id=guild_id),
    )
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message("Hello!")

    @client.event
    async def on_ready():
        await tree.sync(guild=discord.Object(id=guild_id))
        print(f"We have logged in as {client.user}")

    return client
