from typing import List

from sqlmodel import Session, select

from config.database import engine
from models.race import Race


def get_races() -> List[Race]:
    """
    Get all races
    """
    with Session(engine) as session:
        statement = select(Race)
        return session.exec(statement).all()


def get_race_by_id(id: int) -> Race:
    """
    Get a race by id
    """
    with Session(engine) as session:
        statement = select(Race).where(Race.id == id)
        return session.exec(statement).first()
