from sqlalchemy.orm import joinedload
from models.arcana import Arcana, ArcanaTier, ArcanaSkill
from config.database import engine
from typing import List
from sqlmodel import Session, select


def get_arcanas():
    """
    Get all arcanas
    """
    with Session(engine) as session:
        statement = select(Arcana)
        return session.exec(statement).all()


def get_arcana_tiers():
    """
    Get all arcana tiers
    """
    with Session(engine) as session:
        statement = select(ArcanaTier)
        return session.exec(statement).all()


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


def create_arcana_skill(skill: ArcanaSkill):
    """
    Create an arcana skill
    """
    with Session(engine) as session:
        session.add(skill)
        session.commit()
        session.refresh(skill)
        return skill
