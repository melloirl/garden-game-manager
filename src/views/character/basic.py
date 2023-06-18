import discord
from discord import app_commands, SelectOption
from discord.ui import Select, View


def embed(character):
    embed = discord.Embed(
        title=character['name'], description='*Informações Básicas*')
    embed.set_image(url=character['image'])
    embed.add_field(name='Idade:', value=character['age'], inline=True)
    embed.add_field(name='Origem:', value=character['origin'], inline=True)
    embed.add_field(name='Raça:', value=character['race'], inline=True)
    embed.add_field(name=' ', value='', inline=False)
    embed.add_field(name='Classe:', value=character['class'], inline=True)
    manas = ', '.join([mana['name'] for mana in character['manas']])
    embed_color = character['manas'][-1]['color'][1:]
    embed_color = int(embed_color, 16)
    embed.color = embed_color
    embed.add_field(name='Mana:', value=manas, inline=True)
    embed.set_footer(icon_url=character['footer_icon'], text=character['origin']) 
    return embed
