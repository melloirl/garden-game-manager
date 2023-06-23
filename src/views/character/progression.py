import discord
from discord import app_commands, SelectOption
from discord.ui import Select, View


def embed(character):
    embed = discord.Embed(
        title=character['name'], description='*Progressão*')
    embed.set_image(url=character['image'])
    embed.add_field(name='Nível:', value=character['level'], inline=True)
    embed.add_field(
        name='XP:', value=f"{character['experience_points']}/{character['level']*100}", inline=True)
    embed.add_field(name=' ', value='', inline=False)
    embed.add_field(name='Vida:', value=f"{character['hp']}/{character['max_hp']}", inline=True)
    embed.add_field(name='Mana:', value=f"{character['mp']}/{character['max_mp']}", inline=True)
    embed.add_field(name='Energia:', value=f"{character['sp']}/{character['max_sp']}", inline=True) 
    embed_color = character['manas'][-1]['color'][1:]
    embed_color = int(embed_color, 16)
    embed.color = embed_color
    embed.set_footer(icon_url=character['footer_icon'], text=character['origin']) 
    return embed
