import logging
import os
from typing import TypeVar

from dotenv import load_dotenv
import discord

import bot

logger = logging.getLogger("valheim."+__name__)

T = TypeVar("T")


def _get_env(t: T, name: str) -> T | None:
    val_str = os.environ.get(name)
    if val_str is None:
        return None

    try:
        val = t(val_str)
        return val
    except ValueError as e:
        logger.error(e)
        return None


if __name__ == "__main__":
    discord.utils.setup_logging(formatter=logging.Formatter(
        "%(asctime)s.%(msecs)03d %(levelname)s %(name)s - %(funcName)s: %(message)s",
        "%Y-%m-%d %H:%M:%S",
    ), level=logging.INFO)  # Default to INFO log level

    # Set my loggers to DEBUG level
    logging.getLogger("valheim").setLevel(logging.DEBUG)

    logger.info("Starting Discord bot")

    # Get configuration from environment
    load_dotenv()

    BOT_TOKEN = _get_env(str, "DISCORD_TOKEN")
    if BOT_TOKEN is None:
        logger.error("`DISCORD_TOKEN` must be defined")
        exit(1)

    GUILD_ID = _get_env(int, "DISCORD_GUILD")
    if GUILD_ID is None:
        logger.error("`DISCORD_GUILD` must be defined")
        exit(1)

    STATUS_HOST = _get_env(str, "STATUS_HTTP_HOST")
    if STATUS_HOST is None:
        logger.error("`STATUS_HTTP_HOST` must be defined")
        exit(1)

    STATUS_PORT = _get_env(int, "STATUS_HTTP_PORT")
    if STATUS_PORT is None:
        logger.error("`STATUS_HTTP_PORT` must be defined")
        exit(1)

    logger.info("Loaded configuration")

    # Create and run the client
    client = bot.init_client(GUILD_ID, STATUS_HOST, STATUS_PORT)

    logger.info("Running bot")
    client.run(BOT_TOKEN, log_handler=None)
