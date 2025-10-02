from leveldb import LevelDB
import amulet_nbt
from amulet_nbt import utf8_escape_decoder

# Initialise DB folder in world file to leveldb
db_filename="ExampleWorld/db"
db = LevelDB(db_filename, create_if_missing=False)

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

for i in nbt["Inventory"]: # output the inventory PARAMS: "Inventory", "EnderChestInventory", "Armor"
    itemName = str(i["Name"])

    if itemName.startswith("minecraft:"): # remove minecraft: prefix
        itemName = itemName[10:]

        if "tag" in i:
            itemName = itemName + "\nDETAILS: " + str(i["tag"]) # print with tag info if its there (includes enchants, custom names etc)

    if itemName == "":
        itemName = "empty"
    
    print (f"{i['Count']} x {itemName}") # print item name and count
    print() # newline for readability



print("---------------------Armour---------------------")

for i in nbt["Armor"]: # output the armor
    #print_nbt(i)
    itemName = str(i["Name"])
    if itemName.startswith("minecraft:"): # remove minecraft: prefix
        itemName = itemName[10:]

        if "tag" in i:
            itemName = itemName + "\nDETAILS: " + str(i["tag"]) # print with tag info if its there (includes enchants, custom names etc)

    if itemName == "":
        itemName = "empty"

    print (f"{i['Count']} x {itemName}") # print item name and count
    print() # newline for readability


print(f"Mainhand - {str(nbt['Mainhand'][0]['Name'])[10:]}")
print(f"Offhand - {str(nbt['Offhand'][0]['Name'])[10:]}")
print(f"Pos - {nbt['Pos']}")



# now lets look at players that arent local_player
print("---------------------Other Players---------------------")

for key in db.keys():
    if key.startswith(b"player"):
        print("Found player key:", key)

nbt = amulet_nbt.load(db[b"player_server_18672b95-daa0-4f02-9286-88428fa48a5c"], little_endian=True, string_decoder=utf8_escape_decoder).compound

db.close()

#print_nbt(nbt)
        
# complete example for showing local player data, other remote players, and their data.