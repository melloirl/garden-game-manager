import logging

# Create a logger object
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)  # You can adjust this level to see more or less information

# Create a handler that writes to a file
handler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

# Add the handler to the logger
logger.addHandler(handler)
