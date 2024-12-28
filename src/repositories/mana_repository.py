from typing import List

from sqlmodel import Session, select

from config.database import engine
from models.mana import ManaNature


def get_manas() -> List[ManaNature]:
    """
    Get all mana natures
    """
    with Session(engine) as session:
        statement = select(ManaNature)
        return session.exec(statement).all()


def get_mana_by_id(id: int) -> ManaNature:
    """
    Get a mana nature by id
    """
    with Session(engine) as session:
        statement = select(ManaNature).where(ManaNature.id == id)
        return session.exec(statement).first()
