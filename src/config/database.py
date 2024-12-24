from sqlmodel import SQLModel, create_engine
import os
from utils.logger import BotLogger
from models.user import User
from models.arcana import Arcana, ArcanaTier, ArcanaSkill
from models.race import Race
from models.region import Region
from models.mana import ManaNature, ManaNatureCompositionLink
from models.character import Character


logger = BotLogger('database', write_to_console=False)

def get_database_url():
    # Get database connection parameters with fallbacks
    user = os.getenv('MYSQL_USER', 'ggm')
    password = os.getenv('MYSQL_PASSWORD', 'ggm')
    host = os.getenv('MYSQL_HOST', 'localhost')
    database = os.getenv('MYSQL_DB', 'ggm')
    
    # Log the connection details (excluding password)
    logger.info(f"Connecting to MySQL database at {host}/{database} as {user}")
    
    return f"mysql+pymysql://{user}:{password}@{host}/{database}"

# Get database URL from environment variables
DATABASE_URL = get_database_url()

engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    """Initialize the database by creating all tables"""
    logger.info("Creating database tables...")
    SQLModel.metadata.create_all(engine)
