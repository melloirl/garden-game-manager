from sqlmodel import Session, select
from models.user import User
from config.database import engine
from datetime import datetime

def get_or_create_user(discord_id: str, player_name: str) -> User:
    with Session(engine) as session:
        # Try to find existing user
        statement = select(User).where(User.discord_id == discord_id)
        user = session.exec(statement).first()
        
        if user:
            # Update last active timestamp
            user.last_active = datetime.utcnow()
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        
        # Create new user if not found
        new_user = User(discord_id=discord_id, player_name=player_name)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user

def increment_gacha_count(discord_id: str):
    with Session(engine) as session:
        statement = select(User).where(User.discord_id == discord_id)
        user = session.exec(statement).first()
        if user:
            user.gacha_count += 1
            session.add(user)
            session.commit()
            session.refresh(user)
            return user.gacha_count
        return 0

def get_user_by_discord_id(discord_id: str) -> User | None:
    with Session(engine) as session:
        statement = select(User).where(User.discord_id == discord_id)
        return session.exec(statement).first()
