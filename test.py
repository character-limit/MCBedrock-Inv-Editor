import plyvel
import amulet_nbt
from amulet_nbt import utf8_escape_decoder

db_dir="ExampleWorld/db"
db = plyvel.DB(db_dir, create_if_missing=False)

print(db.closed)

db.close()