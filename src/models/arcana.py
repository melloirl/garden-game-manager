from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional


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
