import random
from typing import Dict, List, Union

from models.arcana import Arcana, ArcanaSkill, ArcanaSkillEnum, ArcanaTier


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


def create_arcana_data(
    arcana_list: List[Arcana],
    arcana_skills_list: List[ArcanaSkill],
    arcana_tiers_list: List[ArcanaTier],
) -> Dict:
    """
    Given lists of Arcana, ArcanaSkill, and ArcanaTier,
    returns a dictionary of pre-processed data (arcana_name_map, skill_details_map, etc.)
    for easy usage throughout the application.
    """
    # 1) Map arcana name -> arcana object
    arcana_name_map = {arc.name.lower(): arc for arc in arcana_list}

    # 2) Map skill name -> skill object
    skill_details_map = {skill.name: skill for skill in arcana_skills_list}

    # 3) Pre-process tier config
    tier_config = {}
    for tier in arcana_tiers_list:
        tier_config[tier.tier_level] = {
            "name": tier.tier_name,
            "probability": tier.probability,
            "color": int(tier.color, base=16),
        }

    # 4) Organize skills by arcana and tier
    arcana_skills_dict = {}
    for arc in arcana_list:
        arcana_skills_dict[arc.id] = {
            "name": arc.name,
            "icon_url": arc.icon_url,
            "skills_by_tier": {},
        }

    for skill in arcana_skills_list:
        if skill.arcana_id in arcana_skills_dict:
            tier_level = skill.tier.tier_level
            if tier_level not in arcana_skills_dict[skill.arcana_id]["skills_by_tier"]:
                arcana_skills_dict[skill.arcana_id]["skills_by_tier"][tier_level] = []
            arcana_skills_dict[skill.arcana_id]["skills_by_tier"][tier_level].append(
                skill
            )

    # 5) Sort tiers for consistent usage
    sorted_tiers = sorted(arcana_tiers_list, key=lambda x: x.tier_level)

    return {
        "arcana_name_map": arcana_name_map,
        "skill_details_map": skill_details_map,
        "tier_config": tier_config,
        "arcana_skills": arcana_skills_dict,
        "sorted_tiers": sorted_tiers,
    }


def pick_skill_with_probability(
    arcana_name: str,
    arcana_name_map: Dict[str, object],
    arcana_skills_dict: Dict[int, Dict],
    sorted_tiers: List[object],
    GachaResultClass,
) -> object:
    """
    Returns a GachaResult (or None) by randomly picking
    a skill from the given arcana based on tier probability.
    """
    arcana = arcana_name_map.get(arcana_name.lower())
    if not arcana:
        return None

    arcana_config = arcana_skills_dict[arcana.id]
    random_seed = random.random()
    cumulative_prob = 0.0

    for tier in sorted_tiers:
        cumulative_prob += tier.probability
        # If the arcana has skills in this tier, check if we are within threshold
        if (
            tier.tier_level in arcana_config["skills_by_tier"]
            and arcana_config["skills_by_tier"][tier.tier_level]
        ):
            if random_seed <= cumulative_prob:
                chosen_skill = random.choice(
                    arcana_config["skills_by_tier"][tier.tier_level]
                )
                return GachaResultClass(
                    name=chosen_skill.name,
                    tier_level=tier.tier_level,
                    tier_name=tier.tier_name,
                    chance=tier.probability,
                    skill_id=chosen_skill.id,
                )
    return None
