from utils.db import characters_collection, manas_collection, users_collection

from bson.objectid import ObjectId


def get_character_by_name(name):
    if len(name.split()) == 1:
        print(f"Looking for {name} in the database")
        character = characters_collection.find_one(
            {"name": {"$regex": name, "$options": "i"}})
    else:
        print(f"Looking for {name} in the database")
        character = characters_collection.find_one({"name": name})

    if character:
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

    return character


def update_character_by_name(name, new_values):
    # Tenta atualizar o personagem no banco de dados mongodb

    characters_collection.update_one({"name": name}, {"$set": new_values})


def fetch_characters_names():
    # Returns a list of all characters names in alphabetical order
    return [character['name'] for character in characters_collection.find().sort("name", 1)]
