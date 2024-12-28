from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class GachaConfig(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    enabled: bool  # If the Gacha system is enabled
    general_pick_price: int  # Price for a general pick (Pick from any arcana tree)
    choice_pick_price: (
        int  # Price for a choice pick (Pick within a specific arcana tree)
    )
    pity_threshold: int  # Pity threshold for the Gacha system (how many picks until a 5* is guaranteed)
    pity_enabled: bool  # If the pity system is enabled


class GachaResult(BaseModel):
    name: str
    tier_level: int
    tier_name: str
    chance: float
    skill_id: int
