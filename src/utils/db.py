from pymongo import MongoClient
from dotenv import load_dotenv
import os

# load the MongoDB URI
load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
MONGO_DB = os.getenv('MONGO_DB')
# establish a new client connection
client = MongoClient(MONGO_URI)

# define the database name, replace `your_database` with your actual database name
db = client[MONGO_DB]

# define your collections
characters_collection = db['characters']
abilities_collection = db['abilities']
manas_collection = db['manas']
users_collection = db['users']
# add more collections as needed