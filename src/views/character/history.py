import discord
from discord import app_commands, SelectOption
from discord.ui import Select, View


def embed(character):
    embed = discord.Embed(
        title=character['name'], description='*História*')
    embed.set_image(url=character['image'])
    # Add field for appearance
    # Trim the lore description to 1024 characters
    character['lore_description'] = character['lore_description'][:1024]
    embed.add_field(
        name='', value=character['lore_description'], inline=False)
    embed_color = character['manas'][-1]['color'][1:]
    embed_color = int(embed_color, 16)
    embed.color = embed_color
    embed.set_footer(icon_url=character['footer_icon'], text=character['origin']) 
    return embed
