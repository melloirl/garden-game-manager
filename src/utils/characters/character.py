from utils.db import characters_collection, manas_collection, users_collection, abilities_collection
from utils.characters.aggregations import max_hp, max_mp, max_sp

from bson.objectid import ObjectId


def get_character_by_name(name):
    pipeline = [{"$match": {"name": {"$regex": name, "$options": "i"}}}
                ] + max_hp() + max_mp() + max_sp()
    print(f"Looking for {name} in the database")
    character = list(characters_collection.aggregate(pipeline))

    if character:
        character = character[0]  # get the first document from the result
        # Get the list of manas ObjectId's
        mana_ids = character['manas']
        # Get list of the player's ObjectId's
        player_ids = character['player']

        # Replace the list of manas ObjectId's with the actual manas documents
        character['manas'] = [manas_collection.find_one(
            {"_id": ObjectId(mana_id)}) for mana_id in mana_ids]
        # Replace the player object id with the actual player document
        character['player'] = users_collection.find_one(
            {"_id": ObjectId(player_ids)})

    # Convert the max_hp, max_mp and max_sp to int, rounding up
    character['max_hp'] = int(character['max_hp'])
    character['max_mp'] = int(character['max_mp'])
    character['max_sp'] = int(character['max_sp'])

    return character

def get_first_character_by_player_discord_id(discord_id):
    # From the users collection, get the user with the given discord_id
    user = users_collection.find_one({"userID": str(discord_id)})
    # If there are no users with the given discord_id, return None
    if not user:
        return None
    # Get the list of characters ObjectId's
    character_ids = user['characters']
    # If the user has no characters, return None
    if not character_ids:
        return None

    # Get the first character ObjectId
    character_id = character_ids[0]
    # Get the character document
    character = characters_collection.find_one({"_id": ObjectId(character_id)})
    print(character)
    
    # If the character does not exist, return None
    if not character:
        return None

    # Get the list of manas ObjectId's
    mana_ids = character['manas']
    # Replace the list of manas ObjectId's with the actual manas documents
    character['manas'] = [manas_collection.find_one(
        {"_id": ObjectId(mana_id)}) for mana_id in mana_ids]

    # Get list of the player's ObjectId's
    player_id = character['player']
    # Replace the player object id with the actual player document
    character['player'] = users_collection.find_one(
        {"_id": ObjectId(player_id)})

    # Get the list of abilities ObjectId's
    ability_ids = character['abilities']
    # Replace the list of abilities ObjectId's with the actual abilities documents
    character['abilities'] = [abilities_collection.find_one(
        {"_id": ObjectId(ability_id)}) for ability_id in ability_ids]

    return character

    
def update_character_by_name(name, new_values):
    # Tenta atualizar o personagem no banco de dados mongodb

    characters_collection.update_one({"name": name}, {"$set": new_values})


def fetch_characters():
    try:
        # Returns a list of all characters
        characters = list(characters_collection.find())
        # Populate the characters' manas, players and abilities
        populated_characters = []
        for character in characters:
            character['manas'] = [manas_collection.find_one(
                {"_id": ObjectId(mana_id)}) for mana_id in character['manas']]
            character['player'] = users_collection.find_one(
                {"_id": ObjectId(character['player'])})
            character['abilities'] = [abilities_collection.find_one(
                {"_id": ObjectId(ability_id)}) for ability_id in character['abilities']]
            populated_characters.append(character)
        return populated_characters
    except Exception as e:
        print(f"An error occurred: {e}")

