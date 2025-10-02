from leveldb import LevelDB
import amulet_nbt
from amulet_nbt import utf8_escape_decoder

# Initialise DB folder in world file to leveldb
db_filename="sampleworld/db"
db = LevelDB(db_filename)

# Print nbt but pretty function
def print_nbt(nbt):
    print(nbt.to_snbt(indent=4))

# Init iterator for db
iterator = db.new_iterator()

#loop to find how many key value pairs are in the db
numKeys = 0
print("retrieving number of keys, please wait.")
for i in db.keys():
    numKeys += 1
print(f"Total keys: {numKeys}")


# Dictionary to hold all actorprefix values FORMAT: name:count
allEntities = {}

for(key, value) in db.iterate(start=b"actorprefix", end=b"actorprefix\xff"): # Loop through all keys that start with actorprefix 0 \xff allows for characters after actorprefix
    nbt = amulet_nbt.load(value, little_endian=True, string_decoder=utf8_escape_decoder) # Load the nbt from the value
    nbt.compound # Convert into object so can reference specific parts of the nbt - reference with nbt["name"] eg: nbt["identifier"].

    entityType = str(nbt["identifier"]) # Get the entitys identifier data

    # Count total of each entity type
    if entityType == "minecraft:item":
        itemObj = nbt["Item"]
        if "Block" in itemObj:
            id = f"{str(nbt['Item']['Block']['name'])}"
        else:
            id = f"{str(nbt['Item']['Name'])}"

    if id in allEntities:
        allEntities[id] += 1
    else:
        allEntities[id] = 1
        
for (key, value) in allEntities.items():
    print(f"{key} : {value}") # key is name, value is count of that entity type

# the end result of this program should output all of the dropped items and their counts in the world.