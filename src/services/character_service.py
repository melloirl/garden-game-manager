import math

from models.character import Character

CHARACTER_LEVEL_POINTS = {
    1: 5,
    2: 6,
    3: 8,
    4: 10,
    5: 13,
    6: 16,
    7: 20,
    8: 24,
    9: 28,
    10: 28,
}


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


def calculate_character_xp_to_next_level(character: Character) -> int:
    """
    Calculate the XP required to reach the next level.
    """
    return 100 * character.level if character.level < 10 else 0


def calculate_character_remaining_points(character: Character) -> int:
    """
    Calculate the remaining points for a character to spend on attributes.
    """
    # First, we need to calculate the total points for the current level
    total_points = CHARACTER_LEVEL_POINTS.get(character.level, 28)

    # Then, we need to subtract the points already spent
    return total_points - sum(
        [
            character.vitality,
            character.dexterity,
            character.intelligence,
            character.strength,
            character.resistance,
            character.mana,
        ]
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
    xp_to_next_level = calculate_character_xp_to_next_level(character)
    if character.xp_points >= xp_to_next_level:
        character.level += 1
        character.xp_points = abs(character.xp_points - xp_to_next_level)
    else:
        raise ValueError("Character does not have enough XP to level up")

    return character
