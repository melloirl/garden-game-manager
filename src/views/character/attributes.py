import discord
from discord import app_commands, SelectOption
from discord.ui import Select, View


def embed(character):
    embed = discord.Embed(
        title=character['name'], description='*Atributos*')
    embed.set_image(url=character['image'])
    embed.add_field(name='Força:', value=character['strength'], inline=True)
    embed.add_field(
        name='Destreza:', value=character['dexterity'], inline=True)
    # embed.add_field(name=' ', value='', inline=False)
    embed.add_field(name='Vitalidade:', value=character['vitality'], inline=True)
    embed.add_field(name='Inteligência:', value=character['intelligence'], inline=True)
    embed.add_field(name='Controle:', value=character['control'], inline=True)
    embed.add_field(name='Mana:', value=character['mana'], inline=True)
    embed.add_field(name='Resistência:', value=character['resistance'], inline=True)
    embed_color = character['manas'][-1]['color'][1:]
    embed_color = int(embed_color, 16)
    embed.color = embed_color
    embed.set_footer(icon_url=character['footer_icon'], text=character['origin']) 
    return embed
