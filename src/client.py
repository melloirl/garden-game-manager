import discord
import os
import asyncio
from discord.ext import commands
from utils.load_env import load_env
from utils.logger import BotLogger
from config.database import init_db
from services.arcana_service import get_arcana_skills, get_arcana_tiers, get_arcanas

load_env()

def check_required_env():
    """Raise an error if required vars aren't set."""
    required_vars = ["DISCORD_TOKEN", "DISCORD_GUILD_ID", "BOT_PREFIX"]
    missing = [v for v in required_vars if not os.getenv(v)]
    if missing:
        raise ValueError(f"Missing env vars: {', '.join(missing)}")

logger = BotLogger("discord")


def get_prefix(bot, message):
    prefixes = [os.getenv("BOT_PREFIX")]
    return commands.when_mentioned_or(*prefixes)(bot, message)


def load_game_data():
    """Loads the immutable game data from the database."""
    # We start by initializing the database. This will ensure that the tables are created.
    init_db()

    # Then we load the arcana skills, tiers and arcana.
    arcana_skills = get_arcana_skills()
    arcana_tiers = get_arcana_tiers()
    arcana = get_arcanas()

    return arcana_skills, arcana_tiers, arcana


class GardenBot(commands.Bot):
    """
    The main bot class.

    This class is responsible for initializing the bot and loading the game data.

    """

    def __init__(self, *args, **kwargs):
        # For simplicity, we use all intents. Could be refined later.
        intents = discord.Intents.all()

        # Initialize database and load arcana skills synchronously before bot setup
        self.arcana_skills, self.arcana_tiers, self.arcanas = load_game_data()

        # Initialize the bot with the command prefix and intents.
        super().__init__(*args, command_prefix=get_prefix, intents=intents, **kwargs)

        # Initialize the logger.
        self.logger = logger

    async def setup_hook(self):
        self.logger.info("Starting bot setup...")

        # Load extensions first so that slash commands are registered with bot.tree
        self.logger.info("Beginning extension loading process...")
        await self.load_extensions()
        self.logger.info("Extensions loaded successfully")

        guild_obj = discord.Object(id=os.getenv("DISCORD_GUILD_ID"))
        self.logger.info(f"Copying global commands to guild {os.getenv('DISCORD_GUILD_ID')}")
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


async def main():
    check_required_env()
    bot = GardenBot(description="Garden Game Manager")
    async with bot:
        await bot.start(os.getenv("DISCORD_TOKEN"), reconnect=True)


if __name__ == "__main__":
    asyncio.run(main())
