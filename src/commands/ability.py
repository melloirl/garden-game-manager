import discord
import typing
from discord import app_commands, SelectOption
from discord.ui import Select, View
from utils.characters.character import get_character_by_name, fetch_characters, get_first_character_by_player_discord_id
from utils.abilities.ability import fetch_abilities_by_character_name


@app_commands.describe(
    nome='O nome do personagem',
    habilidade='Quer ver a descrição de alguma habilidade específica?'
)
async def grimorio(interaction: discord.Interaction, nome: str = None, habilidade: str = None):
    ''' Retorna as habilidades e feitiços do grimório de um personagem '''
    # Se não houver nome, busca o primeiro personagem do usuário pelo id do discord
    if not nome:
        # Adquire o id do discord do usuário
        user_id = interaction.user.id
        # Adquire o primeiro personagem do usuário
        character = get_first_character_by_player_discord_id(user_id)
        # Se não houver personagem, retorna uma mensagem de erro
        if not character:
            await interaction.response.send_message('Personagem não encontrado', ephemeral=True)
        # Se houver personagem, busca as habilidades do personagem
        else:
            abilities = fetch_abilities_by_character_name(character['name'])
            # Se não houver habilidades, retorna uma mensagem de erro
            if not abilities:
                await interaction.response.send_message('Habilidades não encontradas', ephemeral=True)
            # Se houver habilidades, retorna uma mensagem com o grimório
            else:
                # Inicializa uma string vazia
                grimorio = ''
                # Para cada habilidade, adiciona uma linha com o nome e a descrição
                # Adquire o nível do personagem
                character_level = character['level']
                for ability in abilities:
                    # Verifica se o nível da habilidade é menor ou igual ao nível do personagem
                    if ability['level'] <= character_level:
                        # Se for, mostra a habilidade
                        grimorio += f'**{ability["name"]}** (LVL. {ability["level"]}): '
                        grimorio += f'{ability["description"]}\n'
                        grimorio += f'**Custo:** {ability["cost_amount"]} {ability["cost_type"]}\n'
                        grimorio += f'**Tipo:** {ability["type"]}\n'
                        grimorio += f'**Efeito:** {ability["effect"]}\n'
                        grimorio += f'**Rolagem**: {ability["dice"]}\n'
                        grimorio += f'**Tipo de Dano:** {ability["damage_type"]}\n\n'
                # Envia a mensagem com o grimório
                await interaction.response.send_message(grimorio, ephemeral=True)
    if nome:
        # Busca as habilidades do personagem
        abilities = fetch_abilities_by_character_name(nome)
        # Se não houver habilidades, retorna uma mensagem de erro
        if not abilities:
            await interaction.response.send_message('Personagem não encontrado', ephemeral=True) 
        # Se houver habilidades, retorna uma mensagem com o grimório
        else: 
           # Inicializa uma string vazia
            grimorio = ''
            # Para cada habilidade, adiciona uma linha com o nome e a descrição
            # Adquire o nível do personagem
            character_level = get_character_by_name(nome)['level']
            for ability in abilities:
                # Verifica se o nível da habilidade é menor ou igual ao nível do personagem
                if ability['level'] <= character_level:
                    # Se for, mostra a habilidade
                    grimorio += f'**{ability["name"]}** (LVL. {ability["level"]}): '
                    grimorio += f'{ability["description"]}\n'
                    grimorio += f'**Custo:** {ability["cost_amount"]} {ability["cost_type"]}\n'
                    grimorio += f'**Tipo:** {ability["type"]}\n'
                    grimorio += f'**Efeito:** {ability["effect"]}\n'
                    grimorio += f'**Rolagem**: {ability["dice"]}\n'
                    grimorio += f'**Tipo de Dano:** {ability["damage_type"]}\n\n'
            # Envia a mensagem com o grimório
            await interaction.response.send_message(grimorio, ephemeral=True)

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

async def autocomplete_habilidade(interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
    # Se não houver um nome, retorna uma lista vazia 
    name = interaction.data['options'][0]['value']
    if not name:
        return []
    # Busca a lista de habilidades do personagem
    abilities = fetch_abilities_by_character_name(name)
    # Verifica o nivel do personagem
    character_level = get_character_by_name(name)['level']
    # Remove as habilidades que não podem ser usadas pelo personagem
    abilities = [ability for ability in abilities if ability['level'] <= character_level]
    # Retorna uma lista de objetos Choice com os nomes
    return [app_commands.Choice(name=ability['name'], value=ability['name']) for ability in abilities if ability['name'].startswith(current)]


commands = [(grimorio, autocomplete_nome, 'nome'),(grimorio, autocomplete_habilidade, 'habilidade')]
