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
        print(nbt) 

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
        showTagCompoundValue(nbt, tempArrayOfTags[selection], playerKey)

def showTagCompoundValue(nbt, tagName, playerKey):
    os.system('cls' if os.name == 'nt' else 'clear')

    print(f"Showing data for tag: {tagName}")

    tagValue = nbt[tagName]
    
    if isinstance(tagValue, (TAG_List)):
        for i in tagValue:
            print_nbt(i) 
    elif isinstance(tagValue, (TAG_Compound)):
        selectTagCompoundValue(tagValue, playerKey)
    else:
        print_nbt(tagValue)

    selection = int(input("Enter -1 to go back."))
    if selection == -1:
        showPlayerData(playerKey)
    else:
        showTagCompoundValue(nbt, tagName, playerKey)

def selectTagCompoundValue(CompoundTagKey, playerKey):
    tempArrayOfTags = []
    os.system('cls' if os.name == 'nt' else 'clear')

    for i, tagName in enumerate(CompoundTagKey): #compound tag is nbt
        print(f"[{i}] : {tagName}")
        tempArrayOfTags.append(tagName)

    selection = int(input("Select a tag by number: "))
    if selection == -1:
        return 
    else:   
        showTagCompoundValue(CompoundTagKey, tempArrayOfTags[selection], playerKey)

showPlayers()