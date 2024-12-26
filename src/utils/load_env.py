# We have three separate .env files for development and production

# The .env file defines general environment variables and exposes the ENVIRONMENT variable
# Which tells us which .env file to load

# The .env.dev file defines environment variables for the development environment
# The .env.prod file defines environment variables for the production environment

import os
from dotenv import load_dotenv


def load_env():
    """
    Load environment variables with the following priority:
    1. System environment variables
    2. .env files (if they exist)
    """
    # First check if required variables are already set in system environment
    required_vars = ["DISCORD_TOKEN", "DISCORD_GUILD_ID", "BOT_PREFIX"]
    all_vars_present = all(os.getenv(var) for var in required_vars)

    # If all required variables are present in system environment, we can skip loading .env files
    if all_vars_present:
        return

    # Otherwise, try to load from .env files as fallback
    try:
        load_dotenv(".env")
    except Exception:
        pass

    # Get environment from system or .env file
    env = os.getenv("ENVIRONMENT")

    # If environment is set, try to load the corresponding .env file
    if env == "dev":
        try:
            load_dotenv(".env.dev")
        except Exception:
            pass
    elif env == "prod":
        try:
            load_dotenv(".env.prod")
        except Exception:
            pass


load_env()
