from sqlmodel import SQLModel, Field, Relationship, Text
from datetime import datetime
from typing import List
from models.region import Region, RaceRegionLink

class Race(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    
    # HP
    base_hp: float = Field(nullable=False)
    hp_per_level: float = Field(nullable=False)
    
    # MP
    base_mp: float = Field(nullable=False)
    mp_per_level: float = Field(nullable=False)
    
    # Resistance
    base_resistance: float = Field(nullable=False)
    
    # Strength
    base_strength: float = Field(nullable=False)
    strength_per_level: float = Field(nullable=False)
    
    # Speed
    base_speed: float = Field(nullable=False)
    speed_per_level: float = Field(nullable=False)
    
    # Description (should be an actual text field)
    description: str = Field(nullable=False, sa_type=Text)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    regions: List[Region] = Relationship(
        back_populates="races",
        link_model=RaceRegionLink
    )
