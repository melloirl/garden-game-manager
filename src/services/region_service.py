from models.region import Region
from sqlmodel import Session, select
from config.database import engine
from typing import List


def get_regions() -> List[Region]:
    """
    Get all regions
    """
    with Session(engine) as session:
        statement = select(Region)
        return session.exec(statement).all()


def get_region_by_id(id: int) -> Region:
    """
    Get a region by id
    """
    with Session(engine) as session:
        statement = select(Region).where(Region.id == id)
        return session.exec(statement).first()
