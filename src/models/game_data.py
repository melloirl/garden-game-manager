from typing import List, Optional

from pydantic import BaseModel

from models.arcana import Arcana, ArcanaSkill, ArcanaTier
from models.character import Character
from models.gacha import GachaConfig
from repositories.arcana_repository import (
    get_arcana_skills,
    get_arcana_tiers,
    get_arcanas,
)
from repositories.character_repository import get_characters
from repositories.gacha_repository import get_gacha_config


class GameData(BaseModel):
    arcana_skills: List[ArcanaSkill] = []
    arcana_tiers: List[ArcanaTier] = []
    arcana: List[Arcana] = []
    characters: List[Character] = []
    gacha_config: Optional[GachaConfig] = None

    def __init__(self, *args, **kwargs):
        # Initialize with default empty values first
        super().__init__(*args, **kwargs)
        # Then load the actual data
        self.reload()

    def reload(self) -> None:
        """Reloads all game data from the database."""
        self.arcana_skills = get_arcana_skills()
        self.arcana_tiers = get_arcana_tiers()
        self.arcana = get_arcanas()
        self.characters = get_characters()
        self.gacha_config = get_gacha_config()
