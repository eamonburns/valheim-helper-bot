import os

from dotenv import load_dotenv

import bot


if __name__ == "__main__":
    # Get configuration from environment
    load_dotenv()

    BOT_TOKEN = os.environ.get("DISCORD_TOKEN")
    if BOT_TOKEN is None:
        print("Error: `BOT_TOKEN` must be defined")
        exit(1)

    bot.client.run(BOT_TOKEN)
