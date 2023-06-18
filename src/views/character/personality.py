import discord
from discord import app_commands, SelectOption
from discord.ui import Select, View


def embed(character):
    embed = discord.Embed(
        title=character['name'], description='*Personalidade*')
    embed.set_image(url=character['image'])
    # Add field for appearance
    # Trim the personality description to 1024 characters
    character['personality_description'] = character['personality_description'][:1024]
    embed.add_field(
        name='', value=character['personality_description'], inline=False)
    embed_color = character['manas'][-1]['color'][1:]
    embed_color = int(embed_color, 16)
    embed.color = embed_color
    embed.set_footer(icon_url=character['footer_icon'], text=character['origin']) 
    return embed
