from typing import List, Optional

from sqlalchemy.orm import joinedload
from sqlmodel import Session, select

from config.database import engine
from models.character import Character


def get_characters() -> List[Character]:
    """
    Get all characters
    """
    with Session(engine) as session:
        statement = select(Character)
        return session.exec(statement).all()


def get_character_by_id(character_id: int) -> Optional[Character]:
    """
    Get a character by id
    """
    with Session(engine) as session:
        statement = select(Character).where(Character.id == character_id)
        return session.exec(statement).first()


def get_character_by_player_id(user_id: int) -> Optional[Character]:
    """
    Get a character by player id with all relationships loaded
    """
    with Session(engine) as session:
        statement = (
            select(Character)
            .options(
                joinedload(Character.race),
                joinedload(Character.region),
                joinedload(Character.mana_nature),
            )
            .where(Character.user_id == user_id)
        )
        return session.exec(statement).first()


def update_character(character: Character) -> Character:
    """
    Update a character based on its updated model
    """
    with Session(engine) as session:
        session.add(character)
        session.commit()
        session.refresh(character)
        return character


def update_character_arcana_skills(
    character_id: int, skill_ids: list[int]
) -> Optional[list[int]]:
    """
    Update the arcana_skills field of a character
    """
    with Session(engine) as session:
        statement = select(Character).where(Character.id == character_id)
        character = session.exec(statement).first()
        if character:
            character.arcana_skills = skill_ids
            session.add(character)
            session.commit()
            session.refresh(character)
            return character.arcana_skills

    return None
