import math

from models.character import Character


def calculate_character_max_hp(character: Character) -> int:
    """
    Calculate the max HP for a character based on race stats, level, and vitality.
    """
    character_hp_rate = 0.08 if character.vitality == 0 else character.vitality / 40
    return math.ceil(
        character.race.base_hp
        + (character.race.hp_per_level * character.level)
        * (1 + character_hp_rate * character.vitality)
    )


def calculate_character_max_mp(character: Character) -> int:
    """
    Calculate the max MP for a character based on race stats, level, and mana.
    """
    character_mp_rate = 0.08 if character.mana == 0 else character.mana / 8
    return math.ceil(
        character.race.base_mp
        + (character.race.mp_per_level * character_mp_rate) * character.mana
    )


def calculate_character_ad_modifier(character: Character) -> float:
    """
    Calculate AD (attack damage) modifier.
    """
    return 1 + (1 / 10) * character.level + (1 / 8) * character.strength


def calculate_character_ap_modifier(character: Character) -> float:
    """
    Calculate AP (ability power) modifier.
    """
    return 1 + (1 / 10) * character.level + (2 / 8) * character.intelligence


def calculate_character_damage_reduction(character: Character) -> float:
    """
    Calculate damage reduction based on level and resistance.
    """
    return (character.level + character.resistance) / 100


def calculate_character_actions_per_turn(character: Character) -> int:
    """
    Calculate how many actions per turn a character can make.
    """
    return math.ceil(
        (
            character.race.base_speed
            + (character.dexterity + character.race.speed_per_level) / 100
        )
        / 2
    )


def restore_character(character: Character) -> Character:
    """
    Restore character HP/MP to their max values.
    """
    character.current_hp = calculate_character_max_hp(character)
    character.current_mp = calculate_character_max_mp(character)
    return character


def level_up_character(character: Character) -> Character:
    """
    Increase character level by 1 and reset remaining points, etc.
    """
    character.level += 1
    character.remaining_points = 10
    return character
