import discord
import typing
from discord import app_commands
from utils.characters.character import get_character_by_name, fetch_characters, update_character_by_name, get_first_character_by_player_discord_id
from utils.abilities.ability import fetch_abilities_by_character_name

@app_commands.describe(
    habilidade='A habilidade que você quer usar',
    nome='O personagem que vai usar a habilidade'
)
async def usar(interaction: discord.Interaction, habilidade: str, nome: str = None ):
    ''' Usa uma habilidade do grimório de um personagem '''
    # Se não houver nome, busca o primeiro personagem do usuário pelo id do discord, se houver nome, busca o personagem pelo nome
    if not nome:
        # Adquire o id do discord do usuário
        user_id = interaction.user.id
        # Adquire o primeiro personagem do usuário
        character = get_first_character_by_player_discord_id(user_id)
        # Adquire o nome do personagem
        nome = character['name']
    else:
        character = get_character_by_name(nome)
    # Se não houver personagem, retorna uma mensagem de erro
    if not character:
        await interaction.response.send_message('Personagem não encontrado', ephemeral=True)
    # Se houver personagem, busca as habilidades do personagem
    else:
        abilities = fetch_abilities_by_character_name(nome)
        # Se não houver habilidades, retorna uma mensagem de erro
        if not abilities:
            await interaction.response.send_message('Habilidade não encontrada', ephemeral=True)
        # Se houver habilidades, busca a habilidade pelo nome
        else:
            selected_ability = [ability for ability in abilities if ability['name'] == habilidade]
            # Verifica o tipo de recurso que a habilidade usa
            match(selected_ability[0]['cost_type']):
                case 'Mana':
                    # Verifica se o personagem tem mana suficiente
                    if character['mp'] < selected_ability[0]['cost_amount']:
                        await interaction.response.send_message('Mana insuficiente', ephemeral=True)
                    else:
                        # Reduz a mana do personagem pelo custo da habilidade
                        character['mp'] -= selected_ability[0]['cost_amount']
                        # Atualiza o personagem no banco de dados
                         # Adicione somente o ObjectId do objeto a um array
                        for mana in character['manas']:
                            character['manas'][character['manas'].index(mana)] = mana['_id']
                        # Para cada objeto em character['player']
                        # Adicione somente o ObjectId do objeto a um array
                        character['player'] = character['player']['_id']
                        # Para cada objeto em character['abilities']
                        # Adicione somente o ObjectId do objeto a um array
                        for ability in character['abilities']:
                            character['abilities'][character['abilities'].index(ability)] = ability['_id']
                        update_character_by_name(nome, character)
                        # Se tiver, usa a habilidade
                        await interaction.response.send_message(f'{character["name"]} usou {selected_ability[0]["name"]}')
                case 'Energia':
                    # Verifica se o personagem tem energia suficiente
                    if character['sp'] < selected_ability[0]['cost_amount']:
                        await interaction.response.send_message('Energia insuficiente', ephemeral=True)
                    else:
                        # Reduz a energia do personagem pelo custo da habilidade
                        character['sp'] -= selected_ability[0]['cost_amount']
                        # Atualiza o personagem no banco de dados
                        update_character_by_name(nome, character)
                        # Se tiver, usa a habilidade
                        await interaction.response.send_message('Habilidade usada', ephemeral=True)
                case 'Vida':
                    # Verifica se o personagem tem vida suficiente
                    if character['hp'] < selected_ability[0]['cost_amount']:
                        await interaction.response.send_message('Vida insuficiente', ephemeral=True)
                    else:
                        # Reduz a vida do personagem pelo custo da habilidade
                        character['hp'] -= selected_ability[0]['cost_amount']
                        # Atualiza o personagem no banco de dados
                        update_character_by_name(nome, character)
                        # Se tiver, usa a habilidade
                        await interaction.response.send_message('Habilidade usada', ephemeral=True)
                case _:
                    # Se não tiver, retorna uma mensagem de erro
                    await interaction.response.send_message('Tipo de recurso não encontrado', ephemeral=True)

async def autocomplete_nome(interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
    # Busca a lista de nomes de personagens
    names = fetch_characters()()
    # Retorna uma lista de objetos Choice com os nomes
    return [app_commands.Choice(name=name, value=name) for name in names if name.startswith(current)]

async def autocomplete_habilidade(interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
    # Se não houver um nome, retorna uma lista vazia 
    name = interaction.data['options'][0]['value']
    if not name:
        # Busca o personagem pelo id do discord
        user_id = interaction.user.id
        # Adquire o primeiro personagem do usuário
        character = get_first_character_by_player_discord_id(user_id)
        # Adquire o nome do personagem
        name = character['name']
    # Busca a lista de habilidades do personagem
    abilities = fetch_abilities_by_character_name(name)
    # Verifica o nivel do personagem
    character_level = get_character_by_name(name)['level']
    # Remove as habilidades que não podem ser usadas pelo personagem
    abilities = [ability for ability in abilities if ability['level'] <= character_level]
    # Retorna uma lista de objetos Choice com os nomes
    return [app_commands.Choice(name=ability['name'], value=ability['name']) for ability in abilities if ability['name'].startswith(current)]

commands = [(usar, autocomplete_nome, 'nome'),(usar, autocomplete_habilidade, 'habilidade')]