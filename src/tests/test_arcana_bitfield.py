import utils.arcana_bitfield as ab

test_bitfield = 0 | ab.ArcanaSkill.MAGICLESS


def test_resolve_skill_mask():
    """
    Test resolving a skill to its bitmask.
    """
    # We start by ensuring that the skill enum has the correct bitmask.
    assert ab.ArcanaSkill.PROJECTILE.value == 1 << 1
    # We then test that the resolve_skill_mask function returns the correct bitmask.
    assert ab.resolve_skill_mask(ab.ArcanaSkill.PROJECTILE) == 1 << 1
    # We also test that the resolve_skill_mask function returns the correct bitmask for an integer.
    assert ab.resolve_skill_mask(1) == 1 << 1


def test_has_skill():
    """
    Test checking if a skill is in the bitfield.
    """
    global test_bitfield
    assert ab.has_skill(test_bitfield, ab.ArcanaSkill.MAGICLESS) is True
    assert ab.has_skill(test_bitfield, ab.ArcanaSkill.GROUP_TELEPORTATION) is False


def test_add_skill():
    """
    Test adding a skill to the bitfield.
    """
    global test_bitfield
    test_bitfield = ab.add_skill(
        test_bitfield, ab.ArcanaSkill.LONG_DISTANCE_TELEPORTATION
    )
    # We then check that the bitfield has the correct value.
    assert (
        ab.has_skill(test_bitfield, ab.ArcanaSkill.LONG_DISTANCE_TELEPORTATION) is True
    )
    assert ab.has_skill(test_bitfield, ab.ArcanaSkill.GROUP_TELEPORTATION) is False
    # We also test that adding a skill that is already in the bitfield does not change the bitfield.
    test_bitfield = ab.add_skill(test_bitfield, ab.ArcanaSkill.MAGICLESS)
    assert test_bitfield == test_bitfield


def test_remove_skill():
    """
    Test removing a skill from the bitfield.
    """
    global test_bitfield
    # Since we now have some arcana skills set, we should no longer be magicless.
    test_bitfield = ab.remove_skill(test_bitfield, ab.ArcanaSkill.MAGICLESS)
    assert ab.has_skill(test_bitfield, ab.ArcanaSkill.MAGICLESS) is False
    # We also test that removing a skill that is not in the bitfield does not change the bitfield.
    test_bitfield = ab.remove_skill(test_bitfield, ab.ArcanaSkill.MAGICLESS)
    assert test_bitfield == test_bitfield


def test_get_skills():
    """
    Test getting a list of skills from the bitfield.
    """
    wizard_bitfield = (
        0
        | ab.ArcanaSkill.GROUP_TELEPORTATION
        | ab.ArcanaSkill.PROJECTILE
        | ab.ArcanaSkill.MIRACLE
    )
    # By default, the skills are returned in the order they are defined in the enum, so
    # we need to check against an ordered list.
    assert ab.get_skills(wizard_bitfield) == sorted(
        [
            ab.ArcanaSkill.MIRACLE,
            ab.ArcanaSkill.GROUP_TELEPORTATION,
            ab.ArcanaSkill.PROJECTILE,
        ],
        key=lambda skill: skill.value,
    )
    # We also test that the get_skills function returns an empty list if no skills are set.
    assert ab.get_skills(0) == []


def test_get_skill_ids():
    """
    Test getting a list of skill IDs from the bitfield.
    """
    global test_bitfield
    assert ab.get_skill_ids(test_bitfield) == [53]
    test_bitfield = ab.add_skill(test_bitfield, ab.ArcanaSkill.PROJECTILE)
    assert ab.get_skill_ids(test_bitfield) == [1, 53]
    test_bitfield = ab.add_skill(test_bitfield, ab.ArcanaSkill.GROUP_TELEPORTATION)
    assert ab.get_skill_ids(test_bitfield) == [1, 52, 53]
