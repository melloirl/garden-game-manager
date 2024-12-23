from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    discord_id: str = Field(index=True, unique=True)
    player_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_active: datetime = Field(default_factory=datetime.utcnow)
    gacha_count: int = Field(default=0)
    active_character_id: Optional[int] = Field(default=None, foreign_key="character.id")
    active_character: Optional["Character"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[User.active_character_id]"}
    )

    # Use a string annotation for the list of Character
    characters: List["Character"] = Relationship(back_populates="user")
