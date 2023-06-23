import discord
import os
import glob
import importlib.util
from dotenv import load_dotenv
from discord import app_commands
import logging

# Create directory for logs if not exists
os.makedirs('logs', exist_ok=True)

# Create a logger object
logger = logging.getLogger('discord')
# Adjust this level to see more or less information
logger.setLevel(logging.INFO)

# Create a handler that writes to a file
handler = logging.FileHandler(
    filename='logs/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

# Add the handler to the logger
logger.addHandler(handler)

# Load environment variables
load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')

# Replace with your guild id
MY_GUILD = discord.Object(id=995177227698311199)


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)

        # Initialize command tree
        self.tree = app_commands.CommandTree(self)

        # Dynamically load commands
        for filename in glob.glob('src/commands/*.py'):
            spec = importlib.util.spec_from_file_location('commands', filename)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for command in getattr(module, 'commands', []):
                # Check if the command is already registered
                if isinstance(command, tuple):
                    # Check if the command is not already registered
                    if not self.tree.get_command(command[0].__name__):
                        print(f"Adding command: {command[0].__name__}")

                        # Manually apply the decorator here
                        self.tree.command()(command[0])
                    # Register the autocomplete
                    cmd = command[0]
                    autocomplete_function = command[1]
                    autocomplete_param_name = command[2]
                    print(f"Adding autocomplete: {command[0].__name__}") 
                    # Now add the autocomplete to the added command
                    self.tree.get_command(cmd.__name__).autocomplete(
                        autocomplete_param_name)(autocomplete_function)

                elif not self.tree.get_command(command.__name__):
                    print(f"Adding command: {command.__name__}")

                    # Manually apply the decorator here
                    self.tree.command()(command)

    async def setup_hook(self):
        """
        In this basic example, we just synchronize the app commands to one guild.
        Instead of specifying a guild to every command, we copy over our global 
        commands instead. By doing so, we don't have to wait up to an hour until 
        they are shown to the end-user.
        """

        # Copy the global commands over to your guild
        self.tree.copy_global_to(guild=MY_GUILD)

        # Synchronize the command tree with the guild
        await self.tree.sync(guild=MY_GUILD)


# Initialize intents
intents = discord.Intents.default()

# Initialize client
client = MyClient(intents=intents)


@client.event
async def on_ready():
    """
    Event handler for when the bot is ready.
    Prints bot details and invite link.
    """
    logger.info(f'Logged in as {client.user} (ID: {client.user.id})')
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('Invite Link: https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
    print('------')
