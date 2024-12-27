from models.character import Character
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from config.database import engine
from typing import List
import math


def get_characters() -> List[Character]:
    """
    Get all characters
    """
    with Session(engine) as session:
        statement = select(Character)
        return session.exec(statement).all()


def get_character_by_player_id(user_id: int) -> Character:
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


def update_character_arcana_skills(character_id: int, skill_ids: list[int]):
    with Session(engine) as session:
        statement = select(Character).where(Character.id == character_id)
        character = session.exec(statement).first()
        if character:
            character.arcana_skills = skill_ids
            session.add(character)
            session.commit()
            session.refresh(character)
            return character.arcana_skills


def calculate_character_max_hp(character: Character) -> int:
    character_hp_rate = 0.08 if character.vitality == 0 else character.vitality / 40
    return math.ceil(
        character.race.base_hp
        + (character.race.hp_per_level * character.level)
        * (1 + character_hp_rate * character.vitality)
    )


def calculate_character_max_mp(character: Character) -> int:
    character_mp_rate = 0.08 if character.mana == 0 else character.mana / 8
    return math.ceil(
        character.race.base_mp
        + (character.race.mp_per_level * character_mp_rate) * character.mana
    )


def calculate_character_ad_modifier(character: Character) -> int:
    return 1 + (1 / 10) * character.level + (1 / 8) * character.strength


def calculate_character_ap_modifier(character: Character) -> int:
    return 1 + (1 / 10) * character.level + (2 / 8) * character.intelligence


def calculate_character_damage_reduction(character: Character) -> int:
    return (character.level + character.resistance) / 100


def calculate_character_actions_per_turn(character: Character) -> int:
    return math.ceil(
        (
            character.race.base_speed
            + (character.dexterity + character.race.speed_per_level) / 100
        )
        / 2
    )


def restore_character(character: Character) -> Character:
    character.current_hp = calculate_character_max_hp(character)
    character.current_mp = calculate_character_max_mp(character)

    return character


def level_up_character(character: Character) -> Character:
    character.level += 1
    character.remaining_points = 10
    return character
