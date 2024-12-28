import enum
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Arcana(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    icon_url: str

    # Relationship
    skills: List["ArcanaSkill"] = Relationship(back_populates="arcana")


class ArcanaTier(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tier_name: str
    tier_level: int
    probability: float
    color: str

    # Relationship
    skills: List["ArcanaSkill"] = Relationship(back_populates="tier")


class ArcanaSkill(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str

    # Foreign keys
    arcana_id: Optional[int] = Field(default=None, foreign_key="arcana.id")
    tier_id: Optional[int] = Field(default=None, foreign_key="arcanatier.id")

    # Relationships
    arcana: Arcana = Relationship(back_populates="skills")
    tier: ArcanaTier = Relationship(back_populates="skills")


class ArcanaSkillEnum(enum.IntFlag):
    """
    Arcana skill bitfield.
    Each skill is a power of 2 to allow bitwise operations.
    """

    MAGICLESS = 1 << 0
    PROJECTILE = 1 << 1
    PRESSURE = 1 << 2
    EXPLOSION = 1 << 3
    PENETRATION = 1 << 4
    IGNITION = 1 << 5
    CORROSION = 1 << 6
    TRUE_DAMAGE = 1 << 7
    DISRUPTION = 1 << 8
    DESINTEGRATION = 1 << 9
    PRIMARY = 1 << 10
    AREA = 1 << 11
    VINCULATION = 1 << 12
    COMPOSITE = 1 << 13
    ENHANCEMENT = 1 << 14
    REPRODUCTION = 1 << 15
    EVOLUTION = 1 << 16
    ANIMATION = 1 << 17
    COMPLEX = 1 << 18
    RESISTANCE = 1 << 19
    BARRIER = 1 << 20
    ELASTICITY = 1 << 21
    EXPANSION = 1 << 22
    IMMUNITY = 1 << 23
    ABSORPTION = 1 << 24
    PROTECTION = 1 << 25
    DETECTION = 1 << 26
    MAPPING = 1 << 27
    CLARVOYANCE = 1 << 28
    COMMUNICATION = 1 << 29
    EXPANDED_PERCEPTION = 1 << 30
    READING = 1 << 31
    CONVERSION = 1 << 32
    ADAPTATION = 1 << 33
    REDUCTION = 1 << 34
    RESTAURATION = 1 << 35
    METAMORPHOSIS = 1 << 36
    TRANSMUTATION = 1 << 37
    COMPULSION = 1 << 38
    PHYSICAL_RESTRICTION = 1 << 39
    INHIBITION = 1 << 40
    MAGIC_RESTRICTION = 1 << 41
    TIME_SEAL = 1 << 42
    MINOR_HEALING = 1 << 43
    REANIMATION = 1 << 44
    PURIFICATION = 1 << 45
    GENERAL_HEALING = 1 << 46
    REGENERATION = 1 << 47
    MIRACLE = 1 << 48
    TRANSPOSITION = 1 << 49
    SWAPPING = 1 << 50
    PORTAL = 1 << 51
    GROUP_TELEPORTATION = 1 << 52
    LONG_DISTANCE_TELEPORTATION = 1 << 53
