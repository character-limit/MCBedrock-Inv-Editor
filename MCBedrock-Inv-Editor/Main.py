import string
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


""" iterator.seek(b'actorprefix')

nbt = amulet_nbt.load(iterator.value(), little_endian=True, string_decoder=utf8_escape_decoder)

print_nbt(nbt) """


# Dictionary to hold all actorprefix values FORMAT: entityType:count
allEntities = {}

""" # Loop through every actorprefix key value pair
for(key, value) in db.iterate(start=b"actorprefix", end=b"actorprefix\xff"):  
    print(f"key: {key} , Value len: {len(value)}") """

for(key, value) in db.iterate(start=b"actorprefix", end=b"actorprefix\xff"): # Loop through all keys that start with actorprefix 0 \xff allows for characters after actorprefix
    nbt = amulet_nbt.load(value, little_endian=True, string_decoder=utf8_escape_decoder) # Load the nbt from the value
    nbt.compound # Convert into object so can reference specific parts of the nbt - reference with nbt["name"] eg: nbt["identifier"].

    entityType = str(nbt["identifier"])

    # Count total of each entity type
    if entityType in allEntities:
        allEntities[entityType] += 1
    else:
        allEntities[entityType] = 1

print(allEntities)
    


    