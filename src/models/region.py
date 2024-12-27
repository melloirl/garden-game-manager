from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.race import Race


class RaceRegionLink(SQLModel, table=True):
    race_id: Optional[int] = Field(foreign_key="race.id", primary_key=True)
    region_id: Optional[int] = Field(foreign_key="region.id", primary_key=True)


class Region(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    icon_url: str

    races: list["Race"] = Relationship(  # type: ignore
        back_populates="regions", link_model=RaceRegionLink
    )
