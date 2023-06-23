from utils.db import characters_collection, manas_collection, users_collection, abilities_collection
from utils.characters.aggregations import max_hp, max_mp, max_sp
from utils.characters.character import get_character_by_name

from bson.objectid import ObjectId

def fetch_abilities_by_character_name(name):
    # Get the character document
    character = get_character_by_name(name)
    # Get the list of abilities ObjectId's
    ability_ids = character['abilities']
    # Replace the list of abilities ObjectId's with the actual abilities documents
    character['abilities'] = [abilities_collection.find_one({"_id": ObjectId(ability_id)}) for ability_id in ability_ids] 
    return character['abilities']
