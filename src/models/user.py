from typing import Optional, List
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
    
    active_character: Optional["Character"] = Relationship( #type: ignore
        sa_relationship_kwargs={"foreign_keys": "[User.active_character_id]"}
    )

    characters: List["Character"] = Relationship( #type: ignore
        back_populates="user",
        sa_relationship_kwargs={
            "primaryjoin": "User.id==Character.user_id",
            "foreign_keys": "[Character.user_id]"
        }
    )
