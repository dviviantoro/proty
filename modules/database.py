import os, sys, lmdb, json
from tinydb import TinyDB, Query
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.util import *

db_app_path = temp_dir / "app.json"
db = TinyDB(db_app_path)

def tinydb_insert_dict(category, dict_data):
    table = db.table(category)
    table.insert(dict_data)
    logger.info(f"tinydb record {category} data: {dict_data}")

def tinydb_read(category):
    table = db.table(category)
    return table.all()

def tinydb_check_existence(category, name):
    table = db.table(category)
    return True if table.search(Query().name == name) != [] else False


def tinydb_change_phase(phase):
    table = db.table("general")
    table.update({"phase": phase})
    return table.all()

def tinydb_update_temp(key, value):
    tbl = db.table("temp")
    tbl.update({key: value})
    return tbl.all()

# pisahin .json nya buat calibrasi dan bgn. karena bakal nyampah banget di app.json
def tinydb_append_xy(category, project, xy):
    table = db.table(category)
    current_project = table.search(Query().name == project)
    try:
        current_project[0]["xy"].append(xy)
        table.update({'xy': current_project[0]["xy"]}, Query().name == project)
    except Exception as e:
        print(e)
        table.update({'xy': [xy]}, Query().name == project)

class LMDBDict:
    def __init__(self, db_path: str = str(temp_dir), map_size: int = 1024 * 1024 * 50):
        """
        Initializes the database environment.
        
        Args:
            db_path (str): The directory path for the LMDB database.
            map_size (int): The maximum size the database can grow to, in bytes.
        """
        # Create the directory if it doesn't exist
        os.makedirs(db_path, exist_ok=True)
        self.env = lmdb.open(db_path, map_size=map_size)

    def put(self, key: str, value_dict: dict):
        """
        Stores a dictionary value for a given string key.
        """
        if not isinstance(value_dict, dict):
            raise TypeError("Value must be a dictionary.")
            
        key_bytes = key.encode('utf-8')
        value_bytes = json.dumps(value_dict).encode('utf-8')
        
        with self.env.begin(write=True) as txn:
            txn.put(key_bytes, value_bytes)

    def get(self, key: str) -> dict | None:
        """
        Retrieves a dictionary for a given string key.
        Returns None if the key does not exist.
        """
        key_bytes = key.encode('utf-8')
        
        with self.env.begin() as txn:
            value_bytes = txn.get(key_bytes)
            if value_bytes is None:
                return None
            return json.loads(value_bytes.decode('utf-8'))

    def delete(self, key: str) -> bool:
        """
        Deletes a key-value pair from the database.
        Returns True on success, False if key did not exist.
        """
        key_bytes = key.encode('utf-8')
        with self.env.begin(write=True) as txn:
            return txn.delete(key_bytes)

    def close(self):
        """Closes the database environment."""
        self.env.close()

    def __enter__(self):
        """Enables usage with the 'with' statement."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the environment when exiting the 'with' block."""
        self.close()
