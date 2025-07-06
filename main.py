import os
from typing import TypeVar

from dotenv import load_dotenv

import bot

T = TypeVar("T")


def _get_env(t: T, name: str) -> T | None:
    val_str = os.environ.get(name)
    if val_str is None:
        return None

    try:
        val = t(val_str)
        return val
    except ValueError as e:
        print(e)
        return None


if __name__ == "__main__":
    # Get configuration from environment
    load_dotenv()

    BOT_TOKEN = _get_env(str, "DISCORD_TOKEN")
    if BOT_TOKEN is None:
        print("Error: `DISCORD_TOKEN` must be defined")
        exit(1)

    GUILD_ID = _get_env(int, "DISCORD_GUILD")
    if GUILD_ID is None:
        print("Error: `DISCORD_GUILD` must be defined")
        exit(1)

    # Create and run the client
    client = bot.init_client(GUILD_ID)

    client.run(BOT_TOKEN)
