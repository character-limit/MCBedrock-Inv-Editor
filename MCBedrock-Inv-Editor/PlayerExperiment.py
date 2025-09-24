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

# print(db[b"~local_player"]) #print key that is prefixed with ~local_player

nbt = amulet_nbt.load(db[b"~local_player"], little_endian=True, string_decoder=utf8_escape_decoder).compound

for i in nbt["Inventory"]: # output the inventory
    itemName = str(i["Name"])

    if itemName.startswith("minecraft:"): # remove minecraft: prefix
        itemName = itemName[10:]

        if "tag" in i:
            itemName = itemName + "\nDETAILS: " + str(i["tag"]) # print with tag info if its there (includes enchants, custom names etc)

    if itemName == "":
        itemName = "empty"
    
    print (f"{itemName} x {i['Count']}") # print item name and count
    print() # newline for readability
