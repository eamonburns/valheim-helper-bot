from datetime import datetime

import requests

import discord
from discord import app_commands


class ServerStatus:
    last_status_update: datetime
    error: str | None
    server_name: str | None
    server_type: str | None
    platform: str | None
    player_count: int | None
    password_protected: bool | None
    vac_enabled: bool | None
    port: int | None
    steam_id: int | None
    keywords: str | None
    game_id: int | None
    players: list[dict] | None

    def __init__(self, dct: dict) -> None:
        self.last_status_update = datetime.fromisoformat(
            dct["last_status_update"],
        )
        self.error = dct.get("error")
        self.server_name = dct.get("server_name")
        self.server_type = dct.get("server_type")
        self.platform = dct.get("platform")
        self.player_count = dct.get("player_count")
        self.password_protected = dct.get("password_protected")
        self.vac_enabled = dct.get("vac_enabled")
        self.port = dct.get("port")
        self.steam_id = dct.get("steam_id")
        self.keywords = dct.get("keywords")
        self.game_id = dct.get("game_id")
        self.players = dct.get("players")


def init_client(guild_id: int, status_host: str, status_port: int) -> discord.Client:
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

    @tree.command(
        name="status",
        description="Get the status of the Valheim server.",
        guild=discord.Object(id=guild_id),
    )
    async def status(interaction: discord.Interaction):
        r = requests.get(f"http://{status_host}:{status_port}/status.json")

        status = ServerStatus(r.json())
        last_update = status.last_status_update.astimezone()
        last_update_str = f"{last_update.month}/{last_update.day}/{last_update.year} {last_update.hour}:{last_update.minute}:{last_update.second}"

        print(status)
        if status.error is not None:
            # Convert to local time
            await interaction.response.send_message(
                "Server status can't be retrieved. " +
                f"Last update: {last_update_str}",
            )
            return

        await interaction.response.send_message(
            f'# "{status.server_name}" Status:\n' +
            f'_(Last update at {last_update_str})_\n' +
            f"- Player Count: {status.player_count}\n",
        )

    @client.event
    async def on_ready():
        await tree.sync(guild=discord.Object(id=guild_id))
        print(f"We have logged in as {client.user}")

    return client
