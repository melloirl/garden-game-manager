from datetime import datetime
from typing import Optional

from sqlmodel import BigInteger, Field, Relationship, SQLModel, Text

from models.mana import ManaNature
from models.race import Race
from models.region import Region
from models.user import User


class Character(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)

    # Basic Profile
    name: str
    age: int
    title: Optional[str] = Field(default=None)  # e.g. "The Brave", can be null
    level: int = Field(default=1)  # min level = 1 (optionally add a validator)
    xp_points: int = Field(default=0)
    story: Optional[str] = Field(
        default=None, sa_type=Text
    )  # long text about background
    description: Optional[str] = Field(default=None, sa_type=Text)
    image_url: Optional[str] = Field(default=None)
    coins: int = Field(default=0)

    # Arcana Skills bitfield (store which arcana skills are unlocked)
    arcana_skills: int = Field(default=0, sa_type=BigInteger)

    # Attribute Points
    vitality: int = Field(default=0)
    dexterity: int = Field(default=0)
    intelligence: int = Field(default=0)
    strength: int = Field(default=0)
    resistance: int = Field(default=0)
    mana: int = Field(default=0)

    # Foreign Keys
    user_id: int = Field(foreign_key="user.id")
    region_id: Optional[int] = Field(default=None, foreign_key="region.id")
    race_id: Optional[int] = Field(default=None, foreign_key="race.id")
    mana_nature_id: Optional[int] = Field(default=None, foreign_key="mananature.id")

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Character Points
    current_hp: int = Field(default=0)
    current_mp: int = Field(default=0)

    # Relationships
    user: "User" = Relationship(
        back_populates="characters",
        sa_relationship_kwargs={"foreign_keys": "[Character.user_id]"},
    )
    region: Optional["Region"] = Relationship()
    race: Optional["Race"] = Relationship()
    mana_nature: Optional["ManaNature"] = Relationship()
