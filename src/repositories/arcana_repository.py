from typing import List, Optional

from sqlalchemy.orm import joinedload
from sqlmodel import Session, select

from config.database import engine
from models.arcana import Arcana, ArcanaSkill, ArcanaTier


def create_arcana_skill(skill: ArcanaSkill):
    """
    Create an arcana skill
    """
    with Session(engine) as session:
        session.add(skill)
        session.commit()
        session.refresh(skill)
        return skill


def get_arcanas() -> List[Arcana]:
    """
    Get all arcanas
    """
    with Session(engine) as session:
        statement = select(Arcana)
        return session.exec(statement).all()


def get_arcana_by_id(arcana_id: int) -> Optional[Arcana]:
    """
    Get an arcana by id
    """
    with Session(engine) as session:
        statement = select(Arcana).where(Arcana.id == arcana_id)
        return session.exec(statement).first()


def get_arcana_tiers():
    """
    Get all arcana tiers
    """
    with Session(engine) as session:
        statement = select(ArcanaTier)
        return session.exec(statement).all()


def get_arcana_tier_by_id(tier_id: int) -> Optional[ArcanaTier]:
    """
    Get an arcana tier by id
    """
    with Session(engine) as session:
        statement = select(ArcanaTier).where(ArcanaTier.id == tier_id)
        return session.exec(statement).first()


def get_arcana_skills():
    """
    Get all arcana skills with tier and arcana relationships
    """
    with Session(engine) as session:
        statement = select(ArcanaSkill).options(
            joinedload(ArcanaSkill.tier), joinedload(ArcanaSkill.arcana)
        )
        skills = session.exec(statement).all()
        return skills


def get_arcana_skill_by_id(skill_id: int) -> ArcanaSkill:
    """
    Get an arcana skill by id
    """
    with Session(engine) as session:
        statement = select(ArcanaSkill).where(ArcanaSkill.id == skill_id)
        return session.exec(statement).first()


def get_arcana_skills_by_arcana_id(arcana_id: int) -> List[ArcanaSkill]:
    """
    Get all arcana skills by arcana id with tier and arcana relationships
    """
    with Session(engine) as session:
        statement = (
            select(ArcanaSkill)
            .options(joinedload(ArcanaSkill.tier), joinedload(ArcanaSkill.arcana))
            .where(ArcanaSkill.arcana_id == arcana_id)
        )
        return session.exec(statement).all()


def get_arcana_skills_by_tier_id(tier_id: int):
    """
    Get all arcana skills by tier id with tier and arcana relationships
    """
    with Session(engine) as session:
        statement = (
            select(ArcanaSkill)
            .options(joinedload(ArcanaSkill.tier), joinedload(ArcanaSkill.arcana))
            .where(ArcanaSkill.tier_id == tier_id)
        )
        return session.exec(statement).all()
