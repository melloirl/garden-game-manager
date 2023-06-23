from utils.db import characters_collection, manas_collection, users_collection

from bson.objectid import ObjectId

# This function returns an aggregation pipeline that will be used to get the character max stats

def max_hp():
    return [{"$addFields": {
        "max_hp": {
            "$switch": {
                "branches": [
                    {"case": {"$eq": ["$race", "Humano"]},
                     "then": {"$add": [50, {"$multiply": [1.2, {"$multiply": ["$vitality", 10]}]}, {"$multiply": ["$level", 5]}]}},
                    {"case": {"$eq": ["$race", "Descendente"]},
                     "then": {"$add": [40, {"$multiply": [0.9, {"$multiply": ["$vitality", 10]}]}, {"$multiply": ["$level", 5]}]}},
                    {"case": {"$eq": ["$race", "Híbrido"]},
                     "then": {"$add": [45, {"$multiply": ["$vitality", 10]}, {"$multiply": ["$level", 5]}]}}
                ],
                "default": "Race not recognized"
            }
        }, 
    }}]

def max_mp():
    return [{"$addFields": {
        "max_mp": {
            "$switch": {
                "branches": [
                    {"case": {"$eq": ["$race", "Humano"]},
                     "then": {"$add": [30, {"$multiply": ["$mana", 8]}, {"$multiply": ["$control", 2]}, {"$multiply": ["$level", 3]}]}},
                    {"case": {"$eq": ["$race", "Descendente"]},
                     "then": {"$add": [50, {"$multiply": [1.2, {"$multiply": ["$mana", 8]}]}, {"$multiply": ["$control", 2]}, {"$multiply": ["$level", 3]}]}},
                    {"case": {"$eq": ["$race", "Híbrido"]},
                     "then": {"$add": [45, {"$multiply": [1.1, {"$multiply": ["$mana", 8]}]}, {"$multiply": ["$control", 2]}, {"$multiply": ["$level", 3]}]}},
                ],
                "default": "Race not recognized"
            }
        }, 
    }}]

def max_sp():
    return [{"$addFields": {
        "max_sp": {
            "$switch": {
                "branches": [
                    {"case": {"$eq": ["$race", "Humano"]},
                     "then": {"$add": [40, {"$multiply": ["$strength", 5]}, {"$multiply": ["$dexterity", 5]}, {"$multiply": ["$level", 4]}]}},
                    {"case": {"$eq": ["$race", "Descendente"]},
                     "then": {"$add": [40, {"$multiply": ["$strength", 5]}, {"$multiply": ["$dexterity", 5]}, {"$multiply": ["$level", 4]}]}},
                    {"case": {"$eq": ["$race", "Híbrido"]},
                     "then": {"$add": [50, {"$multiply": [1.1, {"$multiply": ["$strength", 5]}]}, {"$multiply": [1.1, {"$multiply": ["$dexterity", 5]}]}, {"$multiply": ["$level", 4]}]}},
                ],
                "default": "Race not recognized"
            }
        }, 
    }}]

 