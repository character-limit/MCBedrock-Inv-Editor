from leveldb import LevelDB
import amulet_nbt;
from amulet_nbt import utf8_escape_decoder
from amulet_nbt import TAG_List, TAG_Compound
import os

# Initialise DB folder in world file to leveldb
db_filename="ExampleWorld/db"
db = LevelDB(db_filename, create_if_missing=False)

# Print nbt but pretty function
def print_nbt(nbt):
    if isinstance(nbt, (TAG_List, TAG_Compound)):
        print(nbt.to_snbt(indent=4))
    else:
        print(nbt)  # for Python primitives like int, str, float

# Init iterator for db
iterator = db.new_iterator()


arrayOfPlayers = []

for key in db.keys():
    if key.__contains__(b"player"):
        arrayOfPlayers.append(key)



def showPlayers():
    print ("The players in this world are:")
    for i, playerKey in enumerate(arrayOfPlayers):
        print(f"[{i}] : {playerKey}")
    
    selection = int(input("Select a player by number: "))
    showPlayerData(arrayOfPlayers[selection])

def showPlayerData(playerKey):
    tempArrayOfTags = []
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Showing data for player key: {playerKey}")

    nbt = amulet_nbt.load(db[playerKey], little_endian=True, string_decoder=utf8_escape_decoder).compound
    for i, tagName in enumerate(nbt):
        print(f"[{i}] : {tagName}")
        tempArrayOfTags.append(tagName)

    selection = int(input("Select a tag by number: "))
    if selection == -1:
        showPlayers()
    else:   
        showTagValue(nbt, tempArrayOfTags[selection], playerKey)

def showTagValue(nbt, tagName, playerKey):
    os.system('cls' if os.name == 'nt' else 'clear')

    print(f"Showing data for tag: {tagName}")

    tag_value = nbt[tagName]
    
    if isinstance(tag_value, (TAG_Compound, TAG_List)):
        for i in tag_value:
            print_nbt(i) 
    else:
        print_nbt(tag_value)

    selection = int(input("Enter -1 to go back."))
    if selection == -1:
        showPlayerData(playerKey)
    else:   
        showTagValue(nbt, tagName, playerKey)

showPlayers()