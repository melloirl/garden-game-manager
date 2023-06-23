from utils.db import characters_collection, manas_collection, users_collection

from bson.objectid import ObjectId 

def get_all_users():
    # Get all users from the database
    return list(users_collection.find())



def get_user_by_attr(attr, value):
    # Get the user by the given attribute and value
    user = users_collection.find_one({attr: value})
    # If there are multiple users with the same attribute and value, return the first one
    if isinstance(user, list):
        # Populate the user's characters
        user['characters'] = [characters_collection.find_one(
            {"_id": ObjectId(character_id)}) for character_id in user['characters']]
        return user[0]
    # If there are no users with the given attribute and value, return None
    if not user:
        return None
    # Return the user
    # Populate the user's characters
    user['characters'] = [characters_collection.find_one(
        {"_id": ObjectId(character_id)}) for character_id in user['characters']]
    return user
    
    