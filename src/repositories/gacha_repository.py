from sqlmodel import Session, select

from config.database import engine
from models.gacha import GachaConfig


def get_gacha_config() -> GachaConfig:
    with Session(engine) as session:
        statement = select(GachaConfig)
        return session.exec(statement).first()
