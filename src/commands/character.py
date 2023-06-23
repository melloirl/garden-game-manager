import discord
import typing
from discord import app_commands, SelectOption
from discord.ui import Select, View
from utils.characters.character import get_character_by_name, fetch_characters, get_first_character_by_player_discord_id
from views.character import basic, appearance, personality, history, progression, attributes
from utils.db import *
from bson import ObjectId

# Create a dictionary containing the embeds
embeds = {
    'basic': basic.embed,
    'appearance': appearance.embed,
    'personality': personality.embed,
    'history': history.embed,
    'progression': progression.embed,
    'attributes':  attributes.embed,
}

footer_icon = {
    'Naruvala': 'https://media.discordapp.net/attachments/1096537580121624608/1119898150698754149/Naruvala.png?width=676&height=676',
    'Império Daeliseo': 'https://media.discordapp.net/attachments/1096537580121624608/1119898150312882236/imperio.png?width=676&height=676',
    'Ramaliah': 'https://media.discordapp.net/attachments/1096537580121624608/1119898151340474378/ramaliah.png?width=676&height=676',
    'Kainá': 'https://media.discordapp.net/attachments/1096537580121624608/1119898149973131295/kaina.png?width=676&height=676',
    'Ilha de Luminaire': 'https://media.discordapp.net/attachments/1096537580121624608/1119898151730556928/luminaire.png?width=676&height=676',
    'Waiola': 'https://media.discordapp.net/attachments/1096537580121624608/1119898152108040283/waiola.png?width=676&height=676',
}


@app_commands.describe(
    nome='O nome do personagem',
    mostrar='Quer compartilhar sua ficha com os outros jogadores?'
)
async def personagem(interaction: discord.Interaction, nome: str = None, mostrar: typing.Literal[*embeds.keys()] = None):
    ''' Retorna a ficha do personagem '''
    # Se não houver nome, assuma que o usuário quer ver a ficha de seu primeiro personagem
    if not nome:
        character = get_first_character_by_player_discord_id(interaction.user.id)
        print(character)
    else:
        character = get_character_by_name(nome)

    if not character:
        await interaction.response.send_message('Personagem não encontrado', ephemeral=True)
        return

    sender_id = interaction.user.id
    owner_id = character['player']['userID']
 
    if str(sender_id) != str(owner_id) and not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('Você não pode ver a ficha de outro jogador', ephemeral=True)
        return

    character['footer_icon'] = footer_icon[character['origin']]
    embed = embeds['basic'](character)

    options = [
        SelectOption(label='Informações Básicas', value='basic',
                     description='Informações básicas do personagem', emoji='📄'),
        SelectOption(label='Aparência', value='appearance',
                     description='Aparência do personagem', emoji='👤'),
        SelectOption(label='Personalidade', value='personality',
                     description='Personalidade do personagem', emoji='🧠'),
        SelectOption(label='História', value='history',
                     description='História do personagem', emoji='📜'),
        SelectOption(label='Progressão', value='progression',
                     description='Progressão do personagem', emoji='📈'),
        SelectOption(label='Atributos', value='attributes',
                     description='Atributos do personagem', emoji='📊'),
    ]

    class Dropdown(discord.ui.Select):
        def __init__(self):
            super().__init__(placeholder='Informação',
                             options=options, custom_id='info_selection')

        async def callback(self, interaction: discord.Interaction):
            value = interaction.data['values'][0]
            embed = embeds[value](character)
            await interaction.response.edit_message(embed=embed)

    selection_dropdown = View().add_item(Dropdown())

    if mostrar:
        embed = embeds[mostrar](character)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(embed=embed, view=selection_dropdown, ephemeral=True)


async def autocomplete_nome(interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
    try:
        # Adquire o id do discord do usuário
        user_id = interaction.user.id
        # Adquire a lista de todos os personagens
        characters = fetch_characters()
        
        # Criar uma nova lista com apenas os personagens que o usuário é o dono ou se o usuário é um administrador
        characters = [character for character in characters if str(user_id) == str(character['player']['userID']) or interaction.user.guild_permissions.administrator]

        # Extrair os nomes dos personagens
        names = [character['name'] for character in characters]

        # Retorna uma lista de objetos Choice com os nomes que começam com 'current'
        return [app_commands.Choice(name=name, value=name) for name in names if name.startswith(current)]

    except Exception as e:
        print(f"An error occurred: {e}")


commands = [(personagem, autocomplete_nome, 'nome')]
