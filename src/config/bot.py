from typing import TypeVar

from discord.ext import commands

from models.game_data import GameData
from utils.logger import BotLogger

BotT = TypeVar("BotT", bound="GardenBot")


class GardenBot(commands.Bot):
    """Type definitions for the Garden Game Manager bot"""

    game_data: GameData
    logger: BotLogger

    def reload_game_data(self) -> None:
        """Reloads all game data from the database."""
        ...
