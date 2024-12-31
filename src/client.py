import asyncio
import os

import discord
from discord.ext import commands

from config.bot import GardenBot as GardenBotBase
from config.database import init_db
from models.game_data import GameData
from utils.load_env import check_required_env, load_env
from utils.logger import BotLogger


def get_prefix(bot, message):
    """
    Dynamically determine the bot's prefix.
    You can still load from environment at runtime.
    """
    prefixes = [os.getenv("BOT_PREFIX")]
    return commands.when_mentioned_or(*prefixes)(bot, message)


class GardenBot(GardenBotBase):
    """
    The main bot class, responsible for initialization and loading game data.
    """

    def __init__(self, *args, **kwargs):
        # For simplicity, we use all intents. Could be refined later.
        intents = discord.Intents.all()
        # Initialize the database
        init_db()
        # Load the game data
        self.game_data = GameData()

        # Initialize the bot with prefix + intents
        super().__init__(*args, command_prefix=get_prefix, intents=intents, **kwargs)

        # Use the custom bot logger
        self.logger = BotLogger("discord")

    async def setup_hook(self):
        self.logger.info("Starting bot setup...")

        # Load cogs/extensions so slash commands are registered
        self.logger.info("Beginning extension loading process...")
        await self.load_extensions()
        self.logger.info("Extensions loaded successfully")

        guild_id = os.getenv("DISCORD_GUILD_ID")
        guild_obj = discord.Object(id=guild_id)
        self.logger.info(f"Copying global commands to guild {guild_id}")
        self.tree.copy_global_to(guild=guild_obj)

        try:
            self.logger.info("Syncing command tree with Discord...")
            await self.tree.sync(guild=guild_obj)
            self.logger.info("Command tree sync completed successfully")
        except Exception as e:
            self.logger.error(f"Failed to sync command tree: {e}")
            raise

    async def load_extensions(self):
        """Load all cogs/extensions from the cogs directory."""
        for filename in os.listdir("./src/cogs"):
            if filename.endswith(".py"):
                ext_name = f"cogs.{filename[:-3]}"
                try:
                    await self.load_extension(ext_name)
                    self.logger.info(f"Loaded extension '{ext_name}' successfully.")
                except Exception as e:
                    self.logger.error(f"Failed to load extension '{ext_name}': {e}")

    async def on_ready(self):
        self.logger.info(f"Logged in as: {self.user.name} - {self.user.id}")
        self.logger.info(f"Discord.py Version: {discord.__version__}")
        game = discord.Game("feitiços elementais!")
        await self.change_presence(status=discord.Status.online, activity=game)
        self.logger.info("Bot is online and ready!")

    def reload_game_data(self):
        self.game_data.reload()


async def main():
    # 1) Load from .env files only if system env vars are not already set
    load_env()
    # 2) Ensure the required environment variables are present
    check_required_env()

    # 3) Create the bot and start it
    bot = GardenBot(description="Garden Game Manager")
    async with bot:
        await bot.start(os.getenv("DISCORD_TOKEN"), reconnect=True)


if __name__ == "__main__":
    asyncio.run(main())
