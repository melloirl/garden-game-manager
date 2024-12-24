from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

from .user import User

# Character Attributes include:
# - Name : The character's name
# - Age : The character's age
# - Origin Region ID : The character's origin region ID
# - Race ID : The character's race ID
# - Mana Nature ID : The character's mana nature ID
# - Optional Title : The character's optional title
# - Level (1-10) : The character's level
# - XP Points : The character's total XP points
# - Story : The character's background story
# - Description : The character's description
# - Image URL : The character's image URL
# - Enabled arcana skills : we'll go with a bitfield for this for easily setting and checking which arcanas skills are enabled

# Character Attributes include:
# - Vitality
# - Dexterity
# - Intelligence
# - Strength
# - Resistance
# - Mana
# Remaining Points

# Furhtermore, the character will have a list of skills, but this is for future development

class Character(SQLModel, table=True):
  id: int = Field(default=None, primary_key=True)
  name: str
  age: int
  title: str = Field(default=None) # Nullable
  level: int = Field(default=1) # Minimum level is 1
  xp_points: int = Field(default=0)
  description: str
  created_at: datetime = Field(default=datetime.now())
  updated_at: datetime = Field(default=datetime.now())

  # Every character belongs to one user, and every user can have many characters
  user_id: int = Field(foreign_key="user.id")
  user: User = Relationship(back_populates="characters")
