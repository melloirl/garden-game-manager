import discord
import typing
from discord import app_commands, SelectOption
from discord.ui import Select, View
from utils.characters.character import get_character_by_name, update_character_by_name, fetch_characters
from views.character import basic, appearance, personality, history, progression, attributes

attributes = {
    "Nome": "name",
    "Imagem": "image",
    "Idade": "age",
    "Origem": "origin",
    "Classe": "class",
    "Raça": "race",
    "Aparência": "appearance_description",
    "História": "lore_description",
    "Personalidade": "personality_description",
    "Força": "strength",
    "Controle": "control",
    "Destreza": "dexterity",
    "Inteligência": "intelligence",
    "Mana": "mana",
    "Resistencia": "resistance",
    "Vitalidade": "vitality",
    "XP": "experience_points",
    "HP": "hp",
    "Nível": "level",
    "MP": "mp",
    "SP": "sp"
}


@app_commands.describe(
    nome='O nome do personagem',
    attr='O atributo que deseja editar',
    valor='O novo valor do atributo'
)
async def editar(interaction: discord.Interaction, nome: str, attr: typing.Literal[*attributes.keys()], valor: str):
    ''' Edita um atributo do personagem '''

    # Certifica-se que o usuário é administrador 
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('Você não tem permissão para usar este comando', ephemeral=True)
        return
    # Caso o usuário seja administrador, continua
    character = get_character_by_name(nome)
    if not character:
        await interaction.response.send_message('Personagem não encontrado', ephemeral=True)
        return
    # Caso o personagem seja encontrado, continua
    # Verifica se o valor tem letras
    # Verifica se o valor tem prefixos de sinal + ou -
    if valor.startswith('+'):
        # Se sim, soma o valor ao atributo
        character[attributes[attr]] += int(valor[1:])
    elif valor.startswith('-'):
        # Se não, subtrai o valor do atributo
        character[attributes[attr]] -= int(valor[1:])
    else:
        # Se não, atribui o valor ao atributo
        # Se o valor só tiver números, converte para inteiro
        if (valor.isnumeric()):
            valor = int(valor)
        character[attributes[attr]] = valor
    # Para cada objeto em character['manas']
    # Adicione somente o ObjectId do objeto a um array
    for mana in character['manas']:
        character['manas'][character['manas'].index(mana)] = mana['_id']
    
    # Para cada objeto em character['player']
    # Adicione somente o ObjectId do objeto a um array
    character['player'] = character['player']['_id']

    # Tenta atualizar o personagem no banco de dados mongodb
    update_character_by_name(nome, character)
    # Envia uma mensagem de confirmação
    await interaction.response.send_message('Atributo alterado com sucesso', ephemeral=True)


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

commands = [(editar, autocomplete_nome, 'nome')]
