import discord
import os
import asyncio
from discord.ext import commands
from utils.load_env import load_env
from utils.logger import BotLogger
from config.database import init_db
from services.arcana_service import get_arcana_skills, get_arcana_tiers, get_arcanas

load_env()

# Environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_GUILD_ID = os.getenv("DISCORD_GUILD_ID")
PREFIX = os.getenv("BOT_PREFIX")

if not DISCORD_TOKEN or not DISCORD_GUILD_ID or not PREFIX:
    raise ValueError("Missing environment variables. Check your .env file.")

# Initialize a global logger for the bot
logger = BotLogger("discord")


def get_prefix(bot, message):
    prefixes = [PREFIX]
    return commands.when_mentioned_or(*prefixes)(bot, message)


class GardenBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        # Set up intents as before
        intents = discord.Intents.all()

        # Initialize database and load arcana skills synchronously before bot setup
        init_db()
        self.arcana_skills = get_arcana_skills()
        self.arcana_tiers = get_arcana_tiers()
        self.arcanas = get_arcanas()

        super().__init__(*args, command_prefix=get_prefix, intents=intents, **kwargs)
        self.logger = logger

    async def setup_hook(self):
        self.logger.info("Starting bot setup...")

        # Load extensions first so that slash commands are registered with bot.tree
        self.logger.info("Beginning extension loading process...")
        await self.load_extensions()
        self.logger.info("Extensions loaded successfully")

        guild_obj = discord.Object(id=DISCORD_GUILD_ID)
        self.logger.info(f"Copying global commands to guild {DISCORD_GUILD_ID}")
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
    bot = GardenBot(description="Garden Game Manager")
    async with bot:
        await bot.start(DISCORD_TOKEN, reconnect=True)


if __name__ == "__main__":
    asyncio.run(main())
