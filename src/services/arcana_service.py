from typing import Union

from models.arcana import ArcanaSkillEnum


def resolve_arcana_skill_mask(skill: Union[int, ArcanaSkillEnum]) -> int:
    """
    If skill is an ArcanaSkill, return its bitmask.
    If skill is an int, treat that int as the exponent.
    """
    if isinstance(skill, ArcanaSkillEnum):
        return skill.value
    return 1 << skill


def has_arcana_skill(bitfield: int, skill: Union[int, ArcanaSkillEnum]) -> bool:
    """
    Check if the specified bit is set in bitfield.
    """
    mask = resolve_arcana_skill_mask(skill)
    return (bitfield & mask) != 0


def add_arcana_skill(bitfield: int, skill: Union[int, ArcanaSkillEnum]) -> int:
    """
    Set the specified bit in bitfield.
    """
    mask = resolve_arcana_skill_mask(skill)
    return bitfield | mask


def remove_arcana_skill(bitfield: int, skill: Union[int, ArcanaSkillEnum]) -> int:
    """
    Clear the specified bit in bitfield.
    """
    mask = resolve_arcana_skill_mask(skill)
    return bitfield & ~mask


def get_arcana_skills(bitfield: int) -> list[ArcanaSkillEnum]:
    """
    Return a list of ArcanaSkill members set in the bitfield.
    """
    return [skill for skill in ArcanaSkillEnum if (bitfield & skill.value) != 0]


def get_arcana_skill_ids(bitfield: int) -> list[int]:
    """
    Returns the *exponents* (0 through 53) of the bits that are set in 'bitfield'.
    """
    return [i for i in range(54) if (bitfield & (1 << i)) != 0]
