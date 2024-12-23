# We have three separate .env files for development and production

# The .env file defines general environment variables and exposes the ENVIRONMENT variable
# Which tells us which .env file to load

# The .env.dev file defines environment variables for the development environment
# The .env.prod file defines environment variables for the production environment

import os
from dotenv import load_dotenv

def load_env():
    # Load the default .env file first
    load_dotenv('.env')  # Specify the default .env file

    # Load the environment-specific .env file based on the ENVIRONMENT variable
    if os.getenv('ENVIRONMENT') == 'dev':
        load_dotenv('.env.dev')
    elif os.getenv('ENVIRONMENT') == 'prod':
        load_dotenv('.env.prod')

load_env()
