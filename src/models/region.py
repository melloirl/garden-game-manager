from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class RaceRegionLink(SQLModel, table=True):
    race_id: Optional[int] = Field(foreign_key="race.id", primary_key=True)
    region_id: Optional[int] = Field(foreign_key="region.id", primary_key=True)

class Region(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    icon_url: str

    races: list["Race"] = Relationship( # type: ignore
        back_populates="regions",
        link_model=RaceRegionLink
    )