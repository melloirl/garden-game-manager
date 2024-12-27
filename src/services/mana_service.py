from typing import List

from sqlmodel import Session, select

from config.database import engine
from models.mana import Mana


def get_manas() -> List[Mana]:
    """
    Get all manas
    """
    with Session(engine) as session:
        statement = select(Mana)
        return session.exec(statement).all()


def get_mana_by_id(id: int) -> Mana:
    """
    Get a mana by id
    """
    with Session(engine) as session:
        statement = select(Mana).where(Mana.id == id)
        return session.exec(statement).first()
