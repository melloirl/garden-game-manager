# We have three separate .env files for development and production

# The .env file defines general environment variables and exposes the ENVIRONMENT variable
# Which tells us which .env file to load

# The .env.dev file defines environment variables for the development environment
# The .env.prod file defines environment variables for the production environment

import os
from dotenv import load_dotenv


def load_env():
    """
    Load environment variables with Docker-aware priority:
    1. System/Docker environment variables
    2. Environment-specific .env file (.env.dev or .env.prod)
    3. Base .env file
    """
    # Load base .env first
    try:
        load_dotenv(".env")
    except Exception:
        pass

    # Get environment from system (should be set by Docker)
    env = os.getenv("ENVIRONMENT")

    # Load environment-specific file if environment is set
    if env:
        env_file = f".env.{env}"
        try:
            load_dotenv(env_file)
        except Exception:
            pass

    # Verify required variables
    required_vars = ["DISCORD_TOKEN", "DISCORD_GUILD_ID", "BOT_PREFIX"]
    missing = [v for v in required_vars if not os.getenv(v)]
    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}"
        )


load_env()
